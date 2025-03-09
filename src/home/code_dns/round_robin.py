import os

def get_next_round_robin_ip():
    file_path = "ip_address.txt"
    current_ip = get_ip_from_file(file_path)

    ips = ["75.101.146.32", "3.110.253.167", "18.133.93.123"]

    next_index = (ips.index(current_ip) + 1) % len(ips)
    update_ip_in_file(ips[next_index], file_path)

    return ips[next_index]

def get_ip_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            current_ip = file.read().strip()
            return current_ip
    else:
        with open(file_path, "w") as file:
            return "75.101.146.32"

def update_ip_in_file(new_ip, file_path):
    with open(file_path, "w") as file:
        file.write(new_ip)
