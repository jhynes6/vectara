#!/usr/bin/env python3
"""
Client Brief Generator - Comprehensive Client Analysis

This script combines outputs from all three summarizer scripts to generate
a comprehensive client brief with case studies, intake form analysis, and website content.

Usage:
    python client_brief_generator.py --generate-brief --corpus-key "corpus_key"
    python client_brief_generator.py --generate-brief --corpus-key "corpus_key" --output brief.md
    python client_brief_generator.py --help  # Show all options
"""

import argparse
import asyncio
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add the summarizers directory to the Python path
summarizers_path = Path(__file__).parent / "summarizers"
sys.path.insert(0, str(summarizers_path))

try:
    from case_study_summarizer import CaseStudySummarizer, list_workspace_agents, list_workspace_corpora
    from client_intake_summarizer import ClientIntakeSummarizer
    from website_summarizer import WebsiteSummarizer
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error importing summarizer modules: {e}")
    print("Please ensure all summarizer scripts are in the summarizers/ folder.")
    sys.exit(1)

# Load environment variables
load_dotenv(override=True)


class ClientBriefGenerator:
    """Generator for comprehensive client briefs combining all analysis types"""
    
    def __init__(self, api_key: str = None, corpus_key: str = None, agent_id: str = None):
        """
        Initialize the Client Brief Generator
        
        Args:
            api_key: Vectara API key (defaults to VECTARA_API_KEY env var)
            corpus_key: Vectara corpus key (defaults to VECTARA_CORPUS_KEY env var)
            agent_id: Optional agent ID for workspace agents
        """
        self.api_key = api_key or os.environ.get('VECTARA_API_KEY')
        self.corpus_key = corpus_key or os.environ.get('VECTARA_CORPUS_KEY')
        self.agent_id = agent_id
        
        if not self.api_key:
            raise ValueError(
                "Missing Vectara API key. Please set VECTARA_API_KEY environment variable or pass as argument."
            )
        
        if not self.corpus_key:
            raise ValueError(
                "Missing Vectara corpus key. Please set VECTARA_CORPUS_KEY environment variable or pass --corpus-key argument."
            )
        
        # Initialize all three summarizers
        print("🔄 Initializing summarizer components...")
        self.case_study_summarizer = CaseStudySummarizer(
            api_key=self.api_key,
            corpus_key=self.corpus_key,
            agent_id=self.agent_id
        )
        
        self.client_intake_summarizer = ClientIntakeSummarizer(
            api_key=self.api_key,
            corpus_key=self.corpus_key,
            agent_id=self.agent_id
        )
        
        self.website_summarizer = WebsiteSummarizer(
            api_key=self.api_key,
            corpus_key=self.corpus_key,
            agent_id=self.agent_id
        )
        print("✅ All summarizer components initialized successfully")
    
    def discover_case_study_documents(self) -> List[str]:
        """
        Discover all documents in the corpus with content_type = 'case_studies'
        
        Returns:
            List of document IDs with case studies content type
        """
        print("🔍 Discovering case study documents in corpus...")
        
        try:
            import requests
            
            # Use Vectara API to list documents and filter by content_type
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Use the documents endpoint to list all documents
            url = f"https://api.vectara.io/v2/corpora/{self.corpus_key}/documents"
            
            documents = []
            page_key = None
            
            # Paginate through all documents
            while True:
                params = {"limit": 100}
                if page_key:
                    params["page_key"] = page_key
                
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                
                result = response.json()
                page_documents = result.get("documents", [])
                documents.extend(page_documents)
                
                # Check for next page
                metadata = result.get("metadata", {})
                page_key = metadata.get("page_key")
                
                if not page_key:
                    break
            
            # Filter for case study documents
            case_study_docs = []
            for doc in documents:
                doc_metadata = doc.get("metadata", {})
                content_type = doc_metadata.get("content_type", "")
                doc_id = doc.get("id", "")
                
                if content_type == "case_studies" and doc_id:
                    case_study_docs.append(doc_id)
            
            doc_list = sorted(case_study_docs)
            print(f"✅ Found {len(doc_list)} case study documents:")
            for i, doc_id in enumerate(doc_list, 1):
                print(f"   {i:2d}. {doc_id}")
            
            return doc_list
            
        except Exception as e:
            print(f"⚠️  Could not auto-discover case studies: {str(e)}")
            print("🔍 Using fallback method to search for case studies...")
            
            # Fallback: Use a simple query approach
            try:
                # Try to use one of our tools to search for case studies
                from vectara_agentic.tools import VectaraToolFactory
                from pydantic import BaseModel, Field
                
                class CaseStudyDiscoveryArgs(BaseModel):
                    content_type_filter: str = Field(default="case_studies")
                
                vec_factory = VectaraToolFactory(
                    vectara_corpus_key=self.corpus_key,
                    vectara_api_key=self.api_key
                )
                
                discovery_tool = vec_factory.create_rag_tool(
                    tool_name="discover_case_studies",
                    tool_description="Discover case study documents",
                    tool_args_schema=CaseStudyDiscoveryArgs,
                    tool_args_type={
                        "content_type_filter": {
                            "type": "doc", 
                            "is_list": False, 
                            "filter_name": "content_type"
                        }
                    },
                    summary_num_results=50,
                    lambda_val=0.1,
                    include_citations=True,
                )
                
                # This is a more complex approach - for now, return some common case study patterns
                print("📋 Using pattern-based discovery for case studies...")
                common_patterns = [
                    "clients_rapid-pos.md",
                    "clients_clutch.md", 
                    "case_study_1.md",
                    "case_study_2.md"
                ]
                
                print(f"🔍 Trying common case study patterns: {len(common_patterns)} documents")
                for i, doc_id in enumerate(common_patterns, 1):
                    print(f"   {i:2d}. {doc_id}")
                
                return common_patterns
                
            except Exception as fallback_error:
                print(f"⚠️  Fallback discovery also failed: {str(fallback_error)}")
                return []
    
    def generate_case_studies_section(self, doc_ids: List[str], custom_query: str = None) -> str:
        """
        Generate the case studies section of the client brief
        
        Args:
            doc_ids: List of document IDs to analyze
            custom_query: Optional custom query for case study analysis
            
        Returns:
            Formatted case studies section
        """
        print(f"\n📊 [1/3] GENERATING CASE STUDIES SECTION")
        print("=" * 80)
        
        case_studies_content = []
        
        for i, doc_id in enumerate(doc_ids, 1):
            print(f"\n📋 Analyzing case study {i}/{len(doc_ids)}: {doc_id}")
            print("-" * 60)
            
            try:
                summary = self.case_study_summarizer.generate_case_study_summary(
                    doc_id=doc_id,
                    custom_query=custom_query
                )
                case_studies_content.append({
                    "doc_id": doc_id,
                    "summary": summary
                })
                print(f"✅ Case study {i} analyzed successfully")
            except Exception as e:
                error_msg = f"❌ Error analyzing {doc_id}: {str(e)}"
                print(error_msg)
                case_studies_content.append({
                    "doc_id": doc_id,
                    "summary": error_msg
                })
        
        # Format the case studies section
        section = "# 📊 CASE STUDIES ANALYSIS\n\n"
        
        if len(doc_ids) == 1:
            section += f"**Document:** {doc_ids[0]}\n\n"
            section += case_studies_content[0]["summary"]
        else:
            section += f"**Total Case Studies Analyzed:** {len(doc_ids)}\n\n"
            for i, study in enumerate(case_studies_content, 1):
                section += f"## Case Study {i}: {study['doc_id']}\n\n"
                section += study["summary"]
                section += "\n\n---\n\n"
        
        return section
    
    def generate_client_intake_section(self, custom_query: str = None) -> str:
        """
        Generate the client intake form section of the client brief
        
        Args:
            custom_query: Optional custom query for intake analysis
            
        Returns:
            Formatted client intake section
        """
        print(f"\n📋 [2/3] GENERATING CLIENT INTAKE FORM SECTION")
        print("=" * 80)
        
        try:
            summary = self.client_intake_summarizer.generate_client_intake_summary(
                custom_query=custom_query
            )
            print("✅ Client intake form analyzed successfully")
            
            section = "# 📋 CLIENT INTAKE FORM ANALYSIS\n\n"
            section += f"**Filter:** doc.source = 'client_intake_form'\n\n"
            section += summary
            
            return section
        except Exception as e:
            error_msg = f"❌ Error analyzing client intake form: {str(e)}"
            print(error_msg)
            return f"# 📋 CLIENT INTAKE FORM ANALYSIS\n\n{error_msg}\n\n"
    
    def generate_website_section(self, custom_query: str = None) -> str:
        """
        Generate the website analysis section of the client brief
        
        Args:
            custom_query: Optional custom query for website analysis
            
        Returns:
            Formatted website section
        """
        print(f"\n🌐 [3/3] GENERATING WEBSITE CONTENT SECTION")
        print("=" * 80)
        
        try:
            analysis = self.website_summarizer.generate_comprehensive_website_analysis(
                custom_query=custom_query
            )
            print("✅ Website content analyzed successfully")
            
            section = "# 🌐 WEBSITE CONTENT ANALYSIS\n\n"
            section += "**Method:** Sequential analysis of 5 content types\n"
            section += "**Content Types:** services_products, industry_markets, blogs_resources, testimonials, homepage\n\n"
            section += analysis
            
            return section
        except Exception as e:
            error_msg = f"❌ Error analyzing website content: {str(e)}"
            print(error_msg)
            return f"# 🌐 WEBSITE CONTENT ANALYSIS\n\n{error_msg}\n\n"
    
    def generate_client_brief(
        self, 
        case_study_query: str = None,
        intake_query: str = None, 
        website_query: str = None
    ) -> str:
        """
        Generate a comprehensive client brief by auto-discovering case studies and analyzing all content
        
        Args:
            case_study_query: Optional custom query for case studies
            intake_query: Optional custom query for client intake
            website_query: Optional custom query for website analysis
            
        Returns:
            Complete formatted client brief
        """
        print("🚀 STARTING COMPREHENSIVE CLIENT BRIEF GENERATION")
        print("=" * 80)
        
        # Auto-discover case study documents
        doc_ids = self.discover_case_study_documents()
        
        if not doc_ids:
            print("⚠️  No case study documents found. Brief will include intake and website analysis only.")
        
        print(f"📊 Case Studies: {len(doc_ids)} document(s) (auto-discovered)")
        print(f"📋 Client Intake: doc.source = 'client_intake_form'")  
        print(f"🌐 Website Content: 5 content types")
        print(f"🗓️  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Generate header
        brief = f"""# 📄 COMPREHENSIVE CLIENT BRIEF

**Generated:** {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
**Corpus:** {self.corpus_key}
**Analysis Components:** Case Studies ({len(doc_ids)}), Client Intake Forms, Website Content (5 types)

---

"""
        
        # Generate each section
        try:
            # Section 1: Case Studies (auto-discovered)
            if doc_ids:
                case_studies_section = self.generate_case_studies_section(
                    doc_ids=doc_ids,
                    custom_query=case_study_query
                )
                brief += case_studies_section + "\n\n---\n\n"
            else:
                brief += "# 📊 CASE STUDIES ANALYSIS\n\n**No case study documents found** with content_type = 'case_studies'\n\n---\n\n"
            
            # Section 2: Client Intake Forms
            intake_section = self.generate_client_intake_section(
                custom_query=intake_query
            )
            brief += intake_section + "\n\n---\n\n"
            
            # Section 3: Website Analysis
            website_section = self.generate_website_section(
                custom_query=website_query
            )
            brief += website_section + "\n\n"
            
            # Add footer
            brief += f"""---

# 📈 BRIEF GENERATION SUMMARY

- **Total Sections:** 3 (Case Studies, Client Intake, Website Analysis)
- **Case Studies Processed:** {len(doc_ids)}
- **Client Intake Forms:** Analyzed from doc.source = 'client_intake_form'
- **Website Content Types:** services_products, industry_markets, blogs_resources, testimonials, homepage
- **Generation Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Corpus:** {self.corpus_key}

*This brief provides a comprehensive analysis of the client across all available content types.*
"""
            
            print("\n" + "=" * 80)
            print("✅ CLIENT BRIEF GENERATION COMPLETED SUCCESSFULLY")
            print("=" * 80)
            
            return brief
            
        except Exception as e:
            error_section = f"""
# ❌ BRIEF GENERATION ERROR

**Error:** {str(e)}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please check your configuration and try again.
"""
            return brief + error_section


def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive client briefs combining case studies, intake forms, and website analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --generate-brief --corpus-key "dodeka-digital"                    # Generate brief (saves to ~/outputs/)
  %(prog)s --generate-brief --corpus-key "dodeka-digital" --output custom.md # Save to custom location
  %(prog)s --generate-brief --corpus-key "dodeka-digital" --verbose          # Show brief content and save
  %(prog)s --generate-brief --corpus-key "dodeka-digital" --website-query "Focus on services" # Custom queries
  %(prog)s --list-agents                                                     # List available agents
  %(prog)s --list-corpora                                                    # List available corpora

Default Output: /outputs/[corpus_key]_client_brief_[timestamp].md
        """
    )
    
    # Action arguments (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group(required=False)
    action_group.add_argument(
        "--list-agents",
        action="store_true",
        help="List all agents in the Vectara workspace"
    )
    action_group.add_argument(
        "--list-corpora", 
        action="store_true",
        help="List all corpora (document collections) in the Vectara workspace"
    )
    action_group.add_argument(
        "--generate-brief",
        action="store_true",
        help="Generate comprehensive client brief (auto-discovers all case studies with content_type='case_studies')"
    )
    
    # Configuration arguments
    parser.add_argument(
        "--corpus-key",
        help="Vectara corpus key (defaults to VECTARA_CORPUS_KEY env var)"
    )
    
    parser.add_argument(
        "--api-key",
        help="Vectara API key (defaults to VECTARA_API_KEY env var)"
    )
    
    parser.add_argument(
        "--agent-id",
        help="Specific agent ID to use for workspace agents (optional)"
    )
    
    # Query customization
    parser.add_argument(
        "--case-study-query",
        help="Custom query for case study analysis"
    )
    
    parser.add_argument(
        "--intake-query",
        help="Custom query for client intake form analysis"
    )
    
    parser.add_argument(
        "--website-query",
        help="Custom query for website content analysis"
    )
    
    # Output options
    parser.add_argument(
        "--output",
        help="Output file path (default: ~/outputs/[corpus_key]_client_brief_[timestamp].md)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output (also prints brief content to console)"
    )
    
    args = parser.parse_args()
    
    try:
        # Handle list agents request
        if args.list_agents:
            list_workspace_agents(args.api_key)
            return
        
        # Handle list corpora request
        if args.list_corpora:
            list_workspace_corpora(args.api_key)
            return
        
        # Check if we need to generate a brief
        if not args.generate_brief:
            print("❌ Error: Use --generate-brief to create a comprehensive client brief")
            parser.print_help()
            return
        
        # Validate corpus key
        if not args.corpus_key and not os.environ.get('VECTARA_CORPUS_KEY'):
            print("❌ Error: --corpus-key is required (or set VECTARA_CORPUS_KEY environment variable)")
            return
        
        # Initialize the client brief generator
        print("🔄 Initializing Client Brief Generator...")
        generator = ClientBriefGenerator(
            api_key=args.api_key,
            corpus_key=args.corpus_key,
            agent_id=args.agent_id
        )
        
        # Generate the comprehensive client brief (auto-discovers case studies)
        print("\n" + "🚀" + " GENERATING COMPREHENSIVE CLIENT BRIEF " + "🚀")
        print("=" * 80)
        
        brief = generator.generate_client_brief(
            case_study_query=args.case_study_query,
            intake_query=args.intake_query,
            website_query=args.website_query
        )
        
        # Generate default output filename if not provided
        if not args.output:
            # Create timestamp for filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            corpus_key = args.corpus_key or os.environ.get('VECTARA_CORPUS_KEY', 'unknown_corpus')
            filename = f"{corpus_key}_client_brief_{timestamp}.md"
            
            # Create outputs directory in user's home directory
            outputs_dir = Path(__file__).parent / "outputs"
            outputs_dir.mkdir(exist_ok=True)
            
            # Set default output path
            args.output = outputs_dir / filename
        
        # Save to file (now always happens)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(brief)
        print(f"\n💾 Client brief saved to: {args.output}")
        print(f"📄 File size: {len(brief)} characters")
        
        # Also print to console if verbose mode
        if args.verbose:
            print("\n" + "=" * 80)
            print("📄 COMPREHENSIVE CLIENT BRIEF")
            print("=" * 80)
            print(brief)
            print("=" * 80)
        
        # Show brief statistics
        print(f"\n🔍 Brief Statistics:")
        print(f"   - Case Studies: Auto-discovered from corpus")
        print(f"   - Total Characters: {len(brief)}")
        print(f"   - Corpus: {args.corpus_key or os.environ.get('VECTARA_CORPUS_KEY')}")
        print(f"   - Saved to: {args.output}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
