import requests
USER = 'admin'
PASS = 'C1sco12345'

requests.packages.urllib3.disable_warnings()

# url = "https://devnetsandboxiosxe.cisco.com:443/restconf/data/ietf-interfaces:interfaces"
url = "https://devnetsandboxiosxe.cisco.com:443/restconf/data/Cisco-IOS-XE-native:native/interface"

response = requests.request("GET", url, auth=(USER, PASS), verify=False)

print(response.text)
