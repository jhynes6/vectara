#!/usr/bin/env python3
"""
Vectara Workspace Inspector

This script lists all agents, corpora, and documents in a Vectara workspace.
It uses the Vectara API to fetch and display workspace information.
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

console = Console()

@dataclass
class VectaraConfig:
    """Configuration for Vectara API access."""
    api_key: str
    endpoint: str = "https://api.vectara.io"
    
    @classmethod
    def from_env(cls) -> "VectaraConfig":
        """Create config from environment variables."""
        api_key = os.getenv("VECTARA_API_KEY")
        if not api_key:
            raise ValueError(
                "VECTARA_API_KEY environment variable is required. "
                "Please set it in your environment or .env file."
            )
        
        endpoint = os.getenv("VECTARA_ENDPOINT", "https://api.vectara.io")
        return cls(api_key=api_key, endpoint=endpoint)


class VectaraClient:
    """Client for interacting with the Vectara API."""
    
    def __init__(self, config: VectaraConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": config.api_key,
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the Vectara API."""
        url = f"{self.config.endpoint}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            console.print(f"[red]API Error:[/red] {e}")
            if hasattr(e, 'response') and e.response is not None:
                console.print(f"[red]Response:[/red] {e.response.text}")
            raise
    
    def list_corpora(self) -> List[Dict[str, Any]]:
        """List all corpora in the workspace."""
        console.print("[blue]Fetching corpora...[/blue]")
        
        corpora = []
        page_key = None
        
        while True:
            params = {"limit": 100}
            if page_key:
                params["page_key"] = page_key
                
            try:
                response = self._make_request("GET", "/v2/corpora", params=params)
                
                # Add corpora from this page
                corpora.extend(response.get("corpora", []))
                
                # Check for next page
                metadata = response.get("metadata", {})
                page_key = metadata.get("page_key")
                
                if not page_key:
                    break
                    
            except Exception as e:
                console.print(f"[red]Error fetching corpora:[/red] {e}")
                break
        
        return corpora
    
    def list_documents_in_corpus(self, corpus_key: str) -> List[Dict[str, Any]]:
        """List all documents in a specific corpus."""
        console.print(f"[blue]Fetching documents from corpus: {corpus_key}[/blue]")
        
        documents = []
        page_key = None
        
        while True:
            params = {"limit": 100}
            if page_key:
                params["page_key"] = page_key
                
            try:
                response = self._make_request("GET", f"/v2/corpora/{corpus_key}/documents", params=params)
                
                # Add documents from this page
                documents.extend(response.get("documents", []))
                
                # Check for next page
                metadata = response.get("metadata", {})
                page_key = metadata.get("page_key")
                
                if not page_key:
                    break
                    
            except Exception as e:
                console.print(f"[red]Error fetching documents from corpus {corpus_key}:[/red] {e}")
                break
        
        return documents
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        try:
            return self._make_request("GET", "/v2/account")
        except Exception as e:
            console.print(f"[red]Error fetching account info:[/red] {e}")
            return {}
    
    def update_document_metadata(self, corpus_key: str, document_id: str, metadata: Dict[str, Any]) -> bool:
        """Update metadata for a specific document."""
        try:
            payload = {
                "metadata": metadata
            }
            response = self._make_request("PATCH", f"/v2/corpora/{corpus_key}/documents/{document_id}", json=payload)
            return True
        except Exception as e:
            console.print(f"[red]Error updating document {document_id}:[/red] {e}")
            return False
    
    def bulk_update_documents_with_date_created(self, corpus_key: str) -> int:
        """Add date_created metadata to all documents in a corpus."""
        from datetime import datetime
        
        console.print(f"[blue]Updating all documents in corpus {corpus_key} with date_created field...[/blue]")
        
        # Get all documents
        documents = self.list_documents_in_corpus(corpus_key)
        updated_count = 0
        
        # Current timestamp for date_created
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        for doc in documents:
            doc_id = doc.get("id")
            existing_metadata = doc.get("metadata", {})
            
            # Only add date_created if it doesn't already exist
            if "date_created" not in existing_metadata:
                # Add date_created to existing metadata
                updated_metadata = existing_metadata.copy()
                updated_metadata["date_created"] = current_time
                
                if self.update_document_metadata(corpus_key, doc_id, updated_metadata):
                    console.print(f"[green]✓[/green] Updated document: {doc_id}")
                    updated_count += 1
                else:
                    console.print(f"[red]✗[/red] Failed to update document: {doc_id}")
            else:
                console.print(f"[yellow]⚠[/yellow] Document {doc_id} already has date_created")
        
        return updated_count


