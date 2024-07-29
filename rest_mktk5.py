from requests.auth import HTTPBasicAuth
import requests
import json

# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings()

# Authentication details
username = 'rakib'
password = '1234'
base_url = 'https://10.248.27.226/rest'

# Endpoint to add IP addresses
ip_address_url = f"{base_url}/ip/address"

# Static IP address data to be sent as payload
static_ip_addresses = [
    {"address": "192.168.99.2/24", "interface": "lo"},
    {"address": "172.16.5.1/24", "interface": "ether3"},
    {"address": "172.16.6.1/24", "interface": "ether4"},
    {"address": "172.16.7.1/24", "interface": "ether3"},
    {"address": "10.248.27.226/24", "interface": "ether2"},
    {"address": "192.168.111.111/32", "interface": "lo"}
]

# Send each IP address data individually
for ip in static_ip_addresses:
    headers = {'Content-Type': 'application/json'}
    response = requests.put(ip_address_url, json=ip, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    if response.status_code in [200, 201]:  # Both 200 and 201 could indicate success
        print(f"Successfully added IP Address: {ip['address']}")
    else:
        print(f"Failed to add IP Address: {ip['address']}. Status code: {response.status_code}")
        print("Response Text:", response.text)  # Print the response body for more details