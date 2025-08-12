"""Linux system analysis tool for ANT."""

import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import socket
from rich.console import Console
from rich.syntax import Syntax

console = Console()


def analyze_linux_system() -> Dict[str, Any]:
    """Perform comprehensive Linux system analysis.
    
    Returns:
        Dict containing detailed system analysis and formatted report
    """
    
    def run_command(cmd: str, description: str = "") -> str:
        """Run a command and return output safely with real-time display."""
        try:
            # Show what we're running
            console.print(f"\n[dim]Running:[/dim] [bold cyan]{cmd}[/bold cyan]")
            if description:
                console.print(f"[dim]{description}[/dim]")
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            output = result.stdout.strip()
            
            # Show a sample of the output
            if output:
                # Show first few lines of output
                lines = output.split('\n')
                preview_lines = lines[:3] if len(lines) > 3 else lines
                console.print("[dim]Output:[/dim]")
                for line in preview_lines:
                    console.print(f"[dim]  {line}[/dim]")
                if len(lines) > 3:
                    console.print(f"[dim]  ... ({len(lines) - 3} more lines)[/dim]")
            else:
                console.print("[dim]  (no output)[/dim]")
                
            return output
        except subprocess.TimeoutExpired:
            console.print("[red]  Command timed out[/red]")
            return ""
        except Exception as e:
            console.print(f"[red]  Error: {str(e)}[/red]")
            return ""
    
    def parse_size(size_str: str) -> float:
        """Parse size string like '64Gi' or '931.5G' to GB."""
        if not size_str:
            return 0
        
        # Extract number and unit
        match = re.match(r'([\d.]+)([KMGTP]?i?[Bb]?)', size_str)
        if not match:
            return 0
        
        num = float(match.group(1))
        unit = match.group(2).upper()
        
        # Convert to GB
        multipliers = {
            'B': 1e-9, 'KB': 1e-6, 'MB': 1e-3, 'GB': 1,
            'TB': 1000, 'PB': 1000000,
            'KIB': 1024**-3, 'MIB': 1024**-2, 'GIB': 1024**-1,
            'TIB': 1024, 'PIB': 1024**2
        }
        
        return num * multipliers.get(unit, 1)
    
    analysis = {}
    
    console.print("\n[bold green]🔍 Starting Linux System Analysis...[/bold green]\n")
    
    # System Overview
    console.print("[bold blue]📋 Gathering System Overview[/bold blue]")
    analysis['system'] = {
        'hostname': socket.gethostname(),
        'os_info': run_command("lsb_release -d 2>/dev/null | cut -d: -f2 | xargs", "Getting OS information") or 
                  run_command("cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"'", "Fallback OS detection"),
        'kernel': run_command("uname -r", "Getting kernel version"),
        'architecture': run_command("uname -m", "Getting system architecture"),
        'uptime': run_command("uptime -p", "Getting system uptime"),
        'uptime_since': run_command("uptime -s", "Getting boot time")
    }
    
    # CPU Information
    console.print("\n[bold blue]🖥️  Analyzing CPU Performance[/bold blue]")
    cpu_info = run_command("lscpu", "Getting detailed CPU information")
    cpu_model = run_command("grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | xargs", "Getting CPU model")
    cpu_cores = run_command("nproc --all", "Counting CPU cores")
    cpu_threads = run_command("grep -c ^processor /proc/cpuinfo", "Counting CPU threads")
    load_avg = run_command("uptime | grep -o 'load average:.*' | cut -d: -f2 | xargs", "Getting load average")
    
    analysis['cpu'] = {
        'model': cpu_model,
        'cores': cpu_cores,
        'threads': cpu_threads,
        'load_average': load_avg,
        'details': cpu_info
    }
    
    # Memory Information
    console.print("\n[bold blue]🧠 Analyzing Memory Usage[/bold blue]")
    mem_info = run_command("free -h", "Getting memory information")
    mem_total = run_command("free -h | grep Mem | awk '{print $2}'", "Getting total memory")
    mem_used = run_command("free -h | grep Mem | awk '{print $3}'", "Getting used memory")
    mem_available = run_command("free -h | grep Mem | awk '{print $7}'", "Getting available memory")
    swap_info = run_command("free -h | grep Swap | awk '{print $2}'", "Getting swap information")
    
    analysis['memory'] = {
        'total': mem_total,
        'used': mem_used,
        'available': mem_available,
        'swap': swap_info,
        'details': mem_info
    }
    
    # GPU Information
    console.print("\n[bold blue]🎮 Detecting GPU Hardware[/bold blue]")
    gpu_info = ""
    nvidia_info = run_command("nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used,utilization.gpu,power.draw,power.limit --format=csv,noheader,nounits 2>/dev/null", "Checking for NVIDIA GPU")
    
    if nvidia_info:
        analysis['gpu'] = {
            'type': 'NVIDIA',
            'nvidia_smi': nvidia_info,
            'cuda_version': run_command("nvcc --version 2>/dev/null | grep 'release' | grep -o 'V[0-9]*\\.[0-9]*' | cut -d'V' -f2", "Checking CUDA version")
        }
    else:
        # Try for AMD or Intel
        gpu_info = run_command("lspci | grep -i vga", "Checking for other GPU types")
        analysis['gpu'] = {
            'type': 'Other',
            'info': gpu_info
        }
    
    # Storage Information
    console.print("\n[bold blue]💾 Analyzing Storage Devices[/bold blue]")
    disk_info = run_command("df -h", "Getting disk usage information")
    block_devices = run_command("lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE", "Getting block device information")
    
    analysis['storage'] = {
        'disk_usage': disk_info,
        'block_devices': block_devices
    }
    
    # Software Environment
    console.print("\n[bold blue]💻 Scanning Software Environment[/bold blue]")
    analysis['software'] = {
        'shell': os.environ.get('SHELL', ''),
        'python': run_command("python --version 2>&1", "Checking Python version"),
        'node': run_command("node --version 2>/dev/null", "Checking Node.js version"),
        'git': run_command("git --version 2>/dev/null", "Checking Git version"),
        'docker': run_command("docker --version 2>/dev/null", "Checking Docker version"),
        'code_editors': []
    }
    
    # Check for code editors
    console.print("\n[bold blue]📝 Detecting Code Editors[/bold blue]")
    editors = ['code', 'zed', 'cursor', 'vim', 'nano', 'emacs']
    for editor in editors:
        if run_command(f"which {editor} 2>/dev/null", f"Checking for {editor}"):
            analysis['software']['code_editors'].append(editor)
    
    # AI/ML Tools
    console.print("\n[bold blue]🤖 Checking AI/ML Infrastructure[/bold blue]")
    analysis['ai_ml'] = {
        'ollama': run_command("pgrep -f ollama > /dev/null && echo 'Running' || echo 'Not running'", "Checking Ollama service"),
        'conda': run_command("conda --version 2>/dev/null", "Checking Conda"),
        'pip': run_command("pip --version 2>/dev/null", "Checking pip")
    }
    
    # Running Services
    console.print("\n[bold blue]⚙️  Checking Running Services[/bold blue]")
    services = run_command("systemctl list-units --type=service --state=running --no-pager --no-legend | awk '{print $1}' | head -20", "Getting active services")
    analysis['services'] = services.split('\n') if services else []
    
    # Network Information
    console.print("\n[bold blue]🌐 Analyzing Network Configuration[/bold blue]")
    analysis['network'] = {
        'interfaces': run_command("ip addr show | grep '^[0-9]' | awk '{print $2}' | tr -d ':'", "Getting network interfaces"),
        'connections': run_command("ss -tuln | grep LISTEN | wc -l", "Counting listening ports")
    }
    
    # Generate the formatted report
    console.print("\n[bold green]✅ Analysis Complete! Generating Report...[/bold green]\n")
    report = _generate_analysis_report(analysis)
    
    return {
        'success': True,
        'raw_data': analysis,
        'formatted_report': report
    }


def _generate_analysis_report(data: Dict[str, Any]) -> str:
    """Generate a formatted analysis report like Cursor's."""
    
    def format_gpu_info(gpu_data: Dict[str, Any]) -> str:
        """Format GPU information section."""
        if gpu_data.get('type') == 'NVIDIA' and gpu_data.get('nvidia_smi'):
            parts = gpu_data['nvidia_smi'].split(', ')
            if len(parts) >= 6:
                name = parts[0]
                driver = parts[1]
                mem_total = parts[2]
                mem_used = parts[3]
                gpu_util = parts[4]
                power_draw = parts[5]
                power_limit = parts[6] if len(parts) > 6 else "N/A"
                
                return f"""**Graphics - Gaming/AI Ready**
GPU: {name}
Driver: NVIDIA {driver}
CUDA: Version {gpu_data.get('cuda_version', 'Unknown')} support
VRAM Usage: {mem_used}MB / {mem_total}MB ({int(float(mem_used)/float(mem_total)*100) if mem_total and mem_used else 0}% utilized)
GPU Utilization: {gpu_util}%
Power: {power_draw}W / {power_limit}W"""
        else:
            return f"**Graphics**\n{gpu_data.get('info', 'GPU information not available')}"
    
    def format_storage_info(storage_data: Dict[str, Any]) -> str:
        """Format storage information."""
        lines = storage_data.get('disk_usage', '').split('\n')[1:]  # Skip header
        storage_lines = []
        
        for line in lines:
            if line and not line.startswith('tmpfs') and not line.startswith('udev'):
                parts = line.split()
                if len(parts) >= 6:
                    filesystem = parts[0]
                    size = parts[1]
                    used = parts[2]
                    avail = parts[3]
                    use_pct = parts[4]
                    mount = parts[5]
                    
                    if mount == '/':
                        storage_lines.append(f"Primary Storage: {size} (root filesystem at {use_pct} usage - {used} used)")
                    elif '/home' in mount:
                        storage_lines.append(f"Home Storage: {size} ({use_pct} used)")
        
        # Add unmounted devices from lsblk
        block_info = storage_data.get('block_devices', '')
        for line in block_info.split('\n'):
            if 'disk' in line and 'nvme' in line:
                parts = line.split()
                if len(parts) >= 2 and parts[3] == '':  # No mountpoint
                    storage_lines.append(f"Unmounted NVMe: {parts[1]}")
            elif 'disk' in line and ('sd' in line or 'hd' in line):
                parts = line.split()
                if len(parts) >= 2 and parts[3] == '':  # No mountpoint
                    storage_lines.append(f"Unmounted Drive: {parts[1]}")
        
        return "**Storage - Multi-Tier Setup**\n" + "\n".join(storage_lines)
    
    # Start building the report
    report = []
    
    # Title
    report.append("# Linux Machine Analysis")
    report.append("\nBased on comprehensive system analysis, here's a detailed breakdown of your Linux machine:\n")
    
    # System Overview
    uptime_clean = data['system']['uptime'].replace('up ', '')
    report.append("## System Overview")
    report.append(f"**Hostname:** {data['system']['hostname']}")
    report.append(f"**OS:** {data['system']['os_info']}")
    report.append(f"**Kernel:** {data['system']['kernel']}")
    report.append(f"**Architecture:** {data['system']['architecture']}")
    report.append(f"**Uptime:** {uptime_clean}")
    report.append("")
    
    # Hardware Specifications
    report.append("## Hardware Specifications")
    
    # CPU
    cores = data['cpu']['cores']
    threads = data['cpu']['threads']
    load_avg = data['cpu']['load_average']
    
    report.append("### CPU - Performance Analysis")
    report.append(f"**Processor:** {data['cpu']['model']}")
    report.append(f"**Cores:** {cores} physical cores, {threads} threads")
    if load_avg:
        report.append(f"**Load Average:** {load_avg}")
    report.append("")
    
    # Memory
    mem_total = data['memory']['total']
    mem_used = data['memory']['used']
    mem_available = data['memory']['available']
    swap = data['memory']['swap']
    
    report.append("### Memory - Capacity Analysis")
    report.append(f"**Total RAM:** {mem_total}")
    report.append(f"**Used:** {mem_used}")
    report.append(f"**Available:** {mem_available}")
    if swap and swap != "0B":
        report.append(f"**Swap:** {swap}")
    else:
        report.append("**Swap:** Disabled (0B) - Good practice with sufficient RAM")
    report.append("")
    
    # GPU
    if 'gpu' in data:
        report.append("### " + format_gpu_info(data['gpu']))
        report.append("")
    
    # Storage
    if 'storage' in data:
        report.append("### " + format_storage_info(data['storage']))
        report.append("")
    
    # Software Environment
    report.append("## Software Environment")
    
    # Development Tools
    report.append("### Development Tools")
    if data['software']['shell']:
        shell_name = os.path.basename(data['software']['shell'])
        report.append(f"**Shell:** {shell_name}")
    
    if data['software']['python']:
        report.append(f"**Python:** {data['software']['python']}")
    
    if data['software']['node']:
        report.append(f"**Node.js:** {data['software']['node']}")
    
    if data['software']['git']:
        report.append(f"**Git:** {data['software']['git']}")
    
    if data['software']['docker']:
        report.append(f"**Docker:** {data['software']['docker']}")
    else:
        report.append("**Docker:** Not installed")
    
    if data['software']['code_editors']:
        editors = ", ".join(data['software']['code_editors'])
        report.append(f"**Code Editors:** {editors}")
    
    report.append("")
    
    # AI/ML Infrastructure
    if data['ai_ml']['ollama'] == 'Running' or data['ai_ml']['conda'] or data['ai_ml']['pip']:
        report.append("### AI/ML Infrastructure")
        if data['ai_ml']['ollama'] == 'Running':
            report.append("**Ollama:** Running (large language model service)")
        if data['ai_ml']['conda']:
            report.append(f"**Conda:** {data['ai_ml']['conda']}")
        if 'cuda_version' in data.get('gpu', {}):
            report.append("**CUDA Support:** Available for GPU acceleration")
        report.append("")
    
    # Performance Assessment
    report.append("## Performance Assessment")
    
    # Generate recommendations based on the data
    if cores and int(cores) >= 8:
        report.append("✅ **Powerful CPU:** Multi-core processor excellent for development and multitasking")
    
    if mem_total and 'G' in mem_total:
        mem_gb = int(re.findall(r'\d+', mem_total)[0])
        if mem_gb >= 32:
            report.append("✅ **Abundant RAM:** High memory capacity ensures no constraints")
        elif mem_gb >= 16:
            report.append("✅ **Good RAM:** Sufficient memory for most development tasks")
    
    if 'NVIDIA' in data.get('gpu', {}).get('type', ''):
        report.append("✅ **GPU Acceleration:** NVIDIA GPU supports CUDA for AI/ML workloads")
    
    if 'nvme' in data.get('storage', {}).get('block_devices', '').lower():
        report.append("✅ **Fast Storage:** NVMe SSD for optimal performance")
    
    if data['ai_ml']['ollama'] == 'Running':
        report.append("✅ **AI/ML Ready:** Ollama service running for local AI capabilities")
    
    report.append("")
    
    # Current Resource Usage
    report.append("## Current Resource Usage")
    if load_avg:
        avg_vals = load_avg.split(',')
        if avg_vals:
            first_avg = float(avg_vals[0].strip())
            if first_avg < 1.0:
                report.append(f"**CPU Load:** Low ({load_avg.strip()})")
            elif first_avg < 2.0:
                report.append(f"**CPU Load:** Moderate ({load_avg.strip()})")
            else:
                report.append(f"**CPU Load:** High ({load_avg.strip()})")
    
    # Add memory usage percentage if possible
    if mem_used and mem_total:
        try:
            used_num = float(re.findall(r'[\d.]+', mem_used)[0])
            total_num = float(re.findall(r'[\d.]+', mem_total)[0])
            usage_pct = int((used_num / total_num) * 100)
            report.append(f"**Memory:** {usage_pct}% used ({mem_used} of {mem_total})")
        except:
            report.append(f"**Memory:** {mem_used} used of {mem_total}")
    
    report.append("")
    
    # Recommendations
    report.append("## Recommendations")
    
    if data['software']['docker'] == '':
        report.append("• Consider installing Docker for containerized development")
    
    if swap == "0B" and mem_total:
        mem_gb = int(re.findall(r'\d+', mem_total)[0]) if re.findall(r'\d+', mem_total) else 0
        if mem_gb < 16:
            report.append("• Consider enabling swap for additional memory buffer")
    
    if data['ai_ml']['ollama'] == 'Running':
        report.append("• Monitor GPU VRAM usage when running multiple AI models")
    
    # Check for unmounted drives
    if 'unmounted' in data.get('storage', {}).get('block_devices', '').lower():
        report.append("• Consider mounting additional drives for expanded storage")
    
    report.append("• Ensure regular system updates and backups")
    report.append("")
    
    report.append("Your machine appears well-configured for development work and AI/ML tasks with modern hardware and a clean Linux setup.")
    
    return "\n".join(report)