import requests
import socket
import dns.resolver
import ssl
import websockets
import asyncio

# Additional imports for extended discovery
import json
import re
import bs4  # BeautifulSoup for HTML parsing
import scapy.all as scapy  # For network packet analysis
import bluetooth  # For Bluetooth scanning

def get_user_input():
    #Prompt user for an IP address or domain.
    return input("Enter an IP address or domain name: ").strip()

def adapt_http_if_needed(url):
    #Prefaces function to start with HTTP, and use HTTPS only if necessary.
    if request_http(url):
        return url  # Stay with HTTP
    elif request_https(url):
        return f"https://{url}"  # Use HTTPS only when HTTP fails
    return url  # Keep original if neither worked

def request_http(url):
    #Attempt HTTP request, with API/CDN discovery.
    try:
        response = requests.get(f"http://{url}", timeout=5)
        print(f"HTTP Request Success: {response.status_code}")
        discover_http(url, response)  # Apply enhanced discovery
        return True
    except requests.RequestException as e:
        print(f"HTTP Request Failed: {e}")
        return False

def request_https(url):
    #Attempt HTTPS request, with API/CDN discovery.
    try:
        response = requests.get(f"https://{url}", timeout=5, verify=True)
        print(f"HTTPS Request Success: {response.status_code}")
        discover_http(url, response)  # Apply enhanced discovery
        return True
    except requests.RequestException as e:
        print(f"HTTPS Request Failed: {e}")
        return False

def request_srv_alpn(domain):
    #Attempt SRV & ALPN resolution.
    try:
        srv_records = dns.resolver.resolve(f"_http._tcp.{domain}", "SRV")
        for srv in srv_records:
            print(f"SRV Record Found: {srv.target}:{srv.port}")
            return True
    except dns.resolver.NoAnswer:
        print("No SRV record found.")
    except dns.resolver.NXDOMAIN:
        print("Domain does not exist.")
    except Exception as e:
        print(f"SRV Lookup Failed: {e}")
    
    # Try ALPN
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssl_sock:
                print(f"ALPN Negotiated Protocol: {ssl_sock.selected_alpn_protocol()}")
                return True
    except Exception as e:
        print(f"ALPN Negotiation Failed: {e}")

    return False

async def request_websockets(url):
    #Attempt WebSocket connection.
    try:
        async with websockets.connect(f"wss://{url}") as ws:
            print("WebSocket Connection Established")
            return True
    except Exception as e:
        print(f"WebSocket Connection Failed: {e}")
        return False

def discover_http(url, response):
    #Determines response type, available APIs, CDN use, and HTTP methods.
    try:
        headers = response.headers
        content_type = headers.get("Content-Type", "").lower()

        # Determine content type
        if "text/html" in content_type:
            print("Response Type: **HTML**")
            analyze_dom(response.text)  # Call DOM analysis function
        elif "application/json" in content_type:
            print("Response Type: **JSON**")
        elif "application/octet-stream" in content_type or "image/" in content_type or "application/pdf" in content_type:
            print("Response Type: **Binary Data**")
        else:
            print("Response Type: **Unknown**")

        # Detect API sources
        detect_api(headers)

        # Detect CDN presence
        detect_cdn(headers)

        # Determine HTTP methods
        detect_http_methods(url)

    except Exception as e:
        print(f"Discovery Process Failed: {e}")

def analyze_dom(html):
    #Extracts information from webpage DOM for API endpoints, hidden fields, JavaScript.
    pass  # Use BeautifulSoup to parse HTML, extract scripts, forms, links.

def detect_api(headers):
    #Check headers for API-related information.
    pass  # Look for API indicators like X-API-Version, Link, CORS headers.

def detect_cdn(headers):
    #Identify CDN presence via HTTP headers.
    pass  # Analyze headers like Server, CF-Cache-Status, X-Cache.

def detect_http_methods(url):
    #Determine supported HTTP methods using OPTIONS request.
    pass  # Send OPTIONS request and extract 'Allow' header.

def detect_local_network():
    #Discover local network devices using mDNS, DHCP, VLAN, and passive sniffing.
    pass  # Use avahi/mDNS, DHCP analysis, VLAN scanning.

def active_network_scan():
    #Perform ARP scanning, port scanning, traceroute analysis, and packet sniffing.
    pass  # Use scapy/nmap for scanning open ports, running traceroutes.

def wireless_signal_analysis():
    #Scan for WiFi signal strength, hidden SSIDs, and Bluetooth devices.
    pass  # Use WiFi SSID scanning, probe requests, Bluetooth scanning.

def main():
    #Main function to process user input and attempt connections.
    url = get_user_input()
    
    # Ensure we only use HTTPS if necessary
    adapted_url = adapt_http_if_needed(url)

    if request_http(adapted_url):
        return
    elif request_https(adapted_url):
        return
    elif request_srv_alpn(url):
        return
    else:
        print("Trying WebSocket...")
        asyncio.run(request_websockets(url))

    # Additional discovery features
    print("\nStarting Extended Discovery...\n")
    detect_local_network()  # Check for local network services
    active_network_scan()  # Run active network scans
    wireless_signal_analysis()  # Scan for WiFi/Bluetooth proximity-based discovery

if __name__ == "__main__":
    main()

#NEED TO: Adapt CMS specific handling into the model above
"""
class CMSDataHandler:
    def __init__(self, dataset_id):
        self.dataset_id = dataset_id
        self.data = None
    
    def fetch_data(self):
        #Fetch JSON data from CMS API.
        url = f"https://data.cms.gov/provider-data/api/v1/dataset/{self.dataset_id}/items"
        response = requests.get(url)
        if response.status_code == 200:
            self.data = response.json()
            return self.data
        else:
            print(f"Error: {response.status_code}")
            return None

    def save_data(self, filename="data.json"):
        #Save JSON data to a file.
        if self.data:
            with open(filename, "w") as f:
                json.dump(self.data, f, indent=2)
            print(f"Data saved to {filename}")

    def load_data(self, filename="data.json"):
        #Load JSON data from a file.
        with open(filename, "r") as f:
            self.data = json.load(f)
        print("Data loaded successfully.")

    def filter_data(self, key, value):
        #Filter data by a key-value pair.
        if not self.data:
            print("No data loaded.")
            return []
        
        return [entry for entry in self.data if entry.get(key) == value]

    def perform_action(self, action_type):
        #Dynamically perform an action based on user-defined choice.
        if action_type == "filter":
            key = input("Enter the key to filter by: ")
            value = input("Enter the value to match: ")
            filtered = self.filter_data(key, value)
            print(json.dumps(filtered, indent=2))
        elif action_type == "summary":
            self.print_summary()
        elif action_type == "save":
            self.save_data()
        else:
            print("Unknown action.")

    def print_summary(self):
        #Provide a summary of the dataset.
        if not self.data:
            print("No data available.")
            return
        
        total_entries = len(self.data)
        sample_entry = self.data[0] if total_entries > 0 else {}
        print(f"Total entries: {total_entries}")
        print("Sample Entry Keys:", list(sample_entry.keys()))

# Example usage
handler = CMSDataHandler("your_dataset_id_here")
handler.fetch_data()
handler.perform_action("summary")  # This allows ambiguity by letting the user define the action

# For further detail visit the CMS API reference at:
#https://data.cms.gov/provider-data/docs
"""
