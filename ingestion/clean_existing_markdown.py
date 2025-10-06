#!/usr/bin/env python3
import os
import sys
import argparse
import json
from pathlib import Path
from typing import Tuple, Dict
from dotenv import load_dotenv
from openai import OpenAI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch clean existing markdown files with GPT-4o mini (removes nav/headers/footers/boilerplate)")
    parser.add_argument("--input-dir", required=True,
                        help="Directory containing .md files to clean (e.g., ingestion/client_ingestion_outputs/reach_marketing/website)")
    parser.add_argument("--output-dir", default="",
                        help="Directory to write cleaned files. If omitted and --in-place not set, writes to '<input-dir>_cleaned'")
    parser.add_argument("--in-place", action="store_true",
                        help="Overwrite files in-place (use with caution)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of files to process (0 = no limit)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without writing output")
    parser.add_argument("--max-chars", type=int, default=120000,
                        help="Max characters of input markdown to send to LLM per file")
    return parser.parse_args()


def ensure_output_dir(input_dir: Path, output_dir_arg: str, in_place: bool) -> Path:
    if in_place:
        return input_dir
    if output_dir_arg:
        out = Path(output_dir_arg)
    else:
        out = Path(str(input_dir) + "_cleaned")
    out.mkdir(parents=True, exist_ok=True)
    return out


def split_frontmatter(markdown_text: str) -> Tuple[Dict[str, str], str]:
    """
    Split YAML frontmatter (simple key: value pairs) from the markdown body.
    Returns (frontmatter_dict, body_text). If no frontmatter, returns ({}, full_text).
    """
    if markdown_text.startswith("---\n"):
        end_idx = markdown_text.find("\n---\n", 4)
        if end_idx != -1:
            fm_text = markdown_text[4:end_idx]
            body = markdown_text[end_idx + 5:]
            fm_dict: Dict[str, str] = {}
            for line in fm_text.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    fm_dict[key.strip()] = val.strip().strip('"')
            return fm_dict, body
    return {}, markdown_text


def assemble_frontmatter(fm: Dict[str, str]) -> str:
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, str):
            safe = v.replace('"', '\"').replace('\n', ' ').replace('\r', ' ')
            lines.append(f"{k}: \"{safe}\"")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---\n\n")
    return "\n".join(lines)


def llm_clean_markdown_content(markdown_content: str, max_chars: int) -> Tuple[str, str]:
    """
    Clean raw markdown using GPT-4o mini to remove navigation, headers, footers, and boilerplate
    while preserving core informational content and structure. Returns (cleaned_markdown, title).
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    content = markdown_content
    if len(content) > max_chars:
        content = content[:max_chars]

    client = OpenAI(api_key=api_key)

    system_instructions = (
        "You are an expert content extraction assistant. Given a single web page in Markdown, "
        "return only the substantive article/page content. Remove navigation menus, headers, footers, "
        "sidebars, cookie notices, forms, repeated link lists, social links, and boilerplate. Preserve "
        "semantic structure (headings, paragraphs, lists, code blocks). Do not invent content. "
        "If multiple sections exist (e.g., hero + body), keep the meaningful text and headings only. "
        "Do not include site-wide menus or footers."
    )

    user_prompt = (
        "Clean the following Markdown. Return a strict JSON object with keys 'title' and 'content_md'. "
        "- 'title' should be a concise page title inferred from the H1 or the main content. "
        "- 'content_md' should be the cleaned Markdown only, no extra commentary.\n\n"
        "```markdown\n" + content + "\n```"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=4096,
    )
    text = response.choices[0].message.content or ""

    # Try JSON parse
    title = ""
    cleaned = ""
    try:
        data = json.loads(text)
        title = (data.get("title") or "").strip()
        cleaned = (data.get("content_md") or "").strip()
    except Exception:
        # Fallback: use the raw text, derive title from first H1
        cleaned = text
        for ln in cleaned.splitlines():
            ln = ln.strip()
            if ln.startswith('# '):
                title = ln[2:].strip()
                break

    if not cleaned:
        return "", ""
    if not title:
        for ln in cleaned.splitlines():
            ln = ln.strip()
            if ln.startswith('# '):
                title = ln[2:].strip()
                break
    return cleaned, title


def process_file(path: Path, out_dir: Path, in_place: bool, max_chars: int, dry_run: bool) -> Tuple[bool, str]:
    try:
        original = path.read_text(encoding="utf-8", errors="ignore")
        fm, body = split_frontmatter(original)

        cleaned_md, title = llm_clean_markdown_content(body, max_chars=max_chars)
        if not cleaned_md:
            return False, f"LLM returned empty content: {path.name}"

        # Update frontmatter
        fm = dict(fm)
        if title:
            fm.setdefault("title", title)
        fm["post_clean_llm"] = "true"
        fm["word_count"] = str(len(cleaned_md.split()))

        output_text = assemble_frontmatter(fm) + cleaned_md

        target_path = path if in_place else (out_dir / path.name)
        if dry_run:
            return True, f"DRY-RUN would write: {target_path}"

        target_path.write_text(output_text, encoding="utf-8")
        return True, f"Wrote: {target_path}"
    except Exception as e:
        return False, f"Error processing {path.name}: {e}"


def main() -> int:
    load_dotenv()
    args = parse_args()

    input_dir = Path(args.input_dir).resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: input dir not found: {input_dir}", file=sys.stderr)
        return 1

    output_dir = ensure_output_dir(input_dir, args.output_dir, args.in_place)

    md_files = sorted(list(input_dir.glob("*.md")))
    if args.limit > 0:
        md_files = md_files[:args.limit]

    if not md_files:
        print("No markdown files found.")
        return 0

    success = 0
    fail = 0
    for idx, md in enumerate(md_files, start=1):
        ok, msg = process_file(md, output_dir, args.in_place, args.max_chars, args.dry_run)
        print(f"[{idx}/{len(md_files)}] {msg}")
        if ok:
            success += 1
        else:
            fail += 1

    print(f"Done. Success: {success}, Failed: {fail}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