def list_agents(client: VectaraClient):
    """List all agents (this may not be available via API yet)."""
    console.print("\n[bold cyan]🤖 Vectara Agents[/bold cyan]")
    
    # Note: As of my knowledge, Vectara doesn't have a dedicated agents API endpoint
    # This would likely be part of a future update to their API
    try:
        # Try to see if there's an agents endpoint
        agents = client._make_request("GET", "/v2/agents")
        
        if agents:
            agents_table = Table(title="Agents")
            agents_table.add_column("Agent ID", style="cyan")
            agents_table.add_column("Name", style="green")
            agents_table.add_column("Description", style="white")
            
            for agent in agents.get("agents", []):
                agents_table.add_row(
                    agent.get("id", "N/A"),
                    agent.get("name", "N/A"),
                    agent.get("description", "N/A")
                )
            
            console.print(agents_table)
        else:
            console.print("[yellow]No agents found or agents endpoint not available[/yellow]")
            
    except Exception:
        console.print("[yellow]⚠️ Agents API endpoint not available yet.[/yellow]")
        console.print("[dim]Note: Agents are typically created and managed through the vectara-agentic library, not the REST API.[/dim]")


def list_corpora(client: VectaraClient):
    """List all corpora in the workspace."""
    console.print("\n[bold cyan]📚 Vectara Corpora[/bold cyan]")
    
    try:
        corpora = client.list_corpora()
        
        if not corpora:
            console.print("[yellow]No corpora found[/yellow]")
            return corpora
        
        corpora_table = Table(title="Corpora")
        corpora_table.add_column("Name", style="cyan")
        corpora_table.add_column("Key", style="green") 
        corpora_table.add_column("Description", style="white")
        corpora_table.add_column("Created", style="yellow")
        
        for corpus in corpora:
            name = corpus.get("name", "N/A")
            key = corpus.get("key", "N/A")
            description = corpus.get("description", "No description")
            created = corpus.get("created_at", "N/A")
            
            # Truncate description if too long
            if len(description) > 60:
                description = description[:57] + "..."
                
            corpora_table.add_row(name, key, description, created)
        
        console.print(corpora_table)
        console.print(f"\n[green]Total corpora: {len(corpora)}[/green]")
        
        return corpora
        
    except Exception as e:
        console.print(f"[red]Error listing corpora:[/red] {e}")
        return []


def list_documents_in_corpora(client: VectaraClient, corpora: List[Dict[str, Any]]):
    """List all documents in each corpus."""
    console.print("\n[bold cyan]📄 Documents in Corpora[/bold cyan]")
    
    if not corpora:
        console.print("[yellow]No corpora available to check for documents[/yellow]")
        return
    
    total_docs = 0
    
    for corpus in corpora:
        corpus_name = corpus.get("name", "Unknown")
        corpus_key = corpus.get("key", "unknown")
        
        console.print(f"\n[bold green]📁 Corpus: {corpus_name} (Key: {corpus_key})[/bold green]")
        
        try:
            documents = client.list_documents_in_corpus(corpus_key)
            
            if not documents:
                console.print("  [yellow]No documents found[/yellow]")
                continue
            
            # Create a table for this corpus's documents
            docs_table = Table(title=f"Documents in {corpus_name}")
            docs_table.add_column("Document ID", style="cyan", width=25)
            docs_table.add_column("Title", style="green", width=35)
            docs_table.add_column("Content Type", style="blue", width=15)
            docs_table.add_column("Source", style="magenta", width=12)
            docs_table.add_column("Date Created", style="yellow", width=15)
            
            for doc in documents:
                doc_id = doc.get("id", "N/A")
                metadata = doc.get("metadata", {})
                
                # Extract the actual metadata fields
                title = metadata.get("title", "Untitled")
                content_type = metadata.get("content_type", "N/A")
                source = metadata.get("source", "N/A")
                date_created = metadata.get("date_created", "N/A")
                
                # Clean up title (remove newlines and extra whitespace)
                if title and title != "Untitled":
                    title = title.strip().replace('\n', ' ').replace('\r', ' ')
                
                # Format date_created as m/d/y hh:mm
                formatted_date = "N/A"
                if date_created and date_created != "N/A":
                    try:
                        from datetime import datetime
                        # Try to parse the date - handle various formats
                        if "T" in date_created:  # ISO format
                            dt = datetime.fromisoformat(date_created.replace("Z", "+00:00"))
                            formatted_date = dt.strftime("%-m/%-d/%Y %H:%M")
                        else:
                            # Try other common formats
                            try:
                                dt = datetime.strptime(date_created, "%Y-%m-%d %H:%M:%S")
                                formatted_date = dt.strftime("%-m/%-d/%Y %H:%M")
                            except ValueError:
                                formatted_date = date_created[:14] if len(date_created) > 14 else date_created
                    except Exception:
                        formatted_date = date_created[:14] if len(date_created) > 14 else date_created
                
                # Truncate long fields to fit in columns
                if len(title) > 34:
                    title = title[:31] + "..."
                if len(doc_id) > 24:
                    doc_id = doc_id[:21] + "..."
                if len(content_type) > 14:
                    content_type = content_type[:11] + "..."
                if len(source) > 11:
                    source = source[:8] + "..."
                
                docs_table.add_row(doc_id, title, content_type, source, formatted_date)
            
            console.print(docs_table)
            console.print(f"  [green]Documents in this corpus: {len(documents)}[/green]")
            total_docs += len(documents)
            
        except Exception as e:
            console.print(f"  [red]Error fetching documents from corpus {corpus_key}:[/red] {e}")
    
    console.print(f"\n[bold green]📊 Total documents across all corpora: {total_docs}[/bold green]")


