#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
নেটওয়ার্ক অটোমেশন স্ক্রিপ্ট
এটি ৫০০টা রাউটারে স্বয়ংক্রিয়ভাবে লুপব্যাক কনফিগারেশন সেট করে

স্ক্রিপ্টটি চালানোর আগে নিশ্চিত করুন:

templates ফোল্ডারে loopback.j2 ফাইল আছে
সব প্যাকেজ ইনস্টল করা আছে
রাউটারগুলোতে SSH এক্সেস আছে

নেটওয়ার্কের অটোমেশন: লিংক৩ টিম
তারিখ: ডিসেম্বর ২০২৪
"""

# প্রয়োজনীয় লাইব্রেরি
import yaml                                    # কনফিগারেশন ফাইল হ্যান্ডলিং
from jinja2 import Environment, FileSystemLoader    # টেমপ্লেট ইঞ্জিন
from netmiko import ConnectHandler            # রাউটার কানেকশন
import ipaddress                              # আইপি এড্রেস ক্যালকুলেশন
from netmiko.ssh_exception import NetMikoTimeoutException, AuthenticationException

def generate_interface_config(router_number):
    """
    প্রতিটা রাউটারের জন্য ইউনিক লুপব্যাক আইপি জেনারেট করে

    Args:
        router_number (int): রাউটার নম্বর (1-500)

    Returns:
        dict: লুপব্যাক ইন্টারফেস কনফিগারেশন
    """
    # আইপি এড্রেসের তৃতীয় ও চতুর্থ অক্টেট ক্যালকুলেট করি
    third_octet = (router_number - 1) // 256
    fourth_octet = (router_number - 1) % 256 + 1
    
    return {
        'interfaces': {
            'loopback': {
                'number': 0,
                'description': f'Management Interface Router {router_number}',
                'ip': f'10.0.{third_octet}.{fourth_octet}',
                'mask': '255.255.255.255'
            }
        }
    }

def generate_routers_config(start_ip, total_routers):
    """
    সব রাউটারের মূল কনফিগারেশন জেনারেট করে

    Args:
        start_ip (str): বেস আইপি (যেমন: '192.168.0.0')
        total_routers (int): মোট রাউটার সংখ্যা

    Returns:
        dict: সব রাউটারের কনফিগারেশন
    """
    # /23 সাবনেট থেকে আইপি লিস্ট তৈরি
    network = ipaddress.IPv4Network(f"{start_ip}/23", strict=False)
    ip_list = list(network.hosts())[:total_routers]
    
    routers = {
        'routers': []
    }
    
    # প্রতিটা রাউটারের কনফিগ তৈরি
    for i, ip in enumerate(ip_list, 1):
        router = {
            'name': f'router_{i}',
            'ip': str(ip),
            'username': 'admin',
            'password': 'secure123',
            'device_type': 'cisco_ios'
        }
        routers['routers'].append(router)
    
    return routers

def main():
    """
    মূল প্রোগ্রাম - তিনটি ধাপে কাজ করে:
    ১. রাউটার কনফিগ জেনারেট
    ২. টেমপ্লেট প্রস্তুত
    ৩. প্রতিটা রাউটারে কনফিগারেশন পাঠানো
    """
    try:
        # ১. প্রথমে রাউটার কনফিগ জেনারেট
        print("রাউটার কনফিগারেশন জেনারেট করছি...")
        routers = generate_routers_config('192.168.0.0', 500)
        
        # ২. জিনজা টেমপ্লেট সেটআপ
        print("টেমপ্লেট লোড করছি...")
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('loopback.j2')
        
        # ৩. প্রতিটা রাউটারে কাজ করি
        print("\nরাউটার কনফিগারেশন শুরু করছি...")
        
        success_count = 0
        fail_count = 0
        
        for i, router in enumerate(routers['routers'], 1):
            print(f"\n{router['name']} ({router['ip']}) এ কাজ শুরু...")
            
            try:
                # রাউটারের জন্য লুপব্যাক কনফিগ জেনারেট
                interfaces = generate_interface_config(i)
                config = template.render(interface=interfaces['interfaces']['loopback'])
                
                # রাউটারে কানেক্ট
                connection = ConnectHandler(**router)
                
                # কনফিগ পাঠাই
                output = connection.send_config_set(config.split('\n'))
                print(f"{router['name']} এ কাজ সফল!")
                success_count += 1
                
                # কানেকশন বন্ধ
                connection.disconnect()
                
            except NetMikoTimeoutException:
                print(f"সমস্যা: {router['name']} অফলাইন বা পোর্ট বন্ধ")
                fail_count += 1
            except AuthenticationException:
                print(f"সমস্যা: {router['name']} এ লগইন তথ্য ভুল")
                fail_count += 1
            except Exception as e:
                print(f"সমস্যা: {router['name']} এ অজানা সমস্যা: {str(e)}")
                fail_count += 1
        
        # সামারি রিপোর্ট
        print("\n====== কাজের সারসংক্ষেপ ======")
        print(f"মোট রাউটার: {len(routers['routers'])}")
        print(f"সফল: {success_count}")
        print(f"ব্যর্থ: {fail_count}")
        
    except Exception as e:
        print(f"প্রোগ্রামে গুরুতর সমস্যা: {str(e)}")

if __name__ == "__main__":
    main()
