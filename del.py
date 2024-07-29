from requests.auth import HTTPBasicAuth
import requests
import json

requests.packages.urllib3.disable_warnings()

username = 'rakib'
password = '1234'
url = 'https://10.248.27.226/rest'

new_queue = {
       "name": "Home_Client",
       "target": "192.168.1.100/32",
       "max-limit": "5M/5M"
   }

response = requests.post(url+'/queue/simple', json=new_queue, auth=HTTPBasicAuth(username, password), verify=False)

# Print response status and content for debugging
print(f"Status Code: {response.status_code}")
print(f"Response Content: {response.content.decode('utf-8')}")

