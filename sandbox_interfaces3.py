import requests
import json
USER = 'admin'
PASS = 'C1sco12345'

requests.packages.urllib3.disable_warnings()

url = "https://devnetsandboxiosxe.cisco.com:443/restconf/data/ietf-interfaces:interfaces"


payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback150",
        "description": "[Link3 loopback interface]",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.1.1.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

headers = {  
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json'
}

response = requests.request("POST", url, auth=(USER, PASS), headers=headers, data=json.dumps(payload), verify=False)

print(response.text)
