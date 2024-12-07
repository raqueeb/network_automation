```python
# প্রয়োজনীয় লাইব্রেরি ইমপোর্ট 
from netmiko import ConnectHandler
import getpass
from datetime import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
import shutil
import os
from git import Repo

# গ্লোবাল ভ্যারিয়েবল ডিক্লেয়ার করা
backup_folder = '/backups'
vendor_commands = {
    "cisco_ios": "show running-config",        
    "juniper_junos": "show configuration",           
    "mikrotik_routeros": "export configuration"     
}

def backup_single_device(device):
    """ডিভাইস কানেক্ট করে কনফিগার ব্যাকআপ নেয়"""
    
    # ডিভাইসের সাথে SSH কানেকশন স্থাপন
    connection = ConnectHandler(**device)

    # কনফিগারেশন কমান্ড পাঠানো এবং আউটপুট নেয়া
    config = connection.send_command(vendor_commands[device['device_type']])
    
    # ফাইল নামে টাইমস্ট্যাম্প যোগ করা 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_folder}/backup_{device['host']}_{timestamp}.txt"
    
    # কনফিগারেশন ফাইলে রাইট করা
    with open(backup_file, 'w') as f:
        f.write(config)

    # কানেকশন ক্লোজ করা  
    connection.disconnect()
            
    # ফাইল validation করা 
    if validate_backup(backup_file):
        logging.info(f"Backup successful for {device['host']}")
    else:
        logging.error(f"Backup validation failed for {device['host']}")
        
    return backup_file

def backup_all_devices():
    """একাধিক ডিভাইসের কনফিগ ব্যাকআপ নেওয়ার মূল ফাংশন"""
    
    # ইউজার থেকে পাসওয়ার্ড নেয়া
    password = getpass.getpass('Enter password: ')
    
    # টার্গেট ডিভাইসগুলোর লিস্ট
    switch_list = [
        '192.168.1.10',     
        '192.168.1.20',     
        '192.168.1.30'      
    ]
    
    # প্রতিটি ডিভাইসের জন্য ইনফো ডিকশনারি তৈরি  
    device_list = []
    for switch_ip in switch_list:
        device = {
            "device_type": "cisco_ios",      
            "host": switch_ip,               
            "username": "admin",             
            "password": password             
        }
        device_list.append(device)
        
    # মাল্টিথ্রেডিং ব্যবহার করে প্যারালাল ব্যাকআপ 
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_device = {
            executor.submit(backup_single_device, device): device 
            for device in device_list
        }
        
        # ফিউচারগুলো resolve হওয়ার অপেক্ষা  
        for future in as_completed(future_to_device):
            device = future_to_device[future]
            try:
                backup_file = future.result()
                
                # ব্যাকআপ স্ট্যাটাস নিয়ে নোটিফিকেশন পাঠানো 
                send_notification("Successful", f"Device: {device['host']}, File: {backup_file}")

            except Exception as e:
                logging.error(f"Device {device['host']} failed: {str(e)}")
                
                # ব্যাকআপ ফেইল হলে এরর নোটিফিকেশন
                send_notification("Failed", f"Device {device['host']} encountered error: {str(e)}")

def compress_old_backups():
    """পুরনো ব্যাকআপ ফাইল কমপ্রেস করার ফাংশন"""

    # ব্যাকআপ ফোল্ডার এর সকল .txt ফাইল বেছে নেয়া
    for file in os.listdir(backup_folder):
        if file.endswith('.txt'):
            file_path = os.path.join(backup_folder, file)
            
            # ফাইলকে gzip এ কমপ্রেস করা 
            with open(file_path, 'rb') as f_in:
                with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # অরিজিনাল ফাইল ডিলিট করে দেয়া
            os.remove(file_path)
            
def validate_backup(config_file):
    """ব্যাকআপ ফাইল validation করার ফাংশন"""
    
    try:
        with open(config_file, 'r') as f:
            content = f.read()
            # ফাইলের সাইজ চেক করা 
            if len(content) < 100:  
                logging.warning(f"Suspicious backup size for {config_file}")
                return False
            return True
    except Exception as e:
        logging.error(f"Validation failed: {str(e)}")
        return False
        
def send_notification(status, details):
    """ইমেইলে নোটিফিকেশন পাঠানোর ফাংশন"""

    # ইমেইল বেসিক কনফিগারেশন 
    sender = "backup@example.com"
    receiver = "admin@example.com"
    
    # ইমেইল বডি তৈরি  
    msg = MIMEText(f"Backup Status: {status}\n\nDetails:\n{details}")
    msg['Subject'] = f"Backup Report - {datetime.now().date()}"
    msg['From'] = sender
    msg['To'] = receiver
    
    # ইমেইল প্রেরণ করা
    with smtplib.SMTP('mail.example.com') as server:
        server.send_message(msg)

def commit_to_git():
    """ব্যাকআপ ফাইলগুলোকে গিট রিপোতে কমিট করার ফাংশন"""
    
    # গিট রিপো লোড করা 
    repo = Repo(backup_folder)
    
    # সকল পরিবর্তন stage এ যোগ করা  
    repo.git.add(all=True)
    
    # চেঞ্জ কমিট করা 
    repo.index.commit(f"Backup taken on {datetime.now()}")
    
    # রিমোট রিপোতে পুশ করা 
    origin = repo.remote(name='origin')
    origin.push()

# মেইন প্রোগ্রাম
if __name__ == "__main__":

    # লগিং কনফিগারেশন 
    logging.basicConfig(
        filename=f"{backup_folder}/backup_operations.log", 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # ব্যাকআপের মূল কাজ শুরু 
    backup_all_devices()
    
    # পুরনো ফাইল কমপ্রেস করে নেয়া 
    compress_old_backups()
    
    # গিটে কমিট এবং পুশ করা
    commit_to_git()
```

