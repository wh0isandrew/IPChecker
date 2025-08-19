# AbuseIPDB IP Checker & HTML Report Generator

A simple Python script to check a list of IP addresses against the AbuseIPDB API and generate a clean, self-contained HTML report.

## Features

- Reads a list of IP addresses from a text file (`.txt`).
- Queries the AbuseIPDB API for details on each IP
- Generates a self-contained HTML report
- Stylish dark-mode theme for easy reading
- Color-coded abuse confidence scores (Green, Yellow, Red) for quick threat assessment

## Requirements

- Python 3
- `requests` library
- An AbuseIPDB API key.

## Setup & Usage

### 1. Clone or Download

Get the project files onto your computer. You should have at least:
- `IPChecker.py`

### 2. Install Dependencies

Open your terminal or command prompt and run:
```bash
pip install requests
```

### 3. Create an IP List

In the same project directory, create a file named `ips.txt`. Add one IP address per line, for example:

```text
8.8.8.8
8.8.4.4
1.1.1.1
```

### 4. Run the Script

Execute the script from your terminal:
```bash
python ip_checker.py
```

The script will then prompt you to:
1.  Enter your AbuseIPDB API key.
2.  Specify the name of your IP list file (e.g., `ips.txt`).
3.  Provide a filename for the HTML report (e.g., `report.html`).

## Output

After the script finishes, you’ll find an HTML file (e.g., `report.html`) in your project directory. Open it in any web browser to view a detailed report with a card for each IP address, showing:

- Country
- ISP
- Domain
- Abuse Confidence Score (with color-coding)
