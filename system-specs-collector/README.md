# System Specs Collector v1.0

A comprehensive and user-friendly Python tool to collect detailed system information including CPU, memory, disk, GPU, and OS specs.

## 📦 Features

- CPU information (cores, frequency, usage)
- Memory usage
- Disk partitions and usage
- Operating System details
- GPU stats (requires `GPUtil`)
- Output to JSON, CSV, or human-readable text

## ⚙️ Requirements

- Python 3.6+
- [psutil](https://pypi.org/project/psutil/)
- Optional: [GPUtil](https://pypi.org/project/GPUtil/) (for GPU information)

Install dependencies using pip:

```bash
pip install psutil GPUtil
```

## 🚀 Usage

```bash
python3 system_specs.py [-f FORMAT] [-o OUTPUT]
```

### Arguments

- `-f`, `--format`: Output format. Choose from `text` (default), `json`, or `csv`
- `-o`, `--output`: Output file name (without extension)
- `-v`, `--version`: Show script version

### Examples

```bash
# Human-readable output (default)
python3 system_specs.py

# Save output as JSON
python3 system_specs.py -f json -o my_system_info

# Save output as CSV
python3 system_specs.py -f csv -o my_system_info
```

## 📊 Output Details

- **JSON**: Full nested structure of the collected data.
- **CSV**: Flattened key-value pairs.
- **Text**: Formatted summary printed on the console.

## 💡 Notes

- GPU info is only available if `GPUtil` is installed and a compatible GPU is detected.
- All time and values are captured at the point of script execution.

## 👍 License

MIT License

---

**Author**: aabhinavg1
**Version**: 1.0.0  
**Created**: 2025

