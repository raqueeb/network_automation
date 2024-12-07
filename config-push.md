
```bash
# প্রথমে একটা নতুন ফোল্ডার বানাই
mkdir network_automation
cd network_automation

# পাইথন ভার্চুয়াল এনভায়রনমেন্ট সেটআপ
python -m venv venv
source venv/bin/activate  # লিনাক্স/ম্যাকের জন্য
# অথবা 
.\venv\Scripts\activate  # উইন্ডোজের জন্য

# প্রয়োজনীয় প্যাকেজ ইনস্টল
pip install netmiko pyyaml jinja2 paramiko
```

### প্রজেক্ট স্ট্রাকচার

এবার আমাদের ফাইলগুলো সুন্দর করে সাজিয়ে রাখি:

```
network_automation/
│
├── configs/               # কনফিগারেশন ফাইল
│   ├── routers.yml
│   └── interfaces.yml
│
├── templates/            # টেমপ্লেট ফাইল
│   └── loopback.j2
│
├── scripts/             # পাইথন স্ক্রিপ্ট
│   └── deploy.py
│
└── logs/               # লগ ফাইল
    └── automation.log
```

## দ্বিতীয় অধ্যায়: কনফিগারেশন ফাইল

### ১. রাউটার কনফিগারেশন (configs/routers.yml)

```yaml
routers:
  - name: dhaka_router_1
    ip: 192.168.1.1
    username: admin
    password: secure123    # প্রোডাকশনে এভাবে পাসওয়ার্ড রাখবেন না
    type: cisco_ios
    location: Dhaka
    port: 22

  - name: ctg_router_1
    ip: 192.168.1.2
    username: admin
    password: secure123
    type: cisco_ios
    location: Chittagong
    port: 22
```

### ২. ইন্টারফেস কনফিগারেশন (configs/interfaces.yml)

```yaml
interfaces:
  loopback:
    number: 0
    description: Management Interface
    ip: 10.0.0.1
    mask: 255.255.255.0
    enabled: true
    tags:
      - management
      - monitoring
```

## তৃতীয় অধ্যায়: টেমপ্লেট ডিজাইন

### টেমপ্লেট ফাইল (templates/loopback.j2)

```jinja2
{# লুপব্যাক ইন্টারফেস কনফিগারেশন #}
{% if interface.enabled %}
interface Loopback{{ interface.number }}
 description {{ interface.description }}
 ip address {{ interface.ip }} {{ interface.mask }}
 no shutdown
{% for tag in interface.tags %}
 tag {{ tag }}
{% endfor %}
{% endif %}
```

## চতুর্থ অধ্যায়: অটোমেশন স্ক্রিপ্ট

এবার আমরা মূল স্ক্রিপ্ট লিখব যা সব কাজ করবে:

```python
# scripts/deploy.py

import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import logging
from datetime import datetime
import ssl
from pathlib import Path

class NetworkAutomation:
    def __init__(self):
        """অটোমেশন ক্লাস ইনিশিয়ালাইজেশন"""
        self.setup_logging()
        self.base_path = Path(__file__).parent.parent
        
    def setup_logging(self):
        """লগিং সেটআপ"""
        log_file = self.base_path / 'logs' / f'automation_{datetime.now():%Y%m%d_%H%M}.log'
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def load_config(self):
        """কনফিগারেশন ফাইল লোড করা"""
        try:
            with open(self.base_path / 'configs' / 'routers.yml') as f:
                self.routers = yaml.safe_load(f)
            with open(self.base_path / 'configs' / 'interfaces.yml') as f:
                self.interfaces = yaml.safe_load(f)
            logging.info("কনফিগারেশন ফাইল সফলভাবে লোড হয়েছে")
        except Exception as e:
            logging.error(f"কনফিগারেশন লোড করতে সমস্যা: {str(e)}")
            raise
            
    def create_config(self):
        """টেমপ্লেট থেকে কনফিগারেশন তৈরি"""
        try:
            env = Environment(loader=FileSystemLoader(self.base_path / 'templates'))
            template = env.get_template('loopback.j2')
            self.config = template.render(interface=self.interfaces['interfaces']['loopback'])
            logging.info("কনফিগারেশন টেমপ্লেট তৈরি সফল")
        except Exception as e:
            logging.error(f"টেমপ্লেট প্রসেসিং সমস্যা: {str(e)}")
            raise
            
    def configure_routers(self):
        """সব রাউটারে কনফিগারেশন পাঠানো"""
        for router in self.routers['routers']:
            try:
                print(f"\n{router['name']} এ কাজ শুরু...")
                connection = ConnectHandler(**router)
                output = connection.send_config_set(self.config.split('\n'))
                print(f"{router['name']} এ কাজ সফল!")
                logging.info(f"{router['name']} configured successfully")
                connection.disconnect()
            except Exception as e:
                error_msg = f"{router['name']} এ সমস্যা: {str(e)}"
                print(error_msg)
                logging.error(error_msg)
                
    def run(self):
        """মূল প্রোগ্রাম চালানো"""
        try:
            self.load_config()
            self.create_config()
            self.configure_routers()
            print("\nসব রাউটারে কাজ শেষ!")
            logging.info("Automation completed successfully")
        except Exception as e:
            print(f"সমস্যা হয়েছে: {str(e)}")
            logging.error(f"Major error: {str(e)}")

if __name__ == "__main__":
    automation = NetworkAutomation()
    automation.run()
```

[পরবর্তী অংশ পরের মেসেজে...]