from requests.auth import HTTPBasicAuth
import requests
import json

username = 'rakib' 
password = '1234'
url = 'http://10.248.27.226/rest' 

response = requests.get(url+'/interface', auth=HTTPBasicAuth(username, password), verify=False)
print(json.dumps(response.json(), indent=4))
