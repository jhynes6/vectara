#!/usr/bin/env python3
"""
Supabase Client Brief Generator - Comprehensive Client Analysis

This script generates comprehensive client briefs using Supabase Vector DB
for RAG retrieval instead of Vectara.

Usage:
    python supabase_brief_generator.py --client-id "client-name"
    python supabase_brief_generator.py --client-id "client-name" --output brief.md
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import psycopg2

from openai import OpenAI
from dotenv import load_dotenv

# Import Supabase vector store
from supabase_vector_store import SupabaseVectorStore

load_dotenv(override=True)

# Utility to run a list of coroutines concurrently (wrapper for asyncio.gather)
import asyncio as _asyncio_mod

async def _run_all(_coros):
    return await _asyncio_mod.gather(*_coros)

def _run_concurrently(_coros):
    """
    Run coroutines concurrently, handling both sync and async contexts.
    If we're already in an event loop, use asyncio.create_task().
    Otherwise, use asyncio.run().
    """
    try:
        # Check if we're already in an event loop
        loop = _asyncio_mod.get_running_loop()
        # We're in an async context, need to handle differently
        import concurrent.futures
        import threading
        
        def run_in_thread():
            return _asyncio_mod.run(_run_all(_coros))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_in_thread)
            return future.result()
            
    except RuntimeError:
        # No event loop running, safe to use asyncio.run()
        return _asyncio_mod.run(_run_all(_coros))

# Embedded prompt instructions (migrated from vertex_ai_rag/agents/shared_prompts.py)
CASE_STUDY_SUMMARIZER_INSTRUCTIONS = """when asked to summarize case studies, format the response as follows:

0. CLIENT: the name of the client in the case study
1. INDUSTRY: the industry category of the CLIENT (rather than the subject of the case) in the case study.

2. SERVICES: the service(s) that were rendered (bullet point list). Try not to be too broad with the service by returning something like "marketing services", instead i'd rather see the individual services that are often sold as standalone services: SEO, PPC, Content, Social Media, Email, Branding, paid media, Public Relations, Direct Marketing, OR Experiential Marketing (assuming the case study mentions it). You should not have more than 5 results for this for a given case study. 

3. RESULTS: extract and list all quantitative results and all qualitative results found in the case study. Limit the Qualitative Results to 5 bullet points. Do not summarize or condense The Quantitative Results into a smaller set of representative points. Only combine if exact duplicates are present. If no quantitative or qualitative results are provided, explicitly state: "No quantitative results provided" or "No qualitative results provided."

4. MECHANISM: the specific mechanism(s) by which the results were achieved. This should answer the question: "How did [service, ex: paid ads] [result, ex: 4x revenue]."

5. SOURCE: the url from the metadata for the --doc-id we are currently summarizing. 

6. CASE STUDY QUALITY: 

