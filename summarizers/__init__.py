"""
Summarizers Package

This package contains specialized summarization scripts for different content types:
- case_study_summarizer.py: Analyzes case studies using doc.id filtering
- client_intake_summarizer.py: Processes client intake forms using doc.source filtering  
- website_summarizer.py: Comprehensive website analysis across 5 content types

Each script can be run independently from the project root:
    python summarizers/case_study_summarizer.py --list-agents
    python summarizers/client_intake_summarizer.py --summarize --corpus-key "corpus_key"
    python summarizers/website_summarizer.py --summarize --corpus-key "corpus_key"
"""
