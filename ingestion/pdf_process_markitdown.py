#!/usr/bin/env python3
"""
PDF Processing with MarkItDown

This script provides an alternative to GPT-4o/pdfplumber processing using
Microsoft's MarkItDown library for converting PDFs to markdown.

MarkItDown is optimized for LLM consumption and preserves document structure
(headings, lists, tables, links) in a way that's ideal for RAG pipelines.

Usage:
    from pdf_process_markitdown import process_pdf_with_markitdown
    
    result = process_pdf_with_markitdown("document.pdf")
    if result['success']:
        print(result['markdown_content'])
"""

import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def process_pdf_with_markitdown(pdf_path: str, include_extracted_text: bool = True) -> Dict[str, Any]:
    """
    Process a PDF file using MarkItDown to extract content as markdown
    
    Args:
        pdf_path: Path to the PDF file to process
        include_extracted_text: Whether to extract raw text separately (for compatibility with GPT format)
        
    Returns:
        Dictionary containing:
            - success (bool): Whether processing succeeded
            - markdown_content (str): Extracted markdown content (formatted like GPT output)
            - extracted_text (str): Raw text extraction (for compatibility)
            - pages_description (list): Empty list (for compatibility with GPT format)
            - pages_processed (int): Number of pages in the PDF (if available)
            - pages_analyzed (int): Same as pages_processed
            - error (str): Error message if processing failed
            - processing_method (str): "markitdown"
    """
    try:
        from markitdown import MarkItDown
        
        logger.info(f"Processing PDF with MarkItDown: {pdf_path}")
        
        # Initialize MarkItDown
        md = MarkItDown()
        
        # Convert the PDF
        result = md.convert(pdf_path)
        
        # Extract the markdown content
        raw_markdown = result.text_content
        
        if not raw_markdown or not raw_markdown.strip():
            logger.warning(f"MarkItDown returned empty content for {pdf_path}")
            return {
                'success': False,
                'markdown_content': '',
                'extracted_text': '',
                'pages_description': [],
                'pages_processed': 0,
                'pages_analyzed': 0,
                'error': 'MarkItDown returned empty content',
                'processing_method': 'markitdown'
            }
        
        # Try to estimate page count from content
        pages_processed = raw_markdown.count('\n\n---\n\n') + 1
        
        # Format output to match GPT processor structure
        # GPT format has: "## Extracted Text" and "## LLM Page Analysis"
        # MarkItDown format will have: "## Extracted Text" and "## MarkItDown Analysis"
        
        formatted_content = []
        
        # Section 1: Extracted Text (raw markdown from MarkItDown)
        if include_extracted_text:
            formatted_content.append("## Extracted Text\n")
            formatted_content.append(raw_markdown)
        
        # Section 2: LLM Analysis (MarkItDown provides this directly, so we note it)
        formatted_content.append("\n\n## MarkItDown Analysis\n")
        formatted_content.append("*Content above was processed with Microsoft MarkItDown, which preserves document structure ")
        formatted_content.append("(headings, lists, tables) optimized for LLM consumption.*\n")
        
        final_content = ''.join(formatted_content)
        
        logger.info(f"✅ MarkItDown processing successful: {pdf_path}")
        logger.info(f"   - Content length: {len(raw_markdown)} characters")
        logger.info(f"   - Estimated sections: {pages_processed}")
        
        return {
            'success': True,
            'markdown_content': final_content,
            'extracted_text': raw_markdown,  # For compatibility with GPT format
            'pages_description': [],  # Empty for MarkItDown (no page-by-page analysis)
            'pages_processed': pages_processed,
            'pages_analyzed': pages_processed,
            'error': None,
            'processing_method': 'markitdown'
        }
        
    except ImportError:
        error_msg = "MarkItDown is not installed. Install with: pip install 'markitdown[pdf]'"
        logger.error(f"❌ {error_msg}")
        return {
            'success': False,
            'markdown_content': '',
            'extracted_text': '',
            'pages_description': [],
            'pages_processed': 0,
            'pages_analyzed': 0,
            'error': error_msg,
            'processing_method': 'markitdown'
        }
    except Exception as e:
        error_msg = f"Error processing PDF with MarkItDown: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return {
            'success': False,
            'markdown_content': '',
            'extracted_text': '',
            'pages_description': [],
            'pages_processed': 0,
            'pages_analyzed': 0,
            'error': error_msg,
            'processing_method': 'markitdown'
        }


