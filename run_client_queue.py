#!/usr/bin/env python3
"""
Client Queue Batch Runner for Agentic Workflow

This script parses a markdown file containing client onboarding queue entries
and runs the agentic workflow for each client programmatically.

Queue format:
[client_id, drive_folder_id, website_url]

Usage:
    python run_client_queue.py --queue-file client_onboarding_queue.md
    python run_client_queue.py --queue-file client_onboarding_queue.md --max-concurrent 2
    python run_client_queue.py --queue-file client_onboarding_queue.md --start-from "push-analytics"
"""

import sys
import os
import re
import asyncio
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# Import the agentic workflow
from agentic_workflow import AgenticWorkflowOrchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ClientQueueRunner')


class ClientQueueParser:
    """Parses client onboarding queue markdown files"""
    
    @staticmethod
    def parse_queue_file(file_path: str) -> List[Dict[str, str]]:
        """
        Parse markdown file with client queue entries.
        
        Expected format:
        [client_id, drive_folder_id, website_url]
        
        Returns list of client configs.
        """
        clients = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            logger.error(f"Queue file not found: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error reading queue file: {e}")
            return []
        
        # Find all queue entries (lines starting with [)
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#') or line.startswith('**'):
                continue
            
            # Look for [client_id, drive_folder_id, website_url] format
            match = re.match(r'\[([^,]+),\s*([^,]+),\s*([^\]]+)\]', line)
            if match:
                client_id, drive_folder_id, website_url = match.groups()
                
                # Clean up the values
                client_id = client_id.strip()
                drive_folder_id = drive_folder_id.strip()
                website_url = website_url.strip()
                
                # Validate client_id (alphanumeric, hyphens, underscores)
                if not re.match(r'^[a-zA-Z0-9_-]+$', client_id):
                    logger.warning(f"Invalid client_id format on line {line_num}: {client_id}")
                    continue
                
                # Validate website_url (basic URL check)
                if not (website_url.startswith('http://') or website_url.startswith('https://')):
                    logger.warning(f"Invalid website URL format on line {line_num}: {website_url}")
                    continue
                
                clients.append({
                    'client_id': client_id,
                    'drive_folder_id': drive_folder_id,
                    'website_url': website_url,
                    'line_number': line_num
                })
                
                logger.info(f"Parsed client: {client_id} -> {website_url}")
            else:
                # Log non-matching lines for debugging
                if line and not line.startswith('#') and not line.startswith('**'):
                    logger.debug(f"Skipping line {line_num}: {line}")
        
        logger.info(f"Successfully parsed {len(clients)} clients from queue file")
        return clients