এখানে আমরা আগের সকল স্টেপগুলো একত্রিত করে পুরো একটা স্ক্রিপ্ট তৈরি করলাম। কোডের গুরুত্বপূর্ণ অংশগুলো সংক্ষেপে বর্ণনা করা হল:

1. প্রথমে সকল প্রয়োজনীয় লাইব্রেরি/মডিউল ইমপোর্ট করা হল।
2. `backup_single_device(device)` নামে একটি ফাংশন লেখা হল যেটা একটি নির্দিষ্ট ডিভাইসে কানেক্ট করে কনফিগারেশন ব্যাকআপ নিবে।  
3. `backup_all_devices()` নামের মূল ফাংশনটি থ্রেড পুল তৈরি করবে এবং একাধিক ডিভাইসের ব্যাকআপ প্রসেস প্যারালালি করবে। 
4. `compress_old_backups()` ফাংশন ব্যাকআপ ফোল্ডার থেকে পুরনো `.txt` ফাইলগুলোকে বেছে নিয়ে কমপ্রেস করবে এবং অরিজিনাল ফাইল ডিলিট করবে।
5. `validate_backup(config_file)` ফাংশন চেক করবে ব্যাকআপকৃত ফাইলের সাইজ সঠিক হয়েছে কিনা। 
6. `send_notification(status, details)` ফাংশন ব্যাকআপ স্ট্যাটাসের ইমেল নোটিফিকেশন প্রেরণ করবে।
7. `commit_to_git()`  ফাংশন নতুন ব্যাকআপ ফাইলগুলোকে গিট রিপোতে কমিট করে পুশ করবে।
8. মেইন প্রোগ্রাম শুরু করার আগে লগিং কনফিগার করা হবে এবং একে একে উপরের ফাংশনগুলোকে কল করা হবে।

আশা করি এই বিস্তারিত বর্ণনা ও কোড কমেন্টস থেকে আপনি আরও ভালভাবে বুঝতে পারবেন নেটওয়ার্ক অটোমেশনের প্রাথমিক ধাপগুলো কিভাবে পাইথন স্ক্রিপ্টে রূপ নেয়। এটি একটি শুরুর পয়েন্ট মাত্র; ধীরে ধীরে আরও অনেক আকর্ষণীয় ফিচার যোগ করে এই স্ক্রিপ্টকে একটি দক্ষ ও স্কেলেবল নেটওয়ার্ক অটোমেশন টুলে রূপান্তরিত করা সম্ভব।