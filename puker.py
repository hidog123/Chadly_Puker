from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
import time  # Import time for adding delays


# File paths
js_file_path = "script.js"  # Path to the JavaScript file
url_file_path = "urls.txt"  # Path to the file containing URLs
output_html_path = "result7.html"
# Function to execute JavaScript in the browser console on links
def execute_js_in_console(js_code, url_list, delay=10):
    # Configure Chrome WebDriver
    chrome_options = Options()
    # Remove the headless mode argument to show the browser window
    #chrome_options.add_argument("--headless")  # This line is removed for visible Chrome instance
    chrome_options.add_argument("--disable-gpu")  # Disable GPU usage (optional)
    chrome_options.add_argument("--no-sandbox")  # Useful for some Linux environments
    service = Service()  # Ensure the chromedriver executable is in PATH or specify the location
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.implicitly_wait(10)  # Adjust implicit wait for Selenium interactions
    results = {}
    
    # Process each URL
    for url in url_list:
        try:
            driver.get(url)
            print(f"Processing URL: {url}")
            time.sleep(delay)  # Wait for the page to fully load and for the JS code to execute
            # Execute JavaScript in the browser's console using execute_script
            driver.execute_script(f"console.log('Executing JS code on {url}'); {js_code}")
            
            # Optionally, wait some more time if necessary
            time.sleep(delay)

            # After executing JS, get the HTML response (the modified DOM)
            html_response = driver.execute_script("return document.documentElement.outerHTML;")
            extracted_data = re.findall(r'(?<=<br>)(.*?)(?=<br>)', html_response)

            results[url] = extracted_data
        except Exception as e:
            print(f"Error processing {url}: {e}")
            results[url] = None

    driver.quit()
    return results

# Read JavaScript code from file
try:
    with open(js_file_path, 'r') as file:
        javascript_code = file.read()
except FileNotFoundError:
    print(f"Error: JavaScript file '{js_file_path}' not found.")
    exit()

# Read URLs from file
try:
    with open(url_file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"Error: URLs file '{url_file_path}' not found.")
    exit()

# Execute the function with a longer delay (e.g., 15 seconds)
output = execute_js_in_console(javascript_code, urls, delay=15)
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Extracted Results</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
            text-align: left;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
</head>
<body>
    <h1>Extracted Results</h1>
    <table>
        <thead>
            <tr>
                <th>URL</th>
                <th>Extracted Data</th>
            </tr>
        </thead>
        <tbody>
"""

# Populate the table rows with data
for url, data in output.items():
    html_content += f"<tr><td>{url}</td><td>{'<br>'.join(data) if data else 'No Data Found'}</td></tr>"
    
# Close the HTML table and body
html_content += """
        </tbody>
    </table>
</body>
</html>
"""

# Save the HTML file
with open(output_html_path, 'w') as file:
    file.write(html_content)

print(f"Results saved to {output_html_path}")
