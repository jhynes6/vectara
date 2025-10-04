#!/usr/bin/env python3
"""
OpenAI Agent-Based Client Onboarding Workflow

This script reimplements the complete client onboarding workflow using OpenAI Assistants API.
Multiple specialized agents coordinate to handle:
1. Client ingestion (website + Drive content)
2. PDF reprocessing
3. Vertex AI RAG upload
4. Client brief generation

Architecture:
- Coordinator Agent: Orchestrates the workflow and makes decisions
- Ingestion Agent: Handles website and Drive content ingestion
- PDF Agent: Processes and reprocesses PDFs
- Brief Agent: Generates comprehensive client briefs
- Upload Agent: Manages Vertex AI RAG uploads

Usage:
    python agentic_workflow.py --client-id "client-name" \\
        --drive-folder-id "1ABC123..." \\
        --client-homepage-url "https://example.com"
"""

import sys
import os
import json
import argparse
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Add OpenAI to path
sys.path.insert(0, '/home/ubuntu/.local/lib/python3.13/site-packages')
from openai import OpenAI, AsyncOpenAI

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AgenticWorkflow')

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'ingestion'))


class WorkflowTools:
    """Tools that agents can use to perform workflow tasks"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client_id = config['client_id']
        self.drive_folder_id = config.get('drive_folder_id', '')
        self.client_homepage_url = config.get('client_homepage_url', '')
        self.output_dir = config.get('output_dir', 'ingestion/client_ingestion_outputs')
        self.workers = config.get('workers', 4)
        self.credentials = config.get('credentials', './service_account.json')
        self.pdf_processor = config.get('pdf_processor', 'markitdown')
        
        # Workflow state
        self.state = {
            'ingestion_complete': False,
            'pdf_reprocessing_complete': False,
            'upload_complete': False,
            'brief_complete': False,
            'errors': []
        }
    
    async def run_ingestion(self) -> Dict[str, Any]:
        """Run client ingestion (website + Drive)"""
        logger.info("🔧 Tool: run_ingestion")
        
        try:
            from new_client_ingestion import VertexAIClientOnboarder
            
            onboarder = VertexAIClientOnboarder(
                client_id=self.client_id,
                drive_folder_id=self.drive_folder_id,
                client_homepage_url=self.client_homepage_url,
                output_dir=self.output_dir,
                workers=self.workers,
                credentials_file=self.credentials,
                pdf_processor=self.pdf_processor
            )
            
            # Create directories
            onboarder.create_client_directories()
            
            # Create corpus
            onboarder.create_vertex_corpus()
            
            # Run ingestion
            website_task = onboarder.run_website_ingestion(self.config.get('use_llm_categories', True))
            drive_task = onboarder.run_drive_ingestion(self.config.get('use_llm_categories', True))
            
            website_result, drive_result = await asyncio.gather(website_task, drive_task)
            
            self.state['ingestion_complete'] = True
            
            return {
                'success': True,
                'website_result': str(website_result),
                'drive_result': str(drive_result),
                'message': 'Ingestion completed successfully'
            }
            
        except Exception as e:
            error_msg = f"Ingestion failed: {str(e)}"
            self.state['errors'].append(error_msg)
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def reprocess_pdfs(self) -> Dict[str, Any]:
        """Reprocess failed PDFs"""
        logger.info("🔧 Tool: reprocess_pdfs")
        
        try:
            from reprocess_failed_pdfs import FailedPDFReprocessor
            
            client_output_dir = os.path.join(self.output_dir, self.client_id)
            reprocessor = FailedPDFReprocessor(output_dir=client_output_dir)
            
            # Scan for failed PDFs
            failed_pdfs = reprocessor.scan_for_failed_pdfs()
            reprocessor.failed_files = [{'file': Path(f[0]).name, 'file_id': f[1]} for f in failed_pdfs]
            
            if not failed_pdfs:
                self.state['pdf_reprocessing_complete'] = True
                return {
                    'success': True,
                    'message': 'No failed PDFs found',
                    'reprocessed_count': 0,
                    'failed_count': 0
                }
            
            # Reprocess each failed PDF
            for md_file_path, file_id, metadata in failed_pdfs:
                reprocessor.reprocess_failed_pdf(
                    md_file_path, file_id, metadata,
                    method='auto',
                    credentials_file=self.credentials
                )
            
            self.state['pdf_reprocessing_complete'] = True
            
            return {
                'success': True,
                'message': f'Reprocessed {len(reprocessor.reprocessed_files)} PDFs',
                'reprocessed_count': len(reprocessor.reprocessed_files),
                'failed_count': len(reprocessor.still_failed),
                'still_failed': [Path(f).name for f in reprocessor.still_failed]
            }
            
        except Exception as e:
            error_msg = f"PDF reprocessing failed: {str(e)}"
            self.state['errors'].append(error_msg)
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def upload_to_vertex(self) -> Dict[str, Any]:
        """Upload processed files to Vertex AI RAG"""
        logger.info("🔧 Tool: upload_to_vertex")
        
        try:
            from new_client_ingestion import VertexAIClientOnboarder
            
            onboarder = VertexAIClientOnboarder(
                client_id=self.client_id,
                drive_folder_id=self.drive_folder_id,
                client_homepage_url=self.client_homepage_url,
                output_dir=self.output_dir,
                workers=self.workers,
                credentials_file=self.credentials,
                pdf_processor=self.pdf_processor
            )
            
            files_to_upload = onboarder.get_files_to_upload()
            successful_uploads, failed_uploads = onboarder.upload_files_to_vertex_ai(files_to_upload)
            total_files = successful_uploads + failed_uploads
            
            # Generate report
            report_file = onboarder.generate_onboarding_report((successful_uploads, failed_uploads))
            
            self.state['upload_complete'] = True
            
            return {
                'success': True,
                'message': f'Uploaded {successful_uploads}/{total_files} files to Vertex AI',
                'successful_uploads': successful_uploads,
                'failed_uploads': failed_uploads,
                'total_files': total_files,
                'report_file': str(report_file)
            }
            
        except Exception as e:
            error_msg = f"Vertex AI upload failed: {str(e)}"
            self.state['errors'].append(error_msg)
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def generate_brief(self) -> Dict[str, Any]:
        """Generate client brief"""
        logger.info("🔧 Tool: generate_brief")
        
        try:
            from client_brief_generator import ClientBriefGenerator
            
            generator = ClientBriefGenerator(
                corpus_key=self.client_id,
                drive_folder_id=self.drive_folder_id,
                credentials_file=self.credentials
            )
            
            # Generate brief
            brief = generator.generate_client_brief()
            
            # Save brief
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.client_id}_client_brief_{timestamp}.md"
            outputs_dir = Path(__file__).parent / "outputs"
            outputs_dir.mkdir(exist_ok=True)
            brief_path = outputs_dir / filename
            
            with open(brief_path, 'w', encoding='utf-8') as f:
                f.write(brief)
            
            # Upload to Drive if configured
            upload_success = False
            if self.drive_folder_id:
                file_id = generator.upload_brief_to_drive(str(brief_path), self.drive_folder_id)
                upload_success = bool(file_id)
            
            self.state['brief_complete'] = True
            
            return {
                'success': True,
                'message': 'Brief generated successfully',
                'brief_path': str(brief_path),
                'brief_size': len(brief),
                'uploaded_to_drive': upload_success
            }
            
        except Exception as e:
            error_msg = f"Brief generation failed: {str(e)}"
            self.state['errors'].append(error_msg)
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def get_state(self) -> Dict[str, Any]:
        """Get current workflow state"""
        return self.state


class AgenticWorkflowOrchestrator:
    """Orchestrates the workflow using OpenAI Assistants as agents"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client_id = config['client_id']
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.openai_client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)
        
        # Initialize workflow tools
        self.tools = WorkflowTools(config)
        
        # Agent IDs (will be created)
        self.coordinator_agent_id = None
        
        logger.info("✅ Agentic workflow orchestrator initialized")
    
    def create_coordinator_agent(self) -> str:
        """Create the coordinator agent using OpenAI Assistants API"""
        logger.info("Creating coordinator agent...")
        
        instructions = """You are the Coordinator Agent for a client onboarding workflow.

Your job is to orchestrate the complete client onboarding process through these steps:

1. **Ingestion Phase**: Ingest client website and Google Drive content
2. **PDF Processing Phase**: Reprocess any failed PDF extractions
3. **Upload Phase**: Upload all processed content to Vertex AI RAG
4. **Brief Generation Phase**: Generate a comprehensive client brief

You must:
- Execute steps in the correct order
- Check for errors after each step
- Make decisions about whether to continue or abort
- Provide clear status updates
- Handle failures gracefully

After each step, analyze the results and decide the next action.
If a step fails, you should report it and decide whether to continue or abort.

Your response should be concise and actionable."""

        tools_spec = [
            {
                "type": "function",
                "function": {
                    "name": "run_ingestion",
                    "description": "Run client ingestion (website scraping + Google Drive download). This must be the first step.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "reprocess_pdfs",
                    "description": "Reprocess any PDFs that failed during ingestion. Run this after ingestion.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "upload_to_vertex",
                    "description": "Upload all processed files to Vertex AI RAG corpus. Run after PDF reprocessing.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_brief",
                    "description": "Generate comprehensive client brief. Run after upload is complete.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_state",
                    "description": "Get the current state of the workflow",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]
        
        assistant = self.openai_client.beta.assistants.create(
            name=f"Coordinator Agent - {self.client_id}",
            instructions=instructions,
            tools=tools_spec,
            model="gpt-4o-2024-11-20"  # Latest model with good function calling
        )
        
        self.coordinator_agent_id = assistant.id
        logger.info(f"✅ Created coordinator agent: {assistant.id}")
        
        return assistant.id
    
    async def execute_tool_call(self, tool_name: str, tool_args: Dict) -> Dict[str, Any]:
        """Execute a tool call"""
        logger.info(f"🛠️  Executing tool: {tool_name}")
        
        tool_methods = {
            'run_ingestion': self.tools.run_ingestion,
            'reprocess_pdfs': self.tools.reprocess_pdfs,
            'upload_to_vertex': self.tools.upload_to_vertex,
            'generate_brief': self.tools.generate_brief,
            'get_state': self.tools.get_state
        }
        
        if tool_name not in tool_methods:
            return {'error': f'Unknown tool: {tool_name}'}
        
        tool_method = tool_methods[tool_name]
        
        # Call async methods with await, sync methods directly
        if asyncio.iscoroutinefunction(tool_method):
            result = await tool_method()
        else:
            result = tool_method()
        
        logger.info(f"✅ Tool {tool_name} completed: {result.get('success', False)}")
        return result
    
    async def run_workflow(self) -> Dict[str, Any]:
        """Run the complete workflow using the coordinator agent"""
        start_time = datetime.now()
        
        logger.info("")
        logger.info("🚀" * 40)
        logger.info("AGENTIC CLIENT ONBOARDING WORKFLOW (OpenAI Assistants)")
        logger.info("🚀" * 40)
        logger.info(f"Client: {self.client_id}")
        logger.info(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("")
        
        try:
            # Create coordinator agent
            agent_id = self.create_coordinator_agent()
            
            # Create a thread for this workflow
            thread = self.openai_client.beta.threads.create()
            logger.info(f"Created conversation thread: {thread.id}")
            
            # Send initial message to coordinator
            initial_message = f"""Please orchestrate the complete client onboarding workflow for client: {self.client_id}

Website: {self.config.get('client_homepage_url', 'N/A')}
Drive Folder: {self.config.get('drive_folder_id', 'N/A')}

Execute all phases in order:
1. Ingestion
2. PDF Reprocessing
3. Upload to Vertex AI
4. Brief Generation

Proceed with the workflow."""
            
            self.openai_client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=initial_message
            )
            
            # Run the assistant
            run = self.openai_client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=agent_id
            )
            
            logger.info("🤖 Coordinator agent is now orchestrating the workflow...")
            
            # Poll for completion and handle tool calls
            max_iterations = 50  # Prevent infinite loops
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                # Get run status
                run = self.openai_client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                
                logger.info(f"Agent status: {run.status} (iteration {iteration})")
                
                if run.status == 'completed':
                    logger.info("✅ Workflow completed!")
                    break
                
                elif run.status == 'requires_action':
                    # Handle tool calls
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    logger.info(f"Agent requested {len(tool_calls)} tool call(s)")
                    
                    tool_outputs = []
                    for tool_call in tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                        
                        logger.info(f"  📞 Tool call: {tool_name}")
                        
                        # Execute the tool
                        result = await self.execute_tool_call(tool_name, tool_args)
                        
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(result)
                        })
                    
                    # Submit tool outputs
                    run = self.openai_client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                
                elif run.status in ['failed', 'cancelled', 'expired']:
                    logger.error(f"❌ Workflow {run.status}")
                    if run.last_error:
                        logger.error(f"Error: {run.last_error}")
                    break
                
                # Wait before polling again
                await asyncio.sleep(2)
            
            # Get final messages
            messages = self.openai_client.beta.threads.messages.list(
                thread_id=thread.id,
                order='asc'
            )
            
            # Extract agent responses
            agent_responses = []
            for msg in messages.data:
                if msg.role == 'assistant':
                    for content in msg.content:
                        if hasattr(content, 'text'):
                            agent_responses.append(content.text.value)
            
            # Get final state
            final_state = self.tools.get_state()
            
            # Generate report
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("")
            logger.info("=" * 80)
            logger.info("🎉 AGENTIC WORKFLOW FINISHED")
            logger.info("=" * 80)
            logger.info(f"Client: {self.client_id}")
            logger.info(f"Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
            logger.info("")
            logger.info("Results:")
            logger.info(f"  {'✅' if final_state['ingestion_complete'] else '❌'} Ingestion: {'Complete' if final_state['ingestion_complete'] else 'Failed'}")
            logger.info(f"  {'✅' if final_state['pdf_reprocessing_complete'] else '❌'} PDF Reprocessing: {'Complete' if final_state['pdf_reprocessing_complete'] else 'Failed'}")
            logger.info(f"  {'✅' if final_state['upload_complete'] else '❌'} Vertex Upload: {'Complete' if final_state['upload_complete'] else 'Failed'}")
            logger.info(f"  {'✅' if final_state['brief_complete'] else '❌'} Brief Generation: {'Complete' if final_state['brief_complete'] else 'Failed'}")
            
            if final_state['errors']:
                logger.info(f"\n⚠️  Errors encountered:")
                for error in final_state['errors']:
                    logger.info(f"  • {error}")
            
            logger.info("=" * 80)
            logger.info("")
            
            # Clean up
            self.openai_client.beta.assistants.delete(agent_id)
            logger.info(f"🧹 Cleaned up agent: {agent_id}")
            
            return {
                'success': all([
                    final_state['ingestion_complete'],
                    final_state['upload_complete'],
                    final_state.get('brief_complete', True)  # Optional
                ]),
                'client_id': self.client_id,
                'duration_seconds': duration,
                'state': final_state,
                'agent_responses': agent_responses
            }
            
        except Exception as e:
            logger.error(f"❌ Workflow failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            return {
                'success': False,
                'client_id': self.client_id,
                'error': str(e)
            }


def get_user_inputs() -> Optional[Dict[str, Any]]:
    """Interactively collect user inputs"""
    print("\n" + "🚀" * 40)
    print("AGENTIC CLIENT ONBOARDING WORKFLOW (OpenAI)")
    print("🚀" * 40)
    print("\nThis workflow uses OpenAI Assistants to orchestrate:")
    print("  1. Client ingestion (website + Drive)")
    print("  2. PDF reprocessing")
    print("  3. Vertex AI RAG upload")
    print("  4. Client brief generation")
    print("\nPlease provide the following information:\n")
    
    # Get client ID
    while True:
        client_id = input("👤 Client ID (unique identifier): ").strip()
        if client_id and all(c.isalnum() or c in '-_' for c in client_id):
            break
        print("❌ Please enter a valid client ID (alphanumeric characters, hyphens, and underscores only)")
    
    # Get Drive folder ID
    while True:
        drive_input = input("💾 Google Drive folder ID or URL: ").strip()
        if not drive_input:
            print("❌ Please enter a Google Drive folder ID or URL")
            continue
        
        try:
            if drive_input.startswith('http'):
                if '/folders/' in drive_input:
                    drive_folder_id = drive_input.split('/folders/')[1].split('?')[0].split('#')[0]
                else:
                    print("❌ Invalid Google Drive folder URL format")
                    continue
            else:
                drive_folder_id = drive_input
            break
        except Exception:
            print("❌ Invalid Google Drive folder ID or URL")
    
    # Get client homepage URL
    while True:
        homepage_url = input("🌐 Client homepage URL (e.g., https://example.com): ").strip()
        if not homepage_url:
            print("❌ Please enter a homepage URL")
            continue
        
        if not homepage_url.startswith(('http://', 'https://')):
            homepage_url = 'https://' + homepage_url
        
        try:
            from urllib.parse import urlparse
            result = urlparse(homepage_url)
            if result.scheme and result.netloc:
                break
            else:
                print("❌ Please enter a valid URL")
        except Exception:
            print("❌ Please enter a valid URL")
    
    print("\n⚙️  Optional Settings:")
    
    workers_input = input("⚡ Number of parallel workers [4]: ").strip()
    workers = int(workers_input) if workers_input else 4
    
    llm_choice = input("🤖 Enable LLM categorization? [Y/n]: ").strip().lower()
    use_llm_categories = llm_choice != 'n' and llm_choice != 'no'
    
    print("\n📄 PDF Processor:")
    print("   1. markitdown (recommended)")
    print("   2. gpt (most accurate, expensive)")
    print("   3. pdfplumber (basic)")
    pdf_choice = input("Select [1/2/3, default: 1]: ").strip()
    pdf_map = {'1': 'markitdown', '2': 'gpt', '3': 'pdfplumber', '': 'markitdown'}
    pdf_processor = pdf_map.get(pdf_choice, 'markitdown')
    
    credentials = input("🔑 Service account JSON path [./service_account.json]: ").strip()
    if not credentials:
        credentials = './service_account.json'
    
    print("\n📋 Configuration Summary:")
    print("-" * 50)
    print(f"Client ID: {client_id}")
    print(f"Website: {homepage_url}")
    print(f"Drive Folder: {drive_folder_id}")
    print(f"Workers: {workers}")
    print(f"LLM Categories: {'Yes' if use_llm_categories else 'No'}")
    print(f"PDF Processor: {pdf_processor}")
    
    confirm = input("\n✅ Start workflow? [Y/n]: ").strip().lower()
    if confirm in ['n', 'no']:
        print("❌ Cancelled")
        return None
    
    return {
        'client_id': client_id,
        'drive_folder_id': drive_folder_id,
        'client_homepage_url': homepage_url,
        'workers': workers,
        'use_llm_categories': use_llm_categories,
        'pdf_processor': pdf_processor,
        'credentials': credentials
    }


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Agentic client onboarding workflow using OpenAI Assistants',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--client-id', help='Client ID')
    parser.add_argument('--drive-folder-id', help='Google Drive folder ID')
    parser.add_argument('--client-homepage-url', help='Client homepage URL')
    parser.add_argument('--output-dir', default='ingestion/client_ingestion_outputs')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--no-llm-categories', action='store_true')
    parser.add_argument('--pdf-processor', choices=['gpt', 'markitdown', 'pdfplumber'], default='markitdown')
    parser.add_argument('--credentials', default='./service_account.json')
    parser.add_argument('--batch-mode', action='store_true')
    
    args = parser.parse_args()
    
    # Determine mode
    if args.batch_mode or (args.client_id and args.drive_folder_id and args.client_homepage_url):
        if not (args.client_id and args.drive_folder_id and args.client_homepage_url):
            logger.error("❌ Batch mode requires --client-id, --drive-folder-id, and --client-homepage-url")
            return 1
        
        config = {
            'client_id': args.client_id,
            'drive_folder_id': args.drive_folder_id,
            'client_homepage_url': args.client_homepage_url,
            'output_dir': args.output_dir,
            'workers': args.workers,
            'use_llm_categories': not args.no_llm_categories,
            'pdf_processor': args.pdf_processor,
            'credentials': args.credentials
        }
    else:
        # Interactive mode
        config = get_user_inputs()
        if config is None:
            return 1
    
    # Create orchestrator and run workflow
    orchestrator = AgenticWorkflowOrchestrator(config)
    result = await orchestrator.run_workflow()
    
    return 0 if result['success'] else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
