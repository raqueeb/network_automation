from ncclient import manager

model = manager.connect(host='devnetsandboxiosxe.cisco.com',
                    port=830,
                    username='admin',
                    password='C1sco12345',
                    hostkey_verify=False,
                    device_params={'name':'iosxe'})

config_data = """
<config>
	<native
		xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
		<hostname>Link3_Test2</hostname>
	</native>
</config>"""

reply = model.edit_config(config_data,  target = 'running')
print(reply)
model.close_session()