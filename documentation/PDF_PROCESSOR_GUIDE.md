# PDF Processor Options Guide

## Overview

The client ingestion pipeline now supports three PDF processing methods:

1. **GPT-4o** (gpt) - AI-powered with image analysis
2. **MarkItDown** (markitdown) - Microsoft's LLM-optimized converter [NEW ⭐]
3. **pdfplumber** (pdfplumber) - Basic text extraction fallback

## Quick Comparison

| Feature | GPT-4o | MarkItDown | pdfplumber |
|---------|--------|------------|------------|
| **Speed** | Slow ⏱️ | Fast ⚡ | Fast ⚡ |
| **Cost** | $$$ (API calls) | Free ✅ | Free ✅ |
| **Structure Preservation** | Excellent ⭐⭐⭐ | Excellent ⭐⭐⭐ | Poor ⭐ |
| **Image Analysis** | Yes 📸 | No | No |
| **LLM Optimization** | Yes 🤖 | Yes 🤖 | No |
| **Tables** | Excellent | Good | Basic |
| **Headers/Lists** | Excellent | Excellent | None |
| **Requires** | OpenAI API Key | `pip install markitdown[pdf]` | `pip install pdfplumber` |

## When to Use Each

### MarkItDown (Recommended Default) ⭐

**Use when:**
- You want fast, high-quality extraction
- Structure matters (headings, lists, tables)
- LLM consumption is the goal
- You don't need image/diagram analysis
- Cost is a concern

**Pros:**
- Free and fast
- Excellent structure preservation
- Optimized for LLM consumption
- No API keys needed
- Handles most common PDF types well

**Cons:**
- Can't analyze images/diagrams
- May struggle with complex layouts

### GPT-4o

**Use when:**
- PDFs contain important images/diagrams
- Pitch decks with visual content
- Complex layouts requiring AI understanding
- Budget allows for API costs
- Maximum accuracy is critical

**Pros:**
- Analyzes images and diagrams
- Understands context
- Best for visual-heavy documents

**Cons:**
- Expensive (API costs)
- Slower processing
- Requires OpenAI API key

### pdfplumber (Fallback)

**Use when:**
- Simple text-only PDFs
- As automatic fallback if others fail
- No special structure needed

**Pros:**
- Simple and reliable
- No dependencies issues

**Cons:**
- No structure preservation
- Plain text only
- No markdown formatting

## Usage Examples

### Command Line

#### With new_client_ingestion.py

```bash
# Interactive mode - you'll be prompted to select
python new_client_ingestion.py

# Batch mode with MarkItDown (recommended)
python new_client_ingestion.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com" \
    --pdf-processor markitdown

# Batch mode with GPT-4o
python new_client_ingestion.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com" \
    --pdf-processor gpt

# Batch mode with pdfplumber
python new_client_ingestion.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com" \
    --pdf-processor pdfplumber
```

#### Standalone Drive Ingestion

```bash
# Use MarkItDown for PDFs
python ingestion/ingest_specific_drive_folder.py \
    --folder-id "1ABC..." \
    --pdf-processor markitdown

# Use GPT-4o for PDFs
python ingestion/ingest_specific_drive_folder.py \
    --folder-id "1ABC..." \
    --pdf-processor gpt

# Use pdfplumber for PDFs
python ingestion/ingest_specific_drive_folder.py \
    --folder-id "1ABC..." \
    --pdf-processor pdfplumber
```

### Interactive Mode

When running `new_client_ingestion.py` interactively, you'll see:

```
📄 PDF Processing Options:
   1. gpt - GPT-4o with image analysis (most accurate, requires OpenAI API)
   2. markitdown - Microsoft MarkItDown (fast, preserves structure, LLM-optimized)
   3. pdfplumber - Basic text extraction (fallback option)
Select PDF processor [1/2/3, default: 2-markitdown]:
```

Simply press Enter to use MarkItDown (recommended), or type 1 or 3 for other options.

## Output Comparison

