#!/usr/bin/env python3
"""
System Specs Collector v1.0
A comprehensive tool to gather hardware and software specifications.
"""

import platform
import psutil
import csv
import argparse
from datetime import datetime
from typing import Dict, List, Union
import json

try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

__version__ = "1.0.0"

def flatten_dict(d: Dict, parent_key: str = '', sep: str = ': ') -> Dict:
    """Flatten a nested dictionary structure."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key} [{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key} [{i}]", item))
        else:
            items.append((new_key, v))
    return dict(items)

def get_cpu_info() -> Dict:
    """Collect detailed CPU information."""
    try:
        freq = psutil.cpu_freq()
        return {
            "Physical cores": psutil.cpu_count(logical=False),
            "Total cores": psutil.cpu_count(logical=True),
            "Max Frequency (MHz)": freq.max if freq else "N/A",
            "Min Frequency (MHz)": freq.min if freq else "N/A",
            "Current Frequency (MHz)": freq.current if freq else "N/A",
            "CPU Usage per Core (%)": psutil.cpu_percent(percpu=True, interval=1),
            "Total CPU Usage (%)": psutil.cpu_percent(interval=1)
        }
    except Exception as e:
        return {"Error": f"Failed to get CPU info: {str(e)}"}

def get_memory_info() -> Dict:
    """Collect memory/RAM information."""
    try:
        svmem = psutil.virtual_memory()
        return {
            "Total (GB)": round(svmem.total / (1024 ** 3), 2),
            "Available (GB)": round(svmem.available / (1024 ** 3), 2),
            "Used (GB)": round(svmem.used / (1024 ** 3), 2),
            "Percentage (%)": svmem.percent
        }
    except Exception as e:
        return {"Error": f"Failed to get memory info: {str(e)}"}

def get_disk_info() -> List[Dict]:
    """Collect disk/partition information."""
    disk_data = []
    try:
        partitions = psutil.disk_partitions()
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                disk_data.append({
                    "Device": p.device,
                    "Mountpoint": p.mountpoint,
                    "File system type": p.fstype,
                    "Total Size (GB)": round(usage.total / (1024 ** 3), 2),
                    "Used (GB)": round(usage.used / (1024 ** 3), 2),
                    "Free (GB)": round(usage.free / (1024 ** 3), 2),
                    "Percentage (%)": usage.percent
                })
            except Exception as e:
                disk_data.append({
                    "Device": p.device,
                    "Error": f"Failed to read partition: {str(e)}"
                })
    except Exception as e:
        disk_data.append({"Error": f"Failed to get disk info: {str(e)}"})
    return disk_data

def get_os_info() -> Dict:
    """Collect operating system information."""
    try:
        return {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor()
        }
    except Exception as e:
        return {"Error": f"Failed to get OS info: {str(e)}"}

def get_gpu_info() -> List[Dict]:
    """Collect GPU information if available."""
    if not HAS_GPU:
        return [{"Info": "GPUtil package not installed"}]
    
    try:
        gpus = GPUtil.getGPUs()
        gpu_list = []
        for gpu in gpus:
            gpu_list.append({
                "ID": gpu.id,
                "Name": gpu.name,
                "Driver Version": gpu.driver,
                "Memory Total (MB)": gpu.memoryTotal,
                "Memory Used (MB)": gpu.memoryUsed,
                "Memory Free (MB)": gpu.memoryFree,
                "Load (%)": round(gpu.load * 100, 1),
                "Temperature (°C)": gpu.temperature
            })
        return gpu_list if gpus else [{"Info": "No GPUs detected"}]
    except Exception as e:
        return [{"Error": f"Failed to get GPU info: {str(e)}"}]

def collect_all_info() -> Dict:
    """Collect all system information."""
    return {
        "Timestamp": datetime.now().isoformat(),
        "Version": __version__,
        "OS Info": get_os_info(),
        "CPU Info": get_cpu_info(),
        "Memory Info": get_memory_info(),
        "Disk Info": get_disk_info(),
        "GPU Info": get_gpu_info()
    }

def save_to_csv(data: Dict, filename: str) -> None:
    """Save collected data to CSV file."""
    try:
        flat_data = flatten_dict(data)
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Property", "Value"])
            for key, value in flat_data.items():
                writer.writerow([key, value])
        print(f"✅ Successfully saved to {filename}")
    except Exception as e:
        print(f"❌ Failed to save CSV: {str(e)}")

def save_to_json(data: Dict, filename: str) -> None:
    """Save collected data to JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)
        print(f"✅ Successfully saved to {filename}")
    except Exception as e:
        print(f"❌ Failed to save JSON: {str(e)}")

def print_human_readable(data: Dict) -> None:
    """Print human-readable system information."""
    print(f"\nSystem Specs Collector v{data.get('Version', '1.0.0')}")
    print("=" * 50)
    print(f"Timestamp: {data.get('Timestamp')}")
    
    # OS Info
    os_info = data.get('OS Info', {})
    print("\nOperating System:")
    print(f"  System: {os_info.get('System', 'N/A')}")
    print(f"  Version: {os_info.get('Version', 'N/A')}")
    print(f"  Machine: {os_info.get('Machine', 'N/A')}")
    
    # CPU Info
    cpu_info = data.get('CPU Info', {})
    print("\nCPU Information:")
    print(f"  Physical Cores: {cpu_info.get('Physical cores', 'N/A')}")
    print(f"  Total Cores: {cpu_info.get('Total cores', 'N/A')}")
    print(f"  Current Frequency: {cpu_info.get('Current Frequency (MHz)', 'N/A')} MHz")
    print(f"  Total Usage: {cpu_info.get('Total CPU Usage (%)', 'N/A')}%")
    
    # Memory Info
    mem_info = data.get('Memory Info', {})
    print("\nMemory Information:")
    print(f"  Total: {mem_info.get('Total (GB)', 'N/A')} GB")
    print(f"  Used: {mem_info.get('Used (GB)', 'N/A')} GB ({mem_info.get('Percentage (%)', 'N/A')}%)")
    
    # GPU Info
    gpu_info = data.get('GPU Info', [{}])[0]
    if 'Name' in gpu_info or 'ID' in gpu_info:
        print("\nGPU Information:")
        print(f"  Name: {gpu_info.get('Name', 'N/A')}")
        print(f"  Memory: {gpu_info.get('Memory Used (MB)', 'N/A')}/{gpu_info.get('Memory Total (MB)', 'N/A')} MB")
        print(f"  Load: {gpu_info.get('Load (%)', 'N/A')}%")

def main():
    parser = argparse.ArgumentParser(
        description="System Specs Collector - Gather comprehensive system information",
        epilog="Example: system_specs.py -f json -o system_info"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["csv", "json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "-o", "--output",
        default="system_specs",
        help="Output filename without extension (default: system_specs)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"System Specs Collector v{__version__}"
    )
    
    args = parser.parse_args()
    data = collect_all_info()
    
    if args.format == "csv":
        save_to_csv(data, f"{args.output}.csv")
    elif args.format == "json":
        save_to_json(data, f"{args.output}.json")
    else:
        print_human_readable(data)

if __name__ == "__main__":
    main()