def main(
    api_key: Optional[str] = typer.Option(
        None, 
        "--api-key", 
        help="Vectara API key (can also be set via VECTARA_API_KEY environment variable)"
    ),
    endpoint: Optional[str] = typer.Option(
        "https://api.vectara.io",
        "--endpoint", 
        help="Vectara API endpoint"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output"
    ),
    update_dates: bool = typer.Option(
        False,
        "--update-dates",
        "-u",
        help="Update all documents in dodeka-digital corpus with date_created metadata"
    )
):
    """
    Inspect your Vectara workspace: list agents, corpora, and documents.
    """
    console.print("\n[bold blue]🔍 Vectara Workspace Inspector[/bold blue]")
    console.print("[dim]Analyzing your Vectara workspace...[/dim]\n")
    
    try:
        # Set up configuration
        if api_key:
            os.environ["VECTARA_API_KEY"] = api_key
        if endpoint:
            os.environ["VECTARA_ENDPOINT"] = endpoint
            
        config = VectaraConfig.from_env()
        client = VectaraClient(config)
        
        # Display account information
        if verbose:
            account_info = client.get_account_info()
            if account_info:
                console.print(f"[bold green]Account ID:[/bold green] {account_info.get('id', 'N/A')}")
                console.print(f"[bold green]Account Name:[/bold green] {account_info.get('name', 'N/A')}")
        
        # Handle update dates option
        if update_dates:
            console.print("\n[bold yellow]🔄 Updating Documents with Date Created Metadata[/bold yellow]")
            confirm = typer.confirm("This will add 'date_created' metadata to all documents in the dodeka-digital corpus. Continue?")
            if confirm:
                updated_count = client.bulk_update_documents_with_date_created("dodeka-digital")
                console.print(f"\n[bold green]✅ Updated {updated_count} documents with date_created metadata[/bold green]")
            else:
                console.print("[yellow]Update cancelled[/yellow]")
            return
        
        # List agents
        list_agents(client)
        
        # List corpora
        corpora = list_corpora(client)
        
        # List documents in each corpus
        if corpora:
            list_documents_in_corpora(client, corpora)
        
        console.print("\n[bold green]✅ Workspace inspection complete![/bold green]")
        
    except ValueError as e:
        console.print(f"[red]Configuration Error:[/red] {e}")
        console.print("\n[yellow]💡 Tip:[/yellow] Set your VECTARA_API_KEY environment variable or create a .env file")
        typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected Error:[/red] {e}")
        if verbose:
            import traceback
            console.print(f"[red]Traceback:[/red]\n{traceback.format_exc()}")
        typer.Exit(1)


if __name__ == "__main__":
    typer.run(main)
