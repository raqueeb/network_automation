import requests
requests.packages.urllib3.disable_warnings()

USER = 'admin'
PASS = 'C1sco12345'

uri = 'https://devnetsandboxiosxe.cisco.com:443/restconf/data/Cisco-IOS-XE-native:native/hostname'

headers = {
      "Accept" : "application/yang-data+json"
   }

response = requests.get(
    url=uri,
    headers=headers,
    auth=(USER, PASS),
    verify=False)
    
print(response.json())