Display CASE STUDY QUALITY LIKE THIS (don't include the quotes): 
--
-  COMPOSITE SCORE: 0.93

-  BREAKDOWN: 
  - Results: 0.95
  - Mechanism: 0.90
  - Services: 0.90
  - Industry: 0.95
- Weighted calculation: (0.95×0.40) + (0.90×0.25) + (0.90×0.20) + (0.95×0.15) = 0.9275
--

Here is the info you need on how to calculate CASE STUDY QUALITY to and generate the values shown above: 

You are evaluating the completeness and quality of a business case study. Provide a quality score from 0.0 to 1.0 based on the following weighted criteria:

## CALCULATION METHOD

1. Score each component (0.0-1.0)
2. Apply weights: (Results × 0.4) + (Mechanism × 0.25) + (Services × 0.2) + (Industry × 0.15)
3. APPLY CAP: If Quantifiable Results score ≤ 0.5, cap final score at 0.6
4. Round final score to 2 decimal places

## SCORE INTERPRETATION

- 0.9-1.0: Exceptional case study with 3+ quantifiable results, clear mechanisms, detailed services, and industry context
- 0.8-0.89: Strong case study with 2+ quantifiable results and most other elements
- 0.7-0.79: Good case study with 1+ results but missing some detail
- 0.6: Maximum score for studies lacking strong quantifiable results
- 0.4-0.59: Incomplete case study missing major elements
- 0.1-0.39: Poor case study with minimal useful information
- 0.0: No useful case study content (missing all core elements)"""

CLIENT_INTAKE_FORM_SUMMARIZER_INSTRUCTIONS = """when asked to summarize the client intake form, summarize the content as follows: 

When summarizing the client intake form, you identify the following:

1. TARGET MARKET: the client's target market. focus on industries, headcounts, and company demographics
2. SERVICES: the client's service offerings they provide
3. CASE STUDIES: the case studies provided by the client
4. PAIN POINTS: the pain points of our client's ideal client
5. OFFERS: response to "For each service, what are your top offers (packages/examples) that you would be willing to pitch them?"
6. SERVICE DIFFERENTIATION: how our client is different
7. PRICING: our client's typical pricing packages"""

CLIENT_MATERIALS_SUMMARIZER_INSTRUCTIONS = """your job is to analyze the content of each file and extract any information that would be useful for helping us generate a go to market strategy for our client.

For the .md files, if the section "## LLM Page Analysis" exists in the .md file, you will only summarize the text AFTER the "## LLM Page Analysis" tag from the .md file. The previous section is "## Extracted Text" and can be ignored for now. 

Return your response in this format: 

1. DOC NAME: [normalized document id from the vectara knowledge base]
2. URL: [link to the drive file] 
3, CONTENT OVERVIEW: [explain the contents of the doc in 1 sentence]

4. DETAILED SUMMARY: provide a detailed summary of the doc. for the DETAILED SUMMARY, we are generally NOT interested in information about OUR client (ex: team size, pricing, etc) but we ARE interested in any information that could be useful for positioning their services to their target market. Keep an eye out for any compelling information that could be used to market out client's brand. 
  
5. SOURCE: Include the source URL from the document metadata. Look for a "url" field in the document metadata and include it as "Source: [URL]". If no URL is found in the metadata, state "Source: Not available"."""

CLIENT_WEBSITE_SUMMARIZER_INSTRUCTIONS =  """
            When asked to analyze website content by content type, provide a focused analysis in the following format:

            ### Services Offered
            Based on this specific content type, list all services mentioned:
            - List each service name clearly
            - Include any sub-services or specializations
            - Note unique approaches or methodologies
            - Be comprehensive and specific to this content type

            ### Target Industries  
            Based on this specific content type, list all target industries mentioned:
            - Industries explicitly mentioned as target markets
            - Industries implied by context or descriptions
            - Vertical markets or specialized sectors
            - Geographic focus or market segments
            - Be comprehensive and specific to this content type

            ### Content Type Notes
            - Focus specifically on the content type being analyzed
            - Extract ALL services and industries mentioned in this content type
            - Be thorough and complete for this specific content section
            - If no services or industries are mentioned, state "None found in this content type"

            Provide a clean, focused analysis for the specific content type being queried.
            """

# Unique Mechanism Research prompt
UNIQUE_MECHANISM_SYSTEM_PROMPT = (
    "Using the services listed in the ##CASE STUDIES ANALYSIS section, the ##Client Intake Form Analysis section and the  ## Website Summary section, "
    "select up to 5 services to research new trends for.\n\n"
    "After you've selected your five, research \"new advanced strategies for [service x] in 2025\" and summarize those strategies for a given service. "
    "the key is that we want to know the precise mechanism that a given strategy uses to generate results"
)


def _web_search_google_cse(query: str, num: int = 5) -> List[Dict[str, str]]:
    api_key = os.getenv('GOOGLE_API_KEY')
    cse_id = os.getenv('GOOGLE_CSE_ID')
    if not api_key or not cse_id:
        return []
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': max(1, min(num, 10)),
        'safe': 'off'
    }
    try:
        resp = requests.get('https://www.googleapis.com/customsearch/v1', params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        items = data.get('items', []) or []
        results = []
        for it in items:
            results.append({
                'title': it.get('title', ''),
                'link': it.get('link', ''),
                'snippet': it.get('snippet', '')
            })
        return results
    except Exception:
        return []


def _web_search_serpapi(query: str, num: int = 5) -> List[Dict[str, str]]:
    api_key = os.getenv('SERPAPI_API_KEY')
    if not api_key:
        return []
    params = {
        'engine': 'google',
        'q': query,
        'api_key': api_key,
        'num': max(1, min(num, 10))
    }
    try:
        resp = requests.get('https://serpapi.com/search.json', params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        organic = data.get('organic_results', []) or []
        results = []
        for it in organic[:num]:
            results.append({
                'title': it.get('title', ''),
                'link': it.get('link', ''),
                'snippet': it.get('snippet', '')
            })
        return results
    except Exception:
        return []

def _web_search_brightdata_serp(query: str, num: int = 5) -> List[Dict[str, str]]:
    """Fallback: Use Bright Data Web Unlocker to fetch Google SERP HTML and scrape results."""
    api_token = os.getenv('BRIGHTDATA_API_TOKEN') or os.getenv('API_TOKEN')
    zone = os.getenv('WEB_UNLOCKER_ZONE', 'web_unlocker1')
    if not api_token:
        return []
    try:
        google_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&hl=en&num={max(10, num*2)}"
        payload = json.dumps({
            "zone": zone,
            "url": google_url,
            "format": "raw",
            "method": "GET",
            "country": "US"
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_token}'
        }
        resp = requests.post("https://api.brightdata.com/request?async=true", headers=headers, data=payload, timeout=40)
        resp.raise_for_status()
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        results: List[Dict[str, str]] = []
        # Common Google SERP structure: h3 inside a link
        for h3 in soup.select('a h3'):
            title = h3.get_text(strip=True)
            a = h3.find_parent('a')
            href = a.get('href') if a else ''
            # Attempt to find nearby snippet
            snippet = ''
            snippet_div = None
            # Look ahead for a typical snippet container
            parent = a.find_parent('div') if a else None
            if parent:
                snippet_div = parent.find_next('div')
            if snippet_div:
                snippet = snippet_div.get_text(" ", strip=True)[:300]
            if title and href:
                results.append({'title': title, 'link': href, 'snippet': snippet})
            if len(results) >= num:
                break
        return results
    except Exception:
        return []

# Update unified search to include Bright Data as final fallback
def _web_search(query: str, num: int = 5) -> List[Dict[str, str]]:
    r = _web_search_google_cse(query, num)
    if r:
        return r
    r = _web_search_serpapi(query, num)
    if r:
        return r
    return _web_search_brightdata_serp(query, num)


class SupabaseClientBriefGenerator:
    """Generator for comprehensive client briefs using Supabase RAG"""
    
    def __init__(self, client_id: str, drive_folder_id: str = None, 
                 credentials_file: str = "./service_account.json"):
        """
        Initialize the Client Brief Generator
        
        Args:f
            client_id: Client identifier
            drive_folder_id: Optional Drive folder ID for upload
            credentials_file: Path to service account JSON
        """
        self.client_id = client_id
        self.drive_folder_id = drive_folder_id
        self.credentials_file = credentials_file
        
        # Initialize OpenAI
        openai_key = os.environ.get('OPENAI_API_KEY')
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self.openai_client = OpenAI(api_key=openai_key)
        
        # Initialize Supabase vector store
        self.vector_store = SupabaseVectorStore()
        
        # Concurrency controls
        try:
            self.llm_concurrency = max(1, int(os.getenv('BRIEF_LLM_CONCURRENCY', '6')))
        except Exception:
            self.llm_concurrency = 6
        
        print(f"✅ Initialized brief generator for client: {client_id}")
    
    def query_content_type(self, content_type: str, query: str, limit: int = 50) -> List[Dict]:
        """
        Query specific content type from Supabase
        
        Args:
            content_type: Content type to filter
            query: Query text
            limit: Maximum results
            
        Returns:
            List of matching documents
        """
        results = self.vector_store.query_documents(
            client_id=self.client_id,
            query=query,
            limit=limit,
            content_type_filter=content_type,
            similarity_threshold=1
        )
        return results
    
    def query_all_content(self, query: str, limit: int = 30) -> List[Dict]:
        """Query all content types"""
        results = self.vector_store.query_documents(
            client_id=self.client_id,
            query=query,
            limit=limit,
            similarity_threshold=0.6
        )
        return results
    
    def generate_case_studies_section(self) -> str:
        """Generate case studies section"""
        print("📊 Generating case studies section...")
        
        # Query case studies (empty query => latest items matching filters)
        results = self.query_content_type(
            content_type="case_studies",
            query="",
            limit=500
        )
        
        if not results:
            return "No case studies available.\n"
        
        import asyncio
        sem = asyncio.Semaphore(self.llm_concurrency)
        
        async def summarize_one(doc: Dict[str, Any]) -> str:
            title = doc.get('title', '') or 'Untitled Case Study'
            meta = doc.get('metadata') or {}
            url = None
            if isinstance(meta, dict):
                url = meta.get('url') or meta.get('uri')
            excerpt = (doc.get('content', '') or '')[:4000]
            messages = [
                {"role": "system", "content": CASE_STUDY_SUMMARIZER_INSTRUCTIONS},
                {"role": "user", "content": f"Document Title: {title}\nSource: {url or 'N/A'}\n\nContent (excerpt):\n{excerpt}"}
            ]
            try:
                async with sem:
                    resp = await asyncio.to_thread(
                        self.openai_client.chat.completions.create,
                        model="gpt-5-mini",
                        messages=messages,
                        temperature=1,
                        reasoning_effort="medium",
                    )
                return f"### {title}\n\n{resp.choices[0].message.content}\n"
            except Exception as e:
                return f"### {title}\n\n*Error summarizing this case study: {e}*\n"
        
        summaries = _run_concurrently([summarize_one(r) for r in results])
        
        return "\n".join(summaries) + "\n"
    
    def generate_client_intake_section(self) -> str:
        """Generate client intake form section"""
        print("📝 Generating client intake section...")
        
        results = self.query_content_type(
            content_type="client_intake",  # content_type key for intake docs
            query="",
            limit=5
        )
        
        if not results:
            return "## CLIENT INTAKE FORM\n\nNo intake form data available.\n"
        
        # Build context from the top few documents
        context = "\n\n".join([r.get('content','') for r in results[:3]])
        messages = [
            {"role": "system", "content": CLIENT_INTAKE_FORM_SUMMARIZER_INSTRUCTIONS},
            {"role": "user", "content": f"Use ONLY the following intake form excerpts as context.\n\n{context}"}
        ]
        
        response = self.openai_client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            temperature=1, 
            reasoning_effort="medium"
        )
        
        return f"## CLIENT INTAKE FORM\n\n{response.choices[0].message.content}\n"
    
    def generate_client_materials_summary(self) -> str:
        """Summarize client materials (non-case-study) documents"""
        print("📦 Generating client materials summary...")
        
        # Get all client_materials (empty query => first chunk per doc) and exclude case_studies
        results = self.vector_store.query_documents(
            client_id=self.client_id,
            query="",
            limit=200,
            source_type_filter="client_materials"
        )
        results = [r for r in results if r.get('content_type') != 'case_studies']
        
        if not results:
            return "## CLIENT MATERIALS SUMMARY\n\nNo client materials available.\n"
        
        import asyncio
        sem = asyncio.Semaphore(self.llm_concurrency)
        
        async def summarize_one(doc: Dict[str, Any]) -> str:
            title = doc.get('title', '') or 'Untitled Document'
            meta = doc.get('metadata') or {}
            url = None
            if isinstance(meta, dict):
                url = meta.get('url') or meta.get('uri')
            excerpt = (doc.get('content', '') or '')[:3000]
            messages = [
                {"role": "system", "content": CLIENT_MATERIALS_SUMMARIZER_INSTRUCTIONS},
                {"role": "user", "content": f"Document Title: {title}\nSource: {url or 'N/A'}\n\nContent (excerpt):\n{excerpt}"}
            ]
            try:
                async with sem:
                    resp = await asyncio.to_thread(
                        self.openai_client.chat.completions.create,
                        model="gpt-5-mini",
                        messages=messages,
                        temperature=1,
                        reasoning_effort="medium"
                    )
                return f"### {title}\n\n{resp.choices[0].message.content}\n"
            except Exception as e:
                return f"### {title}\n\n*Error summarizing this document: {e}*\n"
        
        summaries = _run_concurrently([summarize_one(r) for r in results])
        
        return "## CLIENT MATERIALS SUMMARY\n\n" + "\n".join(summaries) + "\n"
    
    def generate_website_summary(self) -> str:
        """Generate website content summary using website-only documents"""
        print("�� Generating website summary...")
        
        # Pull recent website docs (empty query => first chunk per doc)
        results = self.vector_store.query_documents(
            client_id=self.client_id,
            query="",
            limit=20,
            source_type_filter="website"
        )
        
        if not results:
            return "## WEBSITE SUMMARY\n\nNo website content available.\n"
        
        # Build context from a subset of website docs
        rows = []
        for r in results[:15]:
            meta = r.get('metadata') or {}
            url = None
            if isinstance(meta, dict):
                url = meta.get('url') or meta.get('uri')
            rows.append(
                f"Title: {r.get('title','')}\n"
                f"URL: {url or 'N/A'}\n"
                f"Content Excerpt:\n{(r.get('content','') or '')[:700]}\n"
            )
        context = "\n\n".join(rows)
        
        messages = [
            {"role": "system", "content": CLIENT_WEBSITE_SUMMARIZER_INSTRUCTIONS},
            {"role": "user", "content": f"Generate the summary outlined in your system prompt. You can look at content_type in (services_products, blogs_resources, about, homepage, pricing) Use ONLY the following website content as context (multiple pages).\n\n{context}"}
        ]
        
        response = self.openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages,
            temperature=1,
            reasoning_effort="low"
        )
        
        return f"## WEBSITE SUMMARY\n\n{response.choices[0].message.content}\n"

    def generate_unique_mechanism_research(self, case_studies_section: str, intake_section: str, materials_section: str, website_section: str) -> str:
        """Generate Unique Mechanism Research by selecting up to 5 services and doing web research per service.
        Uses services referenced in Case Studies, Client Intake, Client Materials Summary, and Website Summary.
        """
        print("🔎 Generating unique mechanism research...")
        # Step 1: Ask the model to extract up to 5 services as JSON
        selection_messages = [
            {"role": "system", "content": UNIQUE_MECHANISM_SYSTEM_PROMPT + "\nReturn ONLY a JSON array of up to 5 service names (strings)."},
            {"role": "user", "content": (
                f"## CASE STUDIES ANALYSIS\n\n{case_studies_section}\n\n"
                f"## Client Intake Form Analysis\n\n{intake_section}\n\n"
                f"## Client Materials Summary\n\n{materials_section}\n\n"
                f"## Website Summary\n\n{website_section}"
            )}
        ]
        svc_resp = self.openai_client.chat.completions.create(
            model="gpt-5",
            messages=selection_messages,
            temperature=1,
            reasoning_effort="high"
        )
        raw = svc_resp.choices[0].message.content or "[]"
        try:
            services = json.loads(raw)
            if not isinstance(services, list):
                services = []
        except Exception:
            services = []
        services = [s for s in services if isinstance(s, str) and s.strip()][:5]
        if not services:
            return "## UNIQUE MECHANISM RESEARCH\n\nNo services identified from sections to research.\n"
        
        # Step 2: For each service, run a web search and produce a mechanism-focused summary
        import asyncio
        sem = asyncio.Semaphore(self.llm_concurrency)
        
        async def research_one(svc: str) -> str:
            query = f"new advanced strategies for {svc} in 2025"
            web_results = await asyncio.to_thread(_web_search, query, 5)
            refs = "\n".join([f"- {r.get('title','')} ({r.get('link','')})\n  {r.get('snippet','')}" for r in (web_results or [])]) or "No web results found"
            messages = [
                {"role": "system", "content": "You analyze web research to extract precise mechanisms by which strategies deliver results."},
                {"role": "user", "content": (
                    f"Service: {svc}\n"
                    f"Research query: {query}\n\n"
                    f"Web findings (titles, urls, snippets):\n{refs}\n\n"
                    "Task: Summarize new advanced strategies for this service in 2025, with emphasis on the precise mechanisms (the HOW) that lead to results."
                )}
            ]
            try:
                async with sem:
                    mech_resp = await asyncio.to_thread(
                        self.openai_client.chat.completions.create,
                        model="gpt-5",
                        messages=messages,
                        temperature=1,
                        reasoning_effort="high"
                    )
                return f"### {svc}\n\n{mech_resp.choices[0].message.content}\n\n**Query:** {query}\n"
            except Exception as e:
                return f"### {svc}\n\n*Error generating research: {e}*\n\n**Query:** {query}\n"
        
        blocks = _run_concurrently([research_one(s) for s in services])
        
        return "## UNIQUE MECHANISM RESEARCH\n\n" + "\n".join(blocks) + "\n"

    def generate_client_brief(self) -> str:
        """
        Generate complete client brief
        
        Returns:
            Complete brief as markdown string
        """
        print(f"\n{'='*80}")
        print(f"GENERATING CLIENT BRIEF: {self.client_id}")
        print(f"{'='*80}\n")
        
        # Get client stats and document breakdown for header
        stats = self.vector_store.get_client_stats(self.client_id)
        all_docs = self.vector_store.list_documents(self.client_id, limit=10000)
        case_studies_count = sum(1 for d in all_docs if (d.get('content_type') == 'case_studies'))
        intake_count = sum(1 for d in all_docs if d.get('content_type') in ('client_intake', 'client_intake_form'))
        website_types = {d.get('content_type') for d in all_docs if d.get('source_type') == 'website'}
        website_types_count = len(website_types)
        
        generated_str = datetime.now().strftime('%Y-%m-%d at %H:%M:%S')
        analysis_components = f"Case Studies ({case_studies_count}), Client Intake Forms{f' ({intake_count})' if intake_count else ''}, Website Content ({website_types_count} types)"
        
        header = (
            "# COMPREHENSIVE CLIENT BRIEF\n\n"
            f"**Generated:** {generated_str}\\\n"
            f"**Client:** {self.client_id}\\\n"
            f"**Analysis Components:** {analysis_components}\n\n"
            "---\n\n"
            "## CASE STUDIES ANALYSIS\n\n"
            f"**Total Case Studies Analyzed:** {case_studies_count} (sorted by composite score, descending)\n\n"
        )
        
        # Build brief
        brief = header
        
        # Generate sections
        try:
            case_studies_section = self.generate_case_studies_section()
            brief += case_studies_section
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating case studies: {e}")
            case_studies_section = "*Error generating section*\n\n"
            brief += case_studies_section
        
        try:
            intake_section = self.generate_client_intake_section()
            brief += intake_section
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating intake section: {e}")
            intake_section = "## CLIENT INTAKE FORM\n\n*Error generating section*\n\n"
            brief += intake_section
 
        try:
            materials_section = self.generate_client_materials_summary()
            brief += materials_section
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating client materials summary: {e}")
            materials_section = "## CLIENT MATERIALS SUMMARY\n\n*Error generating section*\n\n"
            brief += materials_section
 
        try:
            website_section = self.generate_website_summary()
            brief += website_section
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating website summary: {e}")
            website_section = "## WEBSITE SUMMARY\n\n*Error generating section*\n\n"
            brief += website_section
 
        # Unique Mechanism Research (final section)
        try:
            unique_mech = self.generate_unique_mechanism_research(
                case_studies_section,
                intake_section,
                materials_section,
                website_section,
            )
            brief += unique_mech
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating unique mechanism research: {e}")
            brief += "## UNIQUE MECHANISM RESEARCH\n\n*Error generating section*\n\n"
        
        brief += f"""
---

*This brief was automatically generated from {stats['document_count']} documents 
 using Supabase Vector DB and OpenAI gpt-5-mini.*
"""
        
        print(f"\n{'='*80}")
        print(f"✅ BRIEF GENERATION COMPLETE")
        print(f"{'='*80}\n")
        
        return brief
    
    def upload_brief_to_drive(self, brief_path: str, folder_id: str) -> Optional[str]:
        """
        Upload brief to Google Drive
        
        Args:
            brief_path: Path to brief file
            folder_id: Drive folder ID
            
        Returns:
            File ID if successful, None otherwise
        """
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_file, scopes=SCOPES
            )
            service = build('drive', 'v3', credentials=creds)
            
            file_metadata = {
                'name': Path(brief_path).name,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(brief_path, mimetype='text/markdown')
            
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
            print(f"✅ Uploaded to Drive folder: {folder_url}")
            return file_id
            
        except Exception as e:
            print(f"❌ Failed to upload to Drive: {e}")
            return None


def _get_db_conn_string() -> str:
    conn = os.getenv('SUPABASE_VECTOR_DB_CONN')
    if not conn:
        raise ValueError('SUPABASE_VECTOR_DB_CONN not set')
    return conn


def resolve_drive_folder_id_from_db(client_id: str) -> Optional[str]:
    try:
        conn = psycopg2.connect(_get_db_conn_string())
        cur = conn.cursor()
        cur.execute("SELECT drive_folder_id FROM clients WHERE client_id = %s LIMIT 1", (client_id,))
        row = cur.fetchone()
        cur.close(); conn.close()
        if row and row[0]:
            return row[0]
    except Exception as e:
        print(f"⚠️  Could not resolve Drive folder from DB: {e}")
    return None


def save_brief_to_supabase_db(client_id: str, brief_text: str) -> None:
    try:
        conn = psycopg2.connect(_get_db_conn_string())
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS client_briefs (
              client_id text NOT NULL,
              client_brief text NOT NULL,
              created_at timestamptz DEFAULT now()
            )
            """
        )
        cur.execute(
            "INSERT INTO client_briefs (client_id, client_brief) VALUES (%s, %s)",
            (client_id, brief_text)
        )
        conn.commit()
        cur.close(); conn.close()
        print("✅ Saved brief to Supabase table: client_briefs")
    except Exception as e:
        print(f"❌ Failed to save brief to Supabase DB: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate comprehensive client brief using Supabase'
    )
    parser.add_argument('--client-id', required=True, help='Client ID')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--drive-folder-id', help='Google Drive folder ID for upload')
    parser.add_argument('--credentials', default='./service_account.json',
                       help='Service account credentials')
    
    args = parser.parse_args()
    
    # Generate brief
    generator = SupabaseClientBriefGenerator(
        client_id=args.client_id,
        drive_folder_id=args.drive_folder_id,
        credentials_file=args.credentials
    )
    
    brief = generator.generate_client_brief()
    
    # Save brief
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = Path(f"{args.client_id}_brief_{timestamp}.md")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(brief, encoding='utf-8')
    
    print(f"\n💾 Brief saved to: {output_path}")
    print(f"📏 Size: {len(brief)} characters\n")
    
    # Upload to Drive if requested
    drive_folder_id = args.drive_folder_id
    if not drive_folder_id:
        drive_folder_id = resolve_drive_folder_id_from_db(args.client_id)
    if drive_folder_id:
        print("📤 Uploading to Google Drive...")
        file_id = generator.upload_brief_to_drive(str(output_path), drive_folder_id)
        if file_id:
            folder_url = f"https://drive.google.com/drive/folders/{drive_folder_id}"
            print(f"✅ Uploaded successfully to folder: {folder_url}")
    else:
        print("⚠️  Drive folder ID not provided and could not resolve from DB; skipping Drive upload.")
    
    # Save to Supabase DB (client_briefs)
    save_brief_to_supabase_db(args.client_id, brief)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
