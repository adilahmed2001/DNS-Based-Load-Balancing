import json
import subprocess
import os
from loadbased_round_robin import get_next_loadbased_round_robin_ip
from round_robin import get_next_round_robin_ip
import sys
import requests

def is_web_server_active(url):
    try:
        response = requests.head(url, timeout=1)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

def read_thresholds():
    with open('thresholds.json', 'r') as file:
        thresholds = json.load(file)
        return thresholds

def write_to_thresholds(ip):
    thresholds = read_thresholds()
    thresholds[ip] = 1
    with open('thresholds.json', "w") as file:
        json.dump(thresholds, file)

def run_nsupdate(commands):
    try:
        process = subprocess.Popen(['nsupdate'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.communicate(input='\n'.join(commands))

        if process.returncode == 0:
            print("IP update successful in zone file")
        else:
            print(f"nsupdate command failed with return code {process.returncode}")
            print(process.stderr)

    except Exception as e:
        print(f"An error occurred: {e}")

def get_next_active_round_robin_ip():
    new_ip_website = get_next_round_robin_ip()
    if not is_web_server_active(f"http://{new_ip_website}"):
        new_ip_website = get_next_round_robin_ip()
        if not is_web_server_active(f"http://{new_ip_website}"):
            new_ip_website = get_next_round_robin_ip()
            if not is_web_server_active(f"http://{new_ip_website}"):
                new_ip_website = get_next_round_robin_ip()

    return new_ip_website

def get_next_active_loadbased_round_robin_ip():
    new_ip_website = get_next_loadbased_round_robin_ip()
    if not is_web_server_active(f"http://{new_ip_website}"):
        write_to_thresholds(new_ip_website)
        new_ip_website = get_next_loadbased_round_robin_ip()
        if not is_web_server_active(f"http://{new_ip_website}"):
            write_to_thresholds(new_ip_website)
            new_ip_website = get_next_loadbased_round_robin_ip()
            if not is_web_server_active(f"http://{new_ip_website}"):
                write_to_thresholds(new_ip_website)
                new_ip_website = get_next_loadbased_round_robin_ip()
    return new_ip_website

new_ip_website = get_next_active_round_robin_ip() if int(sys.argv[1]) == 0 else get_next_active_loadbased_round_robin_ip()

update_commands = [
    'server ns1.mohammedadilsaikiran.online',
    'update delete mohammedadilsaikiran.online A',
    f'update add mohammedadilsaikiran.online 0 A {new_ip_website}',
    'send',
]

run_nsupdate(update_commands)
