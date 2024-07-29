import yaml

""" 1. `open("yaml_example.yaml", 'r') as stream`: এই লাইনে `yaml_example.yaml` নামের ফাইলটি খোলা হয়েছে রিড মোডে (`'r'`) এবং এটি `stream` নামক ভেরিয়েবলে সেভ হয়েছে।
2. `yaml_dict = yaml.safe_load(stream)`: ফাইলটি থেকে YAML ফরম্যাটের ডেটা লোড করা হয়েছে `yaml.safe_load()` ফাংশনের মাধ্যমে এবং এই ডেটা অবজেক্ট হিসেবে `yaml_dict` ভেরিয়েবলে সেভ হয়েছে।
 """
with open("yaml_example.yaml", 'r') as stream:
        yaml_dict = yaml.safe_load(stream)

# ইন্টারফেসের নাম একটি ভেরিয়েবলে সংরক্ষণ করুন
int_name = yaml_dict["interface"]["name"]

# ইন্টারফেসের IP ঠিকানা পরিবর্তন করুন
yaml_dict["interface"]["ipv4"]["address"][0]["ip"] = "192.168.0.2"

# ডিকশনারির yaml স্ট্রিং সংস্করণে ফিরে যান
print(yaml.dump(yaml_dict, default_flow_style=False))