def process_pdf_batch_markitdown(pdf_files: list) -> tuple[Dict[str, str], list[Dict]]:
    """
    Process multiple PDF files with MarkItDown
    
    Args:
        pdf_files: List of tuples (file_info, temp_path) where file_info is a dict
                   containing file metadata and temp_path is the path to the PDF
        
    Returns:
        Tuple of (results_dict, failed_files_list) where:
        - results_dict: Dictionary mapping file_id to formatted markdown content string
        - failed_files_list: List of failed file info dictionaries for error reporting
    """
    logger.info(f"🚀 Starting batch PDF processing with MarkItDown for {len(pdf_files)} files")
    
    results = {}
    failed_files = []
    successful = 0
    failed = 0
    
    for file_info, temp_path in pdf_files:
        file_id = file_info['id']
        file_name = file_info['name']
        
        logger.info(f"📄 Processing: {file_name}")
        
        try:
            result = process_pdf_with_markitdown(temp_path, include_extracted_text=True)
            
            if result['success']:
                # Format content to match GPT processor output structure
                # The content should have "## Extracted Text" and "## LLM Analysis" sections
                formatted_content = []
                
                # Add extracted text section
                if result['extracted_text'].strip():
                    formatted_content.append("## Extracted Text\n")
                    # Clean up any form feeds
                    cleaned_text = result['extracted_text'].replace('\f', '\n\n---\n\n')
                    formatted_content.append(cleaned_text)
                
                # Add MarkItDown analysis note
                formatted_content.append("\n\n## LLM Analysis\n")
                formatted_content.append("*Content processed with Microsoft MarkItDown - ")
                formatted_content.append("structure-preserving markdown conversion optimized for LLM consumption. ")
                formatted_content.append("MarkItDown automatically maintains document hierarchy, tables, and formatting.*\n")
                
                # Store the formatted content (matching GPT processor output format)
                results[file_id] = ''.join(formatted_content)
                successful += 1
                logger.info(f"✅ Successfully processed: {file_name} ({result['pages_analyzed']} pages)")
            else:
                logger.error(f"❌ Failed to process: {file_name} - {result['error']}")
                failed += 1
                # Add to failed files list for error reporting
                failed_files.append({
                    'name': file_name,
                    'id': file_id,
                    'mime_type': file_info.get('mimeType', 'unknown'),
                    'size': file_info.get('size', 'N/A'),
                    'url': f"https://drive.google.com/file/d/{file_id}/view",
                    'error': result['error'],
                    'error_type': 'MarkItDownProcessingError',
                    'file_category': 'client_materials',
                    'timestamp': __import__('datetime').datetime.now().isoformat()
                })
                
        except Exception as e:
            logger.error(f"❌ Exception processing {file_name}: {str(e)}")
            failed += 1
            # Add to failed files list for error reporting
            failed_files.append({
                'name': file_name,
                'id': file_id,
                'mime_type': file_info.get('mimeType', 'unknown'),
                'size': file_info.get('size', 'N/A'),
                'url': f"https://drive.google.com/file/d/{file_id}/view",
                'error': str(e),
                'error_type': type(e).__name__,
                'file_category': 'client_materials',
                'timestamp': __import__('datetime').datetime.now().isoformat()
            })
    
    logger.info(f"🎉 MarkItDown batch processing complete:")
    logger.info(f"   ✅ Successful: {successful}/{len(pdf_files)}")
    logger.info(f"   ❌ Failed: {failed}/{len(pdf_files)}")
    
    return results, failed_files


def compare_with_pdfplumber(pdf_path: str) -> Dict[str, Any]:
    """
    Compare MarkItDown output with pdfplumber for a given PDF
    Useful for testing and validation
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Dictionary with comparison results
    """
    import pdfplumber
    from io import BytesIO
    
    logger.info(f"📊 Comparing MarkItDown vs pdfplumber for: {pdf_path}")
    
    # Process with MarkItDown
    markitdown_result = process_pdf_with_markitdown(pdf_path)
    
    # Process with pdfplumber
    pdfplumber_text = []
    try:
        with open(pdf_path, 'rb') as f:
            with pdfplumber.open(BytesIO(f.read())) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pdfplumber_text.append(text)
        
        pdfplumber_content = '\n\n'.join(pdfplumber_text)
        pdfplumber_success = True
    except Exception as e:
        pdfplumber_content = ""
        pdfplumber_success = False
        logger.error(f"pdfplumber failed: {e}")
    
    # Compare results
    comparison = {
        'pdf_path': pdf_path,
        'markitdown': {
            'success': markitdown_result['success'],
            'length': len(markitdown_result['markdown_content']),
            'has_structure': '##' in markitdown_result['markdown_content'] or '**' in markitdown_result['markdown_content']
        },
        'pdfplumber': {
            'success': pdfplumber_success,
            'length': len(pdfplumber_content),
            'has_structure': False  # pdfplumber returns plain text
        }
    }
    
    logger.info(f"📊 Comparison results:")
    logger.info(f"   MarkItDown: {comparison['markitdown']}")
    logger.info(f"   pdfplumber: {comparison['pdfplumber']}")
    
    return comparison


if __name__ == "__main__":
    """Test the MarkItDown processor"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_process_markitdown.py <path-to-pdf>")
        print("       python pdf_process_markitdown.py <path-to-pdf> --compare")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    compare_mode = '--compare' in sys.argv
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if compare_mode:
        # Compare mode
        result = compare_with_pdfplumber(pdf_path)
        print("\n" + "="*80)
        print("COMPARISON RESULTS")
        print("="*80)
        print(f"MarkItDown Success: {result['markitdown']['success']}")
        print(f"MarkItDown Length: {result['markitdown']['length']} chars")
        print(f"MarkItDown Has Structure: {result['markitdown']['has_structure']}")
        print(f"\npdfplumber Success: {result['pdfplumber']['success']}")
        print(f"pdfplumber Length: {result['pdfplumber']['length']} chars")
        print("="*80)
    else:
        # Regular processing mode
        result = process_pdf_with_markitdown(pdf_path)
        
        if result['success']:
            print("\n" + "="*80)
            print("PDF PROCESSING SUCCESSFUL")
            print("="*80)
            print(f"Pages: {result['pages_processed']}")
            print(f"Content length: {len(result['markdown_content'])} characters")
            print(f"\nFirst 500 characters:")
            print("-"*80)
            print(result['markdown_content'][:500])
            print("="*80)
        else:
            print(f"\n❌ Processing failed: {result['error']}")
            sys.exit(1)

