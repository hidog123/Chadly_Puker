import os
import re
from bs4 import BeautifulSoup

# File patterns and constants
html_pattern = re.compile(r'result\d+\.html')
final_html = "final.html"
result1337_html = "result1337.html"
nodata_file = "urls.txt"
lasturl_file = "lasturl.txt"

# Result containers
unique_results = set()
no_data_links = []

# HTML template for final output
final_html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Consolidated Results</title>
    <style>
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        th {{
            background-color: #f2f2f2;
            text-align: left;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f1f1f1;
        }}
    </style>
</head>
<body>
    <h1>Consolidated Results</h1>
    <table>
        <thead>
            <tr>
                <th>URL</th>
                <th>Extracted Data</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</body>
</html>
"""

def process_html_file(file_path):
    global unique_results, no_data_links

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        rows = soup.select("table tbody tr")
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                url = cols[0].text.strip()
                data = cols[1].decode_contents().strip()  # To get raw HTML content
                split_data = [line.strip() for line in data.replace('<br>', '\n').split('\n') if line.strip()]
                
                if "No Data Found" in split_data:
                    no_data_links.append(url)
                else:
                    for line in split_data:
                        unique_results.add((url, line))

def write_final_html():
    rows = "\n".join(
        f"<tr><td>{url}</td><td>{data}</td></tr>"
        for url, data in sorted(unique_results)
    )
    html_content = final_html_template.format(rows=rows)

    # Save to final.html
    with open(final_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Results saved to {final_html}.")

    # Save to result1337.html
    with open(result1337_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Results saved to {result1337_html}.")

def write_nodata_file():
    with open(nodata_file, 'w', encoding='utf-8') as f:
        for url in sorted(no_data_links):
            f.write(url + "\n")

def handle_lasturl():
    # Check if `lasturl.txt` exists and read its contents
    if os.path.exists(lasturl_file):
        with open(lasturl_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        
        # Check if these URLs still have "No Data Found"
        for url in urls:
            if url in no_data_links:
                no_data_links.remove(url)
            else:
                # Delete the URL if it doesn't have data anymore
                urls.remove(url)
        
        # Overwrite `lasturl.txt` with the updated list
        with open(lasturl_file, 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(url + "\n")
    
    # Add the first 10 lines from `nodata.txt` to `lasturl.txt`
    if no_data_links:
        with open(lasturl_file, 'w', encoding='utf-8') as f:
            for url in no_data_links[:10]:
                f.write(url + "\n")
        no_data_links[:] = no_data_links[10:]

def main():
    # Process all result[number].html files
    for file_name in os.listdir('.'):
        if html_pattern.match(file_name):
            process_html_file(file_name)

    # Write consolidated HTML
    write_final_html()
    
    # Write no data links to file
    write_nodata_file()
    
    # Handle lasturl file
    handle_lasturl()

    print(f"Processing complete! Check '{final_html}', '{result1337_html}', '{nodata_file}', and '{lasturl_file}'.")

if __name__ == "__main__":
    main()
