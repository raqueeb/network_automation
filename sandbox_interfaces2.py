import requests
USER = 'admin'
PASS = 'C1sco12345'

requests.packages.urllib3.disable_warnings()

# set REST API headers
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

url = "https://devnetsandboxiosxe.cisco.com:443/restconf/data/ietf-interfaces:interfaces"

response = requests.request("GET", url, auth=(USER, PASS), headers=headers, verify=False)

print(response.text)