class ClientQueueRunner:
    """Runs agentic workflows for clients from queue file"""
    
    def __init__(self, 
                 queue_file: str,
                 max_concurrent: int = 1,
                 start_from: Optional[str] = None,
                 output_dir: str = 'ingestion/client_ingestion_outputs',
                 workers: int = 8,
                 use_llm_categories: bool = True,
                 pdf_processor: str = 'markitdown',
                 credentials: str = './service_account.json'):
        
        self.queue_file = queue_file
        self.max_concurrent = max_concurrent
        self.start_from = start_from
        self.output_dir = output_dir
        self.workers = workers
        self.use_llm_categories = use_llm_categories
        self.pdf_processor = pdf_processor
        self.credentials = credentials
        
        # Results tracking
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def parse_queue(self) -> List[Dict[str, str]]:
        """Parse the queue file and optionally filter from start_from"""
        all_clients = ClientQueueParser.parse_queue_file(self.queue_file)
        
        if not all_clients:
            logger.error("No clients found in queue file")
            return []
        
        # Filter from start_from if specified
        if self.start_from:
            start_index = -1
            for i, client in enumerate(all_clients):
                if client['client_id'] == self.start_from:
                    start_index = i
                    break
            
            if start_index == -1:
                logger.error(f"Start client '{self.start_from}' not found in queue")
                return []
            
            all_clients = all_clients[start_index:]
            logger.info(f"Starting from client: {self.start_from} ({len(all_clients)} clients remaining)")
        
        return all_clients
    
    async def run_single_client(self, client_config: Dict[str, str]) -> Dict[str, Any]:
        """Run agentic workflow for a single client"""
        client_id = client_config['client_id']
        logger.info(f"🚀 Starting workflow for client: {client_id}")
        
        start_time = datetime.now()
        
        try:
            # Create workflow config
            config = {
                'client_id': client_id,
                'drive_folder_id': client_config['drive_folder_id'],
                'client_homepage_url': client_config['website_url'],
                'output_dir': self.output_dir,
                'workers': self.workers,
                'use_llm_categories': self.use_llm_categories,
                'pdf_processor': self.pdf_processor,
                'credentials': self.credentials
            }
            
            # Create orchestrator and run workflow
            orchestrator = AgenticWorkflowOrchestrator(config)
            result = await orchestrator.run_workflow()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Add metadata to result
            result['client_config'] = client_config
            result['duration_seconds'] = duration
            result['start_time'] = start_time.isoformat()
            result['end_time'] = end_time.isoformat()
            
            status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
            logger.info(f"{status} Client {client_id} completed in {duration:.1f}s")
            
            return result
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            error_result = {
                'success': False,
                'client_id': client_id,
                'client_config': client_config,
                'error': str(e),
                'duration_seconds': duration,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }
            
            logger.error(f"❌ FAILED Client {client_id} after {duration:.1f}s: {e}")
            return error_result
    
    async def run_queue(self) -> Dict[str, Any]:
        """Run the complete client queue"""
        clients = self.parse_queue()
        
        if not clients:
            return {
                'success': False,
                'error': 'No clients to process',
                'results': []
            }
        
        self.start_time = datetime.now()
        logger.info("")
        logger.info("🚀" * 50)
        logger.info("CLIENT QUEUE BATCH RUNNER")
        logger.info("🚀" * 50)
        logger.info(f"Queue file: {self.queue_file}")
        logger.info(f"Total clients: {len(clients)}")
        logger.info(f"Max concurrent: {self.max_concurrent}")
        logger.info(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("")
        
        # Process clients
        if self.max_concurrent == 1:
            # Sequential processing
            for i, client_config in enumerate(clients, 1):
                logger.info(f"Processing client {i}/{len(clients)}: {client_config['client_id']}")
                result = await self.run_single_client(client_config)
                self.results.append(result)
        else:
            # Concurrent processing with semaphore
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            async def run_with_semaphore(client_config):
                async with semaphore:
                    return await self.run_single_client(client_config)
            
            tasks = [run_with_semaphore(client_config) for client_config in clients]
            self.results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Convert exceptions to error results
            processed_results = []
            for i, result in enumerate(self.results):
                if isinstance(result, Exception):
                    processed_results.append({
                        'success': False,
                        'client_id': clients[i]['client_id'],
                        'client_config': clients[i],
                        'error': str(result),
                        'duration_seconds': 0,
                        'start_time': datetime.now().isoformat(),
                        'end_time': datetime.now().isoformat()
                    })
                else:
                    processed_results.append(result)
            
            self.results = processed_results
        
        self.end_time = datetime.now()
        total_duration = (self.end_time - self.start_time).total_seconds()
        
        # Generate summary
        successful = [r for r in self.results if r.get('success', False)]
        failed = [r for r in self.results if not r.get('success', False)]
        
        logger.info("")
        logger.info("=" * 80)
        logger.info("🎉 QUEUE PROCESSING COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total clients: {len(self.results)}")
        logger.info(f"Successful: {len(successful)}")
        logger.info(f"Failed: {len(failed)}")
        logger.info(f"Total duration: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
        logger.info("")
        
        if successful:
            logger.info("✅ Successful clients:")
            for result in successful:
                logger.info(f"  • {result['client_id']} ({result['duration_seconds']:.1f}s)")
        
        if failed:
            logger.info("❌ Failed clients:")
            for result in failed:
                error_msg = result.get('error', 'Unknown error')
                logger.info(f"  • {result['client_id']}: {error_msg}")
        
        logger.info("=" * 80)
        logger.info("")
        
        # Save results to file
        results_file = self.save_results()
        logger.info(f"📄 Results saved to: {results_file}")
        
        return {
            'success': len(failed) == 0,
            'total_clients': len(self.results),
            'successful_clients': len(successful),
            'failed_clients': len(failed),
            'total_duration_seconds': total_duration,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'results': self.results,
            'results_file': results_file
        }
    
    def save_results(self) -> str:
        """Save results to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"client_queue_results_{timestamp}.json"
        
        summary = {
            'queue_file': self.queue_file,
            'total_clients': len(self.results),
            'successful_clients': len([r for r in self.results if r.get('success', False)]),
            'failed_clients': len([r for r in self.results if not r.get('success', False)]),
            'total_duration_seconds': (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'max_concurrent': self.max_concurrent,
            'results': self.results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return results_file


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Run agentic workflow for clients from queue markdown file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run all clients sequentially
    python run_client_queue.py --queue-file client_onboarding_queue.md
    
    # Run with max 2 concurrent clients
    python run_client_queue.py --queue-file client_onboarding_queue.md --max-concurrent 2
    
    # Start from a specific client
    python run_client_queue.py --queue-file client_onboarding_queue.md --start-from "push-analytics"
    
    # Custom settings
    python run_client_queue.py --queue-file client_onboarding_queue.md --workers 4 --pdf-processor gpt
        """
    )
    
    parser.add_argument('--queue-file', required=True, help='Path to markdown queue file')
    parser.add_argument('--max-concurrent', type=int, default=1, 
                       help='Maximum number of concurrent clients (default: 1)')
    parser.add_argument('--start-from', help='Start processing from this client ID')
    parser.add_argument('--output-dir', default='ingestion/client_ingestion_outputs',
                       help='Output directory for client files')
    parser.add_argument('--workers', type=int, default=8,
                       help='Number of parallel workers per client')
    parser.add_argument('--no-llm-categories', action='store_true',
                       help='Disable LLM categorization')
    parser.add_argument('--pdf-processor', choices=['gpt', 'markitdown', 'pdfplumber'], 
                       default='markitdown', help='PDF processor to use')
    parser.add_argument('--credentials', default='./service_account.json',
                       help='Path to service account JSON file')
    
    args = parser.parse_args()
    
    # Validate queue file exists
    if not os.path.exists(args.queue_file):
        logger.error(f"Queue file not found: {args.queue_file}")
        return 1
    
    # Validate max concurrent
    if args.max_concurrent < 1:
        logger.error("max-concurrent must be >= 1")
        return 1
    
    # Create runner and execute
    runner = ClientQueueRunner(
        queue_file=args.queue_file,
        max_concurrent=args.max_concurrent,
        start_from=args.start_from,
        output_dir=args.output_dir,
        workers=args.workers,
        use_llm_categories=not args.no_llm_categories,
        pdf_processor=args.pdf_processor,
        credentials=args.credentials
    )
    
    try:
        result = asyncio.run(runner.run_queue())
        return 0 if result['success'] else 1
    except KeyboardInterrupt:
        logger.info("🛑 Queue processing interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Queue processing failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
