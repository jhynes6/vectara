# PDF Processor Quick Reference

## TL;DR

**MarkItDown** = Fast, free, preserves structure (headers, tables, lists) - **USE THIS**  
**GPT-4o** = Slow, costly, but describes images/diagrams - use for pitch decks  
**pdfplumber** = Basic fallback - plain text only

## What Each Processor Does

```
┌─────────────────────────────────────────────────────────────┐
│                    GPT-4o Processor                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input: PDF File                                            │
│    ↓                                                        │
│  Step 1: Extract plain text (pdfminer)                     │
│    ↓                                                        │
│  Step 2: Convert each page to image (pdf2image)            │
│    ↓                                                        │
│  Step 3: Send images to GPT-4o Vision API                  │
│    ↓                                                        │
│  Step 4: Get AI descriptions of diagrams/charts/images     │
│    ↓                                                        │
│  Output:                                                    │
│  ┌─────────────────────────────────────────────┐          │
│  │ ## Extracted Text                           │          │
│  │ Plain text without structure                │          │
│  │                                              │          │
│  │ ## LLM Page Analysis                        │          │
│  │ ### Page 2                                  │          │
│  │ The chart shows... [AI description]         │          │
│  │ ### Page 3                                  │          │
│  │ The diagram displays... [AI description]    │          │
│  └─────────────────────────────────────────────┘          │
│                                                             │
│  ⏱️  Time: 2-3 minutes                                     │
│  💰 Cost: $0.50-1.00 per doc                               │
│  👁️  Sees: Text + Images/Diagrams                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  MarkItDown Processor ⭐                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input: PDF File                                            │
│    ↓                                                        │
│  Step 1: Smart extraction with structure (MarkItDown)      │
│    ↓                                                        │
│  Output:                                                    │
│  ┌─────────────────────────────────────────────┐          │
│  │ ## Extracted Text                           │          │
│  │                                              │          │
│  │ # Document Title                            │          │
│  │                                              │          │
│  │ ## Section 1                                │          │
│  │ Structured content...                       │          │
│  │                                              │          │
│  │ - Bullet list item 1                        │          │
│  │ - Bullet list item 2                        │          │
│  │                                              │          │
│  │ | Table | Data |                            │          │
│  │ |-------|------|                            │          │
│  │ | Row 1 | Val1 |                            │          │
│  │                                              │          │
│  │ ## LLM Analysis                             │          │
│  │ *Processed with MarkItDown...*              │          │
│  └─────────────────────────────────────────────┘          │
│                                                             │
│  ⏱️  Time: 5-10 seconds                                    │
│  💰 Cost: $0.00                                            │
│  📝 Sees: Text with structure (no images)                  │
└─────────────────────────────────────────────────────────────┘
```

## What's in the Output

### Both Processors Create:
- ✅ `## Extracted Text` section
- ✅ `## LLM Analysis` section

### GPT-4o Special Features:
- 👁️ **Image descriptions** in LLM Analysis
- 📊 **Chart interpretations**
- 🎨 **Diagram explanations**
- 📸 **Visual context**

### MarkItDown Special Features:
- 📋 **Structured headers** (`#`, `##`, `###`)
- 📊 **Formatted tables** (markdown tables)
- • **Proper lists** (bullets and numbered)
- **Bold/italic** formatting
- 🔗 **Preserved links**

## Decision Tree

```
Does your PDF have important diagrams/charts/images?
│
├─ YES → Use GPT-4o
│         (you need the visual descriptions)
│
└─ NO → Use MarkItDown ⭐
        (faster, free, better structure)
```

## Command Reference

```bash
# Use MarkItDown (default, recommended)
python run_complete_workflow.py \
    --client-id "client" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com"
    # (markitdown is default)

# Use GPT-4o (for visual content)
python run_complete_workflow.py \
    --client-id "client" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com" \
    --pdf-processor gpt

# Use pdfplumber (fallback)
python run_complete_workflow.py \
    --client-id "client" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com" \
    --pdf-processor pdfplumber
```

## Example Use Cases

### ✅ Use MarkItDown For:
- Capability overview decks (mostly text)
- Service descriptions
- Text-based case studies
- Proposals and contracts
- Technical documentation
- Reports with tables

### ✅ Use GPT-4o For:
- Marketing pitch decks (lots of visuals)
- Infographic-heavy presentations
- Process flow diagrams
- Before/after comparisons
- Data visualization reports
- Architectural diagrams

---

**Default to MarkItDown. Use GPT-4o only when visuals matter.** 🎯


