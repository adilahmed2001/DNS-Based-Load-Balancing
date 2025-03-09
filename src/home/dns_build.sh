#!/bin/bash
    echo "Select an Algorithm:"
    echo "1. Round Robin based"
    echo "2. Geo Location based"
    echo "3. Load based Round Robin"
    echo "4. Exit"

    read -p "Enter your choice (1/2/3/4): " choice

    BIND_LOG="/var/log/named/bind.log"
    COUNT_FILE="/home/dns_log/count.txt"

    if [ ! -f "$COUNT_FILE" ]; then
        echo "0" > "$COUNT_FILE"
    fi

    case $choice in
        1)
            echo "Loading Configuration..."
            sudo cp /home/load_and_round_robin/named.conf /etc/bind
            echo "Success"
            echo "Restarting Bind..."
            sudo service bind9 restart
            echo "Succcess"
            cd code_dns
            echo "Running Python File..."
            tail -n 0 -F "$BIND_LOG" | while read -r line
            do
                if [[ $line == *"queries: info: client"* && $line == *"query: mohammedadilsaikiran.online IN A "* ]]; then
                    current_count=$(($(cat "$COUNT_FILE") + 1))
                    echo "$current_count" > "$COUNT_FILE"
                    sudo python3 update_log.py < ip_address.txt $line
                    sudo python3 run_nsupdate_script.py 0
                fi
            done
            ;;
        2)
            echo "Loading Configuration..."
            sudo cp /home/geo_loc/named.conf /etc/bind
            echo "Restarting Bind..."
            sudo service bind9 restart
            echo "Success"
            echo "If you want to change Algorithm run the script again"
            ;;
        3)
            echo "Loading Configuration..."
            sudo cp /home/load_and_round_robin/named.conf /etc/bind
            echo "Success"
            echo "Restarting Bind..."
            sudo service bind9 restart
            echo "Success"
            cd code_dns
            echo "Running Python Script..."
            tail -n 0 -F "$BIND_LOG" | while read -r line
            do
                if [[ $line == *"queries: info: client"* && $line == *"query: mohammedadilsaikiran.online IN A "* ]]; then
                    current_count=$(($(cat "$COUNT_FILE") + 1))
                    echo "$current_count" > "$COUNT_FILE"
                    sudo python3 update_log.py < load_based_ip_address.txt $line
                    sudo python3 run_nsupdate_script.py 1
                fi
            done
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter a valid option (1/2/3/4)."
            ;;
    esac