### MarkItDown Output
```markdown
## Executive Summary

The proposed solution includes:

1. **AI Integration**
   - Advanced NLP capabilities
   - Real-time processing

2. **Data Analytics**
   - Custom dashboards
   - Automated reporting

| Feature | Status |
|---------|--------|
| API     | ✓      |
| UI      | In Progress |
```

### pdfplumber Output
```
Executive Summary
The proposed solution includes:
AI Integration
Advanced NLP capabilities
Real-time processing
Data Analytics
Custom dashboards
Automated reporting
Feature Status
API ✓
UI In Progress
```

Notice how MarkItDown preserves:
- Headers (`##`)
- Lists (numbered and bulleted)
- Bold formatting (`**`)
- Table structure

## Installation

### MarkItDown (Recommended)
```bash
pip install 'markitdown[pdf]'
```

Already installed in your environment! ✅

### GPT-4o
```bash
# Requires OpenAI Python library (already installed)
# Set your API key:
export OPENAI_API_KEY="sk-..."
```

### pdfplumber
```bash
pip install pdfplumber
```

Already installed! ✅

## Testing the Helper Script

Test MarkItDown processing on a single PDF:

```bash
# Basic test
python ingestion/pdf_process_markitdown.py path/to/document.pdf

# Compare MarkItDown vs pdfplumber
python ingestion/pdf_process_markitdown.py path/to/document.pdf --compare
```

## Migration Guide

### From Existing Setup

If you've been using GPT-4o processing:

**Old workflow:**
```bash
python new_client_ingestion.py \
    --client-id "client" \
    --drive-folder-id "1ABC..."
# (defaults to GPT-4o)
```

**New workflow with MarkItDown:**
```bash
python new_client_ingestion.py \
    --client-id "client" \
    --drive-folder-id "1ABC..." \
    --pdf-processor markitdown
```

**Benefits:**
- Faster processing (no API calls)
- No OpenAI costs
- Still maintains excellent structure
- Better for RAG pipelines

## Troubleshooting

### "MarkItDown is not installed"
```bash
pip install 'markitdown[pdf]'
```

### "No module named 'pdf_process_markitdown'"
Make sure you're running from the project root:
```bash
cd /Users/hynes/dev/vectara
python new_client_ingestion.py
```

### MarkItDown returns empty content
Some PDFs may not work well with MarkItDown. The system will automatically fall back to pdfplumber. You can also manually specify:
```bash
--pdf-processor pdfplumber
```

### Want to reprocess existing clients
To reprocess PDFs with a different processor:
```bash
# Re-run drive ingestion with new processor
python ingestion/ingest_specific_drive_folder.py \
    --folder-id "CLIENT_DRIVE_FOLDER_ID" \
    --output-dir "ingestion/client_ingestion_outputs/CLIENT_ID" \
    --pdf-processor markitdown
```

## Performance Benchmarks

Based on a typical 20-page client deck:

| Processor | Time | Cost | Structure Quality |
|-----------|------|------|-------------------|
| GPT-4o | ~2-3 min | ~$0.50-1.00 | Excellent ⭐⭐⭐ |
| MarkItDown | ~5-10 sec | $0 | Excellent ⭐⭐⭐ |
| pdfplumber | ~5-10 sec | $0 | Poor ⭐ |

## Recommendations

### For Most Clients
**Use MarkItDown** - It's the sweet spot of speed, quality, and cost.

### For Visual-Heavy Content
**Use GPT-4o** - When pitch decks have important diagrams, charts, or infographics that need AI interpretation.

### As Automatic Fallback
**pdfplumber** - The system will automatically use this if MarkItDown fails.

## Source Code

- **MarkItDown Helper**: `ingestion/pdf_process_markitdown.py`
- **GPT-4o Processing**: `ingestion/pdf_process_gpt.py`
- **Main Ingestion**: `ingestion/ingest_specific_drive_folder.py`
- **Client Onboarding**: `new_client_ingestion.py`

## Learn More

- [Microsoft MarkItDown GitHub](https://github.com/microsoft/markitdown)
- [MarkItDown Documentation](https://github.com/microsoft/markitdown#readme)
- Project location: `/Users/hynes/dev/markitdown`

