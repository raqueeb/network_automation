import requests
USER = 'admin'
PASS = 'C1sco12345'

requests.packages.urllib3.disable_warnings()

url = "https://devnetsandboxiosxe.cisco.com:443/restconf/data/ietf-interfaces:interfaces/interface=Loopback150"

payload = {}
headers = {
  'Content-Type': 'application/yang-data+json',
  'Accept': 'application/yang-data+json',
}

response = requests.request("DELETE", url, auth=(USER, PASS), headers=headers, data=payload, verify=False)

print(response.text)
