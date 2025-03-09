import os

directory = "/home/dns_log"

ip_file_mapping = {
    "3.110.253.167": "clients_webserver_in.txt",
    "18.133.93.123": "clients_webserver_eu.txt",
    "75.101.146.32": "clients_webserver_us.txt"
}

count_file_path = "/home/dns_log/count.txt"

with open(count_file_path, 'r') as count_file:
    count = count_file.read().strip()

print("{:<15} {:<25} {:<10}".format("Web Server IP", "File Name", "Client Count"))
print("="*55)

for ip, file_name in ip_file_mapping.items():
    file_path = os.path.join(directory, file_name)

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            line_count = min(len(lines), int(count))
    except FileNotFoundError:
        line_count = 0

    print("{:<15} {:<25} {:<10}".format(ip, file_name, line_count))

print("="*55)
print("Total Clients: {}".format(count))
