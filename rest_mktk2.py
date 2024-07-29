from requests.auth import HTTPBasicAuth
import requests
import json

username = 'rakib'
password = '1234'
url = 'http://10.248.27.226/rest'

# আমাদের রিকোয়েস্ট যাচ্ছে MikroTik API তে
response = requests.get(url + '/system/resource', auth=HTTPBasicAuth(username, password), verify=False)
resources = response.json()
 
# Check and print the CPU Load and Free Memory
cpu_load = resources.get('cpu-load', 'N/A')
free_memory = resources.get('free-memory', 'N/A')
print(f"CPU Load: {cpu_load}%")
print(f"Free Memory: {free_memory} bytes")
