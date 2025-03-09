import sys

def add_line_to_file(file_path, line):
    try:
        with open(file_path, 'a') as file:
            file.write(line + '\n')

    except FileNotFoundError:
        with open(file_path, 'w') as file:
            file.write(line + '\n')
        print(f"File not found. Created a new file '{file_path}' and added the line '{line}'.")


ips_dict = {"3.110.253.167" : "clients_webserver_in.txt", 
"18.133.93.123" : "clients_webserver_eu.txt", 
"75.101.146.32" : "clients_webserver_us.txt" }

file_name = ips_dict[input()]
file_path = f"/home/dns_log/{file_name}"
line_to_add = sys.argv[7]

add_line_to_file(file_path, line_to_add)
