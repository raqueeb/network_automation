from requests.auth import HTTPBasicAuth
import requests

# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings()

# Authentication details
username = 'rakib'
password = '1234'
base_url = 'https://10.248.27.226/rest'

# নতুন ফায়ারওয়াল নিয়ম যোগ করা
web_rule = {
    "chain": "input",
    "protocol": "tcp",
    "dst-port": "80",
    "action": "accept",
    "comment": "Allow HTTP"
}
response = requests.post(base_url+'/ip/firewall/filter/add', json=web_rule, auth=HTTPBasicAuth(username, password), verify=False)
print(response.text)