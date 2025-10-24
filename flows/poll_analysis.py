#!/usr/bin/env python3
"""Enhanced polling script with better progress display and options."""

import os
import time
import requests
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.console import Console

console = Console()

BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro.globalforestwatch.org/api/v1').rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
LIST_ID = os.environ.get('LIST_ID')
ANALYSIS_ID = os.environ.get('ANALYSIS_ID', 'FCD')
HEADERS = {'x-api-key': TOKEN}

def poll_status_with_progress(list_id: str, analysis_id: str, max_attempts: int = 60):
    """Poll analysis status with visual progress indicator."""
    attempts = 0
    last_status = None
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Checking analysis status...", total=None)
        
        while attempts < max_attempts:
            try:
                time.sleep(60)
                res = requests.get(f'{BASE}/list/{list_id}/analysis/{analysis_id}/status', headers=HEADERS)
                res.raise_for_status()
                data = res.json()
                status_value = str(data.get('status', '')).lower()
                current_status = data.get('status')
                
                # Update progress description
                progress.update(task, description=f"Status: {current_status}")
                
                # Only print status changes
                if current_status != last_status:
                    print(f"\n[bold blue]Status changed: {current_status}[/bold blue]")
                    last_status = current_status
                
                # Check for completion states
                if status_value in {'complete', 'completed'}:
                    print(f"[green]✅ Analysis completed successfully![/green]")
                    return data
                elif status_value in {'failed', 'error', 'expired'}:
                    print(f"[red]❌ Analysis failed with status: {current_status}[/red]")
                    return data
                
                attempts += 1
                if attempts >= max_attempts:
                    print(f"[yellow]⏰ Timeout reached after {max_attempts} attempts (10 minutes)[/yellow]")
                    print(f"[yellow]Analysis may still be running. Check status later with:[/yellow]")
                    print(f"[cyan]LIST_ID={list_id} ANALYSIS_ID={analysis_id} python flows/poll_analysis.py[/cyan]")
                    return data
                
                
            except KeyboardInterrupt:
                print(f"\n[yellow]⏹️  Polling interrupted by user[/yellow]")
                print(f"[yellow]Current status: {last_status}[/yellow]")
                print(f"[yellow]You can resume checking with:[/yellow]")
                print(f"[cyan]LIST_ID={list_id} ANALYSIS_ID={analysis_id} python flows/poll_analysis.py[/cyan]")
                return data
            except Exception as e:
                print(f"[red]❌ Error checking status: {e}[/red]")
                return None

def main():
    if not TOKEN:
        raise RuntimeError('Set GFWPRO_API_TOKEN')
    if not LIST_ID:
        raise RuntimeError('Set LIST_ID environment variable')

    print(f"[bold]🔍 Monitoring analysis for List ID: {LIST_ID}[/bold]")
    print(f"[bold]📊 Analysis Type: {ANALYSIS_ID}[/bold]")
    print()
    
    result = poll_status_with_progress(LIST_ID, ANALYSIS_ID)
    
    if result and result.get('status', '').lower() in {'complete', 'completed'}:
        result_url = result.get('resultUrl')
        if result_url:
            print(f"[green]📥 Downloading results...[/green]")
            try:
                res = requests.get(result_url)
                res.raise_for_status()
                filename = f'{LIST_ID}_{ANALYSIS_ID}.zip'
                with open(filename, 'wb') as fh:
                    fh.write(res.content)
                print(f"[green]✅ Results saved to: {filename}[/green]")
            except Exception as e:
                print(f"[red]❌ Error downloading results: {e}[/red]")
        else:
            print(f"[yellow]⚠️  Analysis completed but no download URL available[/yellow]")
            print(f"[yellow]Try using the generate endpoint to create download link[/yellow]")

if __name__ == '__main__':
    main()
