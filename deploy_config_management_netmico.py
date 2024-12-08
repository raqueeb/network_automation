import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import ipaddress

def generate_interface_config(router_number):
    """
    প্রতিটা রাউটারের জন্য ইউনিক লুপব্যাক আইপি জেনারেট করে
    
    এখানে মূল লজিক:
    - প্রতি রাউটারে আলাদা আইপি থাকবে
    - router_1   -> 10.0.0.1
    - router_256 -> 10.0.1.0
    - router_500 -> 10.0.1.244
    
    Args:
        router_number (int): রাউটার নাম্বার (1-500)
    Returns:
        dict: লুপব্যাক কনফিগারেশন
    """
    third_octet = (router_number - 1) // 256
    fourth_octet = (router_number - 1) % 256 + 1
    
    return {
        'interfaces': {
            'loopback': {
                'number': 0,
                'description': f'Management Interface Router {router_number}',
                'ip': f'10.0.{third_octet}.{fourth_octet}',
                'mask': '255.255.255.255'  # /32 মাস্ক
            }
        }
    }

def generate_routers_config(start_ip, total_routers):
    """
    রাউটারের ম্যানেজমেন্ট আইপি জেনারেট করে
    
    মূল লজিক:
    - 192.168.0.0/23 থেকে 512টা আইপি পাওয়া যায়
    - প্রথম রাউটার: 192.168.0.1
    - শেষ রাউটার: 192.168.1.244
    
    Args:
        start_ip (str): বেস আইপি (192.168.0.0)
        total_routers (int): মোট রাউটার সংখ্যা (500)
    Returns:
        dict: রাউটার কনফিগারেশন
    """
    # /23 সাবনেট নিলাম যাতে 500+ আইপি পাই
    network = ipaddress.IPv4Network(f"{start_ip}/23", strict=False)
    ip_list = list(network.hosts())[:total_routers]
    
    routers = {
        'routers': []
    }
    
    for i, ip in enumerate(ip_list, 1):
        router = {
            'name': f'router_{i}',
            'ip': str(ip),
            'username': 'admin',
            'password': 'secure123',
            'type': 'cisco_ios'
        }
        routers['routers'].append(router)
    
    return routers

def main():
    """
    মূল প্রোগ্রাম লজিক
    
    কাজের ধাপ:
    ১. রাউটার ম্যানেজমেন্ট আইপি জেনারেট (192.168.0.0/23)
    ২. প্রতি রাউটারের জন্য লুপব্যাক আইপি জেনারেট (10.0.x.y)
    ৩. কনফিগারেশন পাঠানো
    """
    # ১. প্রথমে ৫০০টা রাউটারের ম্যানেজমেন্ট আইপি জেনারেট
    routers = generate_routers_config('192.168.0.0', 500)
    
    # ২. জিনজা টেমপ্লেট সেটআপ
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('loopback.j2')
    
    # ৩. প্রতিটা রাউটারে কাজ করি
    for i, router in enumerate(routers['routers'], 1):
        # এই রাউটারের জন্য ইউনিক লুপব্যাক
        interfaces = generate_interface_config(i)
        
        # কনফিগ কমান্ড তৈরি
        config = template.render(interface=interfaces['interfaces']['loopback'])
        
        print(f"\n{router['name']} ({router['ip']}) এ কাজ শুরু...")
        try:
            # রাউটারে কানেক্ট
            connection = ConnectHandler(**router)
            
            # কনফিগ পাঠাই
            output = connection.send_config_set(config.split('\n'))
            print(f"{router['name']} এ কাজ সফল!")
            
            # কানেকশন বন্ধ
            connection.disconnect()
        except Exception as e:
            print(f"সমস্যা হয়েছে {router['name']} এ: {str(e)}")

if __name__ == "__main__":
    main()
