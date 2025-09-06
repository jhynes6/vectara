#!/usr/bin/env python3
"""
Setup script for Vectara Workspace Inspector
"""

import os
import shutil
from pathlib import Path
import typer
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def setup_env_file():
    """Set up the .env file interactively."""
    console.print("\n[bold blue]🔧 Setting up environment configuration[/bold blue]")
    
    env_template = Path("env.template")
    env_file = Path(".env")
    
    if env_file.exists():
        overwrite = typer.confirm(f".env file already exists. Overwrite?")
        if not overwrite:
            console.print("[yellow]Keeping existing .env file[/yellow]")
            return
    
    # Copy template to .env
    shutil.copy2(env_template, env_file)
    console.print(f"[green]✓[/green] Created .env file from template")
    
    # Ask for API key
    console.print("\n[cyan]Please enter your Vectara API key:[/cyan]")
    console.print("[dim]You can get this from https://console.vectara.com[/dim]")
    
    api_key = Prompt.ask("API Key", password=True)
    
    if api_key and api_key.strip():
        # Read the .env file and replace the API key
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace the placeholder API key
        content = content.replace('your_vectara_api_key_here', api_key.strip())
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        console.print("[green]✓[/green] API key configured in .env file")
    else:
        console.print("[yellow]⚠️[/yellow] No API key provided. You'll need to edit .env manually.")
    
    console.print("\n[green]✅ Setup complete! You can now run:[/green]")
    console.print("[cyan]  python vectara_inspector.py[/cyan]")
    console.print("[cyan]  # or[/cyan]")
    console.print("[cyan]  ./run.sh[/cyan]")


def check_requirements():
    """Check if all requirements are installed."""
    console.print("[blue]Checking requirements...[/blue]")
    
    try:
        import rich
        import typer
        import requests
        import pandas
        import dotenv
        console.print("[green]✓[/green] All requirements are installed")
        return True
    except ImportError as e:
        console.print(f"[red]✗[/red] Missing requirement: {e}")
        console.print("[yellow]Run: pip install -r requirements.txt[/yellow]")
        return False


def main():
    """Main setup function."""
    console.print("[bold blue]🚀 Vectara Workspace Inspector Setup[/bold blue]")
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        console.print("[red]Error: requirements.txt not found. Make sure you're in the project directory.[/red]")
        typer.Exit(1)
    
    # Check requirements
    if not check_requirements():
        install = typer.confirm("Install requirements now?")
        if install:
            os.system("pip install -r requirements.txt")
        else:
            console.print("[yellow]Please install requirements manually and run setup again.[/yellow]")
            typer.Exit(1)
    
    # Set up .env file
    setup_env_file()


if __name__ == "__main__":
    typer.run(main)
