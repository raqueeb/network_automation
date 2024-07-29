from ncclient import manager

model = manager.connect(host='devnetsandboxiosxe.cisco.com',
                    port=830,
                    username='admin',
                    password='C1sco12345',
                    hostkey_verify=False,
                    device_params={'name':'iosxe'})

    # XML RPC call as a string
config_data = """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <route>
            <ip-route-interface-forwarding-list>
              <prefix>192.168.1.0</prefix>
              <mask>255.255.255.0</mask>
              <fwd-list>
                <fwd>10.1.111.1</fwd>
              </fwd-list>
            </ip-route-interface-forwarding-list>
          </route>
        </ip>
      </native>
    </config>
    """
# Apply the config change
reply = model.edit_config(target="running", config=config_data)
print(reply)
model.close_session()
