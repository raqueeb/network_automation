import tempfile
import subprocess
from netmiko import ConnectHandler

# Cisco IOS-XE connection details
device = {
    "device_type": "cisco_ios",
    "host": "devnetsandboxiosxe.cisco.com",
    "username": "admin",
    "password": "C1sco12345",
}
# Git repository details
git_repo_url = "https://github.com/aiwithr/ios_git"
commit_message = "Automatic config update"


# ------ Connect to device and get device config ------

# Connect to IOS-XE device
net_connect = ConnectHandler(**device)

# Run show command on device
device_config = net_connect.send_command("show run")

# Disconnect from Device
net_connect.disconnect()


# ------ Clone git repo in temporary directory, replace files with new config file and push changes back to git repo  ------

# Create temporary directory
temporary_folder = tempfile.TemporaryDirectory()

# Clone Git Repo
subprocess.call(
    f"cd {temporary_folder.name} && git clone {git_repo_url} . && rd /s /q *.*", shell=True
)

# Write all config to file
with open(f"{temporary_folder.name}/{device['host']}_config.txt", "w") as outfile:
    outfile.write(device_config)

# git init
# git add -A
# git commit -m '{commit_message}'

# git remote add origin {git_repo_url}
# git push origin main --force
# Git commit all changes
subprocess.call(
    f"cd {temporary_folder.name} && git init && git add -A && git commit -m '{commit_message}' git remote add origin {git_repo_url} && git push origin main --force",
    shell=True,
)

# Delete temporary directory
temporary_folder.cleanup()