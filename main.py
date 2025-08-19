import requests
import os


def check_ip(api_key, ip_address, max_age=90):
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': str(max_age)
    }
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    try:
        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        response.raise_for_status()
        decoded_response = response.json()
        return decoded_response.get('data')
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for IP {ip_address}: {http_err}")
        if response.status_code in [401, 403]:
            print("Error: Invalid or unauthorized API key. Please check your key.")
        elif response.status_code == 429:
            print("Error: API rate limit exceeded. Please wait and try again later.")
        else:
            print(f"Error details: {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred while checking IP {ip_address}: {err}")
    return None


def generate_html_report(results_list):
    html_style = """
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #121212;
            color: #e0e0e0;
        }
        h1 { 
            color: #ffffff;
            text-align: center;
            margin-bottom: 30px;
        }
        .container { 
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }
        .ip-card { 
            background-color: #1e1e1e; 
            border: 1px solid #333; 
            border-radius: 8px; 
            padding: 20px; 
            width: 320px; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            transition: transform 0.2s ease-in-out;
        }
        .ip-card:hover {
            transform: translateY(-5px);
        }
        .ip-card h2 { 
            margin-top: 0;
            font-size: 1.5em;
            color: #4a90e2;
            word-wrap: break-word;
        }
        .ip-card p { 
            margin: 8px 0;
            line-height: 1.5;
        }
        .score { 
            font-weight: bold;
            font-size: 1.1em;
            padding: 3px 8px;
            border-radius: 5px;
            color: white;
        }
        .score-low { background-color: #28a745; }
        .score-mid { background-color: #ffc107; color: #121212; }
        .score-high { background-color: #dc3545; }
    </style>
    """
    html_content = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>AbuseIPDB Report</title>{html_style}</head><body>"
    html_content += "<h1>AbuseIPDB IP Address Report</h1><div class='container'>"

    for data in results_list:
        score = data.get('abuseConfidenceScore', 0)
        score_class = 'score-low'
        if 40 <= score <= 75:
            score_class = 'score-mid'
        elif score > 75:
            score_class = 'score-high'

        ip_address = data.get('ipAddress', 'N/A')
        country = data.get('countryCode', 'N/A')
        isp = data.get('isp', 'N/A')
        domain = data.get('domain', 'N/A')
        usage_type = data.get('usageType', 'N/A')
        total_reports = data.get('totalReports', 'N/A')

        html_content += f"""
        <div class="ip-card">
            <h2>{ip_address}</h2>
            <p><strong>Country:</strong> {country}</p>
            <p><strong>ISP:</strong> {isp}</p>
            <p><strong>Domain:</strong> {domain}</p>
            <p><strong>Usage Type:</strong> {usage_type}</p>
            <p><strong>Total Reports:</strong> {total_reports}</p>
            <p><strong>Abuse Score:</strong> <span class="score {score_class}">{score}%</span></p>
        </div>
        """
    html_content += "</div></body></html>"
    return html_content


def main():
    api_key = input("Enter your AbuseIPDB API key: ").strip()
    if not api_key:
        print("API key is required. Exiting.")
        return

    filename = input("Enter the name of the .txt file with IP addresses (e.g., ips.txt): ").strip()
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return

    try:
        with open(filename, 'r') as f:
            ips_to_check = set(line.strip() for line in f if line.strip())
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return

    if not ips_to_check:
        print("No IP addresses found in the file.")
        return

    print(f"\nFound {len(ips_to_check)} unique IP(s) to check. Querying API...")

    all_results = []
    for ip in ips_to_check:
        print(f"  - Checking {ip}...")
        data = check_ip(api_key, ip)
        if data:
            all_results.append(data)

    print("Finished checking all IPs.")

    if all_results:
        output_filename = input("Enter the output filename for the HTML report (e.g., report.html): ").strip()
        if not output_filename.endswith('.html'):
            output_filename += '.html'

        print(f"Generating HTML report...")
        html_report = generate_html_report(all_results)

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_report)
            print(f"\nSuccessfully saved report to '{output_filename}'")
        except Exception as e:
            print(f"Error saving HTML file: {e}")
    else:
        print("No data was retrieved, so no report was generated.")


if __name__ == "__main__":
    main()