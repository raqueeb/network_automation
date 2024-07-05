import requests
import json

USER = 'admin'
PASS = 'C1sco12345'

requests.packages.urllib3.disable_warnings()

uri = 'https://devnetsandboxiosxe.cisco.com:443/restconf/data/Cisco-IOS-XE-native:native/hostname'

headers = {
      "Content-Type": "application/yang-data+json"
   }

payload = {
  "hostname": "Link3_Test"
}

response = requests.put(
    url=uri, headers=headers, 
    data=json.dumps(payload), 
    auth=(USER, PASS), 
    verify=False)

print(response)