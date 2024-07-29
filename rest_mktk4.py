from requests.auth import HTTPBasicAuth
import requests
import json

# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings()

# Authentication details
username = 'rakib'
password = '1234'
base_url = 'https://10.248.27.226/rest'

# Endpoint to print IP addresses
ip_address_url = f"{base_url}/ip/address"

# Make the POST request to print IP addresses
ip_response = requests.get(ip_address_url, auth=HTTPBasicAuth(username, password), verify=False)

print("Response Text:", ip_response.text)  # Print the response body for more details
