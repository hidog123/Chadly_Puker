from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time  # Import time for adding delays

# File paths
js_file_path = "script.js"  # Path to the JavaScript file
url_file_path = "urls.txt"  # Path to the file containing URLs

# Function to execute JavaScript in the browser console on links
def execute_js_in_console(js_code, url_list, delay=10):
    # Configure Chrome WebDriver
    chrome_options = Options()
    # Remove the headless mode argument to show the browser window
    # chrome_options.add_argument("--headless")  # This line is removed for visible Chrome instance
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
            results[url] = html_response
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
print("Results:")
print(output)
with open(output_file_path, 'w') as file:
    file.write(str(table))

print(f"Results saved to {output_file_path}")
