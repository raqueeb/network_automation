from requests.auth import HTTPBasicAuth
import requests

# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings()

# Authentication details
username = 'rakib'
password = '1234'
base_url = 'https://10.248.27.226/rest'

# নতুন ব্যবহারকারী তৈরি
new_user = {
    "name": "rhassan",
    "password": "securepass123",
    "group": "full"
}
response = requests.post(base_url+'/user/add', json=new_user, auth=HTTPBasicAuth(username, password), verify=False)
print(response.text)