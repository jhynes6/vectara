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

# Add path for imports
sys.path.insert(0, '/home/ubuntu/.local/lib/python3.13/site-packages')
from openai import OpenAI
from dotenv import load_dotenv

# Import Supabase vector store
from supabase_vector_store import SupabaseVectorStore

load_dotenv(override=True)


class SupabaseClientBriefGenerator:
    """Generator for comprehensive client briefs using Supabase RAG"""
    
    def __init__(self, client_id: str, drive_folder_id: str = None, 
                 credentials_file: str = "./service_account.json"):
        """
        Initialize the Client Brief Generator
        
        Args:
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
        
        print(f"✅ Initialized brief generator for client: {client_id}")
    
    def query_content_type(self, content_type: str, query: str, limit: int = 20) -> List[Dict]:
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
            similarity_threshold=0.6
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
        
        # Query case studies
        results = self.query_content_type(
            content_type="case_studies",
            query="case studies, success stories, client results, outcomes, projects",
            limit=10
        )
        
        if not results:
            return "## Case Studies\n\nNo case studies available.\n"
        
        # Prepare context
        context = "\n\n".join([
            f"**{r['title']}**\n{r['content'][:500]}..."
            for r in results[:5]
        ])
        
        # Generate summary
        prompt = f"""Based on these case studies and success stories, create a comprehensive summary:

{context}

Create a well-structured case studies section that highlights:
1. Key projects and their outcomes
2. Industries or sectors served
3. Measurable results and success metrics
4. Notable clients or partnerships

Format with clear headings and bullet points."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a business analyst creating comprehensive client briefs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return f"## Case Studies\n\n{response.choices[0].message.content}\n"
    
    def generate_client_intake_section(self) -> str:
        """Generate client intake form section"""
        print("📝 Generating client intake section...")
        
        results = self.query_content_type(
            content_type="client_intake_form",
            query="client information, intake form, business details, contact, goals, objectives",
            limit=5
        )
        
        if not results:
            return "## Client Intake Form\n\nNo intake form data available.\n"
        
        context = "\n\n".join([r['content'] for r in results[:3]])
        
        prompt = f"""Based on this client intake form, create a structured summary:

{context}

Include:
1. Client Overview (name, industry, size)
2. Business Goals and Objectives
3. Target Audience
4. Key Challenges
5. Desired Outcomes

Be concise but comprehensive."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a business analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return f"## Client Intake Form Analysis\n\n{response.choices[0].message.content}\n"
    
    def generate_services_section(self) -> str:
        """Generate services/products section"""
        print("🛠️  Generating services section...")
        
        results = self.query_content_type(
            content_type="services_products",
            query="services, products, offerings, capabilities, solutions",
            limit=15
        )
        
        if not results:
            return "## Services & Products\n\nNo service information available.\n"
        
        context = "\n\n".join([
            f"{r['title']}: {r['content'][:400]}"
            for r in results[:7]
        ])
        
        prompt = f"""Based on these services and products, create a comprehensive overview:

{context}

Structure the response to cover:
1. Core Services/Products
2. Key Capabilities
3. Unique Value Propositions
4. Technology or Methodology Used

Use bullet points and clear categories."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a business analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return f"## Services & Products\n\n{response.choices[0].message.content}\n"
    
    def generate_company_overview(self) -> str:
        """Generate company overview section"""
        print("🏢 Generating company overview...")
        
        results = self.query_all_content(
            query="company overview, about us, mission, vision, history, background",
            limit=10
        )
        
        if not results:
            return "## Company Overview\n\nNo company information available.\n"
        
        context = "\n\n".join([r['content'][:500] for r in results[:5]])
        
        prompt = f"""Based on this information about the company, create a comprehensive overview:

{context}

Include:
1. Company Background
2. Mission and Vision
3. Core Values
4. Market Position
5. Key Differentiators

Keep it professional and concise."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a business analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return f"## Company Overview\n\n{response.choices[0].message.content}\n"
    
    def generate_client_brief(self) -> str:
        """
        Generate complete client brief
        
        Returns:
            Complete brief as markdown string
        """
        print(f"\n{'='*80}")
        print(f"GENERATING CLIENT BRIEF: {self.client_id}")
        print(f"{'='*80}\n")
        
        # Get client stats
        stats = self.vector_store.get_client_stats(self.client_id)
        
        # Build brief
        brief = f"""# Client Brief: {self.client_id}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Database:** Supabase Vector DB
**Documents Indexed:** {stats['document_count']}
**Total Chunks:** {stats['chunk_count']}

---

"""
        
        # Generate sections
        try:
            brief += self.generate_company_overview()
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating company overview: {e}")
            brief += "## Company Overview\n\n*Error generating section*\n\n"
        
        try:
            brief += self.generate_client_intake_section()
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating intake section: {e}")
            brief += "## Client Intake Form\n\n*Error generating section*\n\n"
        
        try:
            brief += self.generate_services_section()
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating services section: {e}")
            brief += "## Services & Products\n\n*Error generating section*\n\n"
        
        try:
            brief += self.generate_case_studies_section()
            brief += "\n"
        except Exception as e:
            print(f"⚠️  Error generating case studies: {e}")
            brief += "## Case Studies\n\n*Error generating section*\n\n"
        
        brief += f"""
---

*This brief was automatically generated from {stats['document_count']} documents 
using Supabase Vector DB and OpenAI GPT-4o.*
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
            
            print(f"✅ Uploaded to Drive: {file.get('id')}")
            return file.get('id')
            
        except Exception as e:
            print(f"❌ Failed to upload to Drive: {e}")
            return None


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
    if args.drive_folder_id:
        print("📤 Uploading to Google Drive...")
        file_id = generator.upload_brief_to_drive(
            str(output_path),
            args.drive_folder_id
        )
        if file_id:
            print(f"✅ Uploaded successfully: {file_id}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
