import json
import os

def get_ip_from_file(ip_file):
    if os.path.exists(ip_file):
        with open(ip_file, "r") as file:
            current_ip = file.read().strip()
            return current_ip
    else:
        with open(ip_file, "w") as file:
            return "75.101.146.32"
        
def update_ip_in_file(new_ip, ip_file):
    with open(ip_file, "w") as file:
        file.write(new_ip)

def get_thresholds_from_json(json_file):
    with open(json_file, 'r') as file:
        thresholds = json.load(file)
    return thresholds
def set_thresholds_to_json(json_file):
    thresholds = {"3.110.253.167": 4, "18.133.93.123": 4, "75.101.146.32": 4}

    with open(json_file, 'w') as file:
        json.dump(thresholds, file)

def decrease_threshold_in_json(ip, json_file):
    thresholds = get_thresholds_from_json(json_file)
    thresholds[ip] -= 1

    with open(json_file, 'w') as file:
        json.dump(thresholds, file)

def check_reset_json_thresholds(json_file, ip_file):
    thresholds = get_thresholds_from_json(json_file)
    #print(thresholds)

    if all(value == 1 for value in thresholds.values()):
        set_thresholds_to_json(json_file)
        update_ip_in_file("3.110.253.167", ip_file)

def get_next_loadbased_round_robin_ip():
    json_file = 'thresholds.json'
    ip_file = "load_based_ip_address.txt"

    check_reset_json_thresholds(json_file, ip_file)

    ips = ["75.101.146.32", "3.110.253.167", "18.133.93.123"]

    current_ip = get_ip_from_file(ip_file)
    current_ip_index  = ips.index(current_ip)
    thresholds = get_thresholds_from_json(json_file)

    if thresholds[current_ip] > 1:
        decrease_threshold_in_json(current_ip, json_file)

        return current_ip
    else:
        next_index = (current_ip_index + 1) % len(ips)
        next_ip = ips[next_index]
        decrease_threshold_in_json(next_ip, json_file)
        update_ip_in_file(next_ip, ip_file)

        return next_ip

