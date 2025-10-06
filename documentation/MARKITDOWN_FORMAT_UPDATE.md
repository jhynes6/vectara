# MarkItDown Format Update - Matching GPT Output Structure

## Summary

Updated the MarkItDown PDF processor to output the same standardized format as the GPT-4o processor, with consistent `## Extracted Text` and `## LLM Analysis` sections.

## What Changed

### Before (Simple Format)
```markdown
# Document Title

Main content...
Tables...
Lists...
```

### After (Standardized Format)
```markdown
## Extracted Text

# Document Title

Main content...
Tables...
Lists...

## LLM Analysis

*Content processed with Microsoft MarkItDown - structure-preserving markdown 
conversion optimized for LLM consumption. MarkItDown automatically maintains 
document hierarchy, tables, and formatting.*
```

## Updated Functions

### 1. `process_pdf_with_markitdown()`

**New Return Values:**
```python
{
    'success': bool,
    'markdown_content': str,      # Now includes ## sections
    'extracted_text': str,        # Raw markdown (NEW)
    'pages_description': list,    # Empty for MarkItDown (NEW - compatibility)
    'pages_processed': int,
    'pages_analyzed': int,        # NEW - compatibility
    'error': str or None,
    'processing_method': 'markitdown'
}
```

**New Parameters:**
- `include_extracted_text`: Controls whether to include the "## Extracted Text" section

### 2. `process_pdf_batch_markitdown()`

**Updated to format output like GPT processor:**
```python
# Format content to match GPT processor output structure
formatted_content = []

# Section 1: Extracted Text
formatted_content.append("## Extracted Text\n")
formatted_content.append(cleaned_text)

# Section 2: LLM Analysis (note)
formatted_content.append("\n\n## LLM Analysis\n")
formatted_content.append("*Content processed with Microsoft MarkItDown...*\n")

results[file_id] = ''.join(formatted_content)
```

## Output Format Examples

### GPT-4o Processor
```markdown
## Extracted Text

[pdfminer raw text extraction]

Product Overview
Features and Benefits
Pricing Information

## LLM Page Analysis

### Page 2

The page displays a product comparison table showing three tiers: Basic, 
Professional, and Enterprise. Each tier is represented with pricing and features...

---

### Page 3

This page contains customer testimonials with photos and quotes from five clients...

---
```

### MarkItDown Processor (NEW)
```markdown
## Extracted Text

# Product Overview

## Features and Benefits

- **Feature 1** - Advanced analytics
- **Feature 2** - Real-time processing
- **Feature 3** - Custom integrations

## Pricing Information

| Tier | Price | Features |
|------|-------|----------|
| Basic | $99/mo | 5 users |
| Pro | $299/mo | 25 users |
| Enterprise | Custom | Unlimited |

## LLM Analysis

*Content processed with Microsoft MarkItDown - structure-preserving markdown 
conversion optimized for LLM consumption. MarkItDown automatically maintains 
document hierarchy, tables, and formatting.*
```

### pdfplumber Processor
```markdown
## Extracted Text

Product Overview
Features and Benefits
Feature 1 Advanced analytics
Feature 2 Real-time processing
Pricing Information
Tier Price Features
Basic $99/mo 5 users
Pro $299/mo 25 users

## LLM Analysis

*Content processed with pdfplumber - basic text extraction.*
```

## Integration with ingest_specific_drive_folder.py

The standardized format is processed uniformly:

```python
# All processors now return data in the same format
if result['success']:
    combined_content = []
    
    # Section 1: Extracted Text
    if result['extracted_text'].strip():
        combined_content.append("## Extracted Text\n")
        cleaned_text = result['extracted_text'].replace('\f', '\n\n---\n\n')
        combined_content.append(cleaned_text)
    
    # Section 2: LLM Analysis (varies by processor)
    if result['pages_description']:  # GPT-4o has page descriptions
        combined_content.append("\n\n## LLM Page Analysis\n")
        for i, description in enumerate(result['pages_description'], 1):
            combined_content.append(f"\n### Page {i + 1}\n")
            combined_content.append(description)
            combined_content.append("\n---\n")
    
    extracted_content[file_id] = '\n'.join(combined_content)
```

## Benefits

### 1. Consistency
All PDFs have the same section structure regardless of processor:
- `## Extracted Text` - Always present
- `## LLM Analysis` - Always present (even if minimal)

### 2. Compatibility
Easy to switch between processors without breaking downstream code:
```bash
# Switch from GPT to MarkItDown - output format stays the same
--pdf-processor gpt      # Detailed page analysis
--pdf-processor markitdown  # Structure-preserving extraction
--pdf-processor pdfplumber  # Basic text
```

### 3. Searchability
Both sections are searchable in Vectara:
- Extracted text = main content
- LLM analysis = additional context

### 4. Debugging
Easy to identify which processor was used and what content came from where.

## When to Use Each Processor

### MarkItDown (Recommended) ⭐
**Best for**: Most documents
**Output**: 
- Rich structured markdown in "Extracted Text"
- Processing note in "LLM Analysis"

### GPT-4o
**Best for**: Visual-heavy documents
**Output**:
- Raw text in "Extracted Text"
- Detailed image/diagram descriptions in "LLM Analysis"

### pdfplumber
**Best for**: Fallback/simple docs
**Output**:
- Plain text in "Extracted Text"
- Simple processing note in "LLM Analysis"

## Testing the New Format

### Test Single PDF
```bash
cd /Users/hynes/dev/vectara

# Test MarkItDown format
python ingestion/pdf_process_markitdown.py path/to/test.pdf

# Should output with ## Extracted Text and ## LLM Analysis sections
```

### Test in Full Workflow
```bash
# Process a client with MarkItDown
python run_complete_workflow.py \
    --client-id "test-client" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://test.com" \
    --pdf-processor markitdown

# Check output format
cat ingestion/client_ingestion_outputs/test-client/client_materials/*.md
```

## Backward Compatibility

### Existing PDFs
- Already processed PDFs keep their format
- No automatic reprocessing
- Can reprocess if desired with new format

### To Reprocess
```bash
# Reprocess with new MarkItDown format
python ingestion/ingest_specific_drive_folder.py \
    --folder-id "CLIENT_DRIVE_FOLDER" \
    --output-dir "ingestion/client_ingestion_outputs/CLIENT_ID" \
    --pdf-processor markitdown
```

## Code Changes Summary

### File: `ingestion/pdf_process_markitdown.py`

**Changes:**
1. Added `extracted_text` to return dict
2. Added `pages_description` (empty list) for compatibility
3. Added `pages_analyzed` for compatibility
4. Format output with `## Extracted Text` and `## LLM Analysis` sections
5. `process_pdf_batch_markitdown()` now formats content consistently

**Lines Changed**: ~50 lines updated

**Backward Compatible**: ✅ Yes (new parameter is optional)

## Verification

After processing, check that PDFs have this structure:

```bash
# Check a processed PDF
cat ingestion/client_ingestion_outputs/CLIENT/client_materials/some-doc.md

# Should see:
# ## Extracted Text
# [content]
# ## LLM Analysis
# [note]
```

## Summary

✅ **MarkItDown processor updated**  
✅ **Same format as GPT processor**  
✅ **Standardized sections: `## Extracted Text` + `## LLM Analysis`**  
✅ **Backward compatible**  
✅ **Drop-in replacement ready**  

All PDF processors now produce consistent, well-structured output! 🎉

