To execute first install bind server using following command:
sudo apt update
sudo apt install bind9

see that the dns requests are forwarded to your dns server when ever pinged.(update name record in dns registrar)

replace files in bind directory in you EC2 instance with bind directory provided in this folder.

add the files present in 'home' directory (inside this folder) to home directory of your EC2 instance.

edit bind configuration files to your host name.

see that your zone file is placed in 'var/lib/bind' directory (for load based and roun robin) zone file

restart bind server using command:

sudo service bind9  restart

In home directory run the dns_build.sh file using following command:

sudo ./dns_build.sh

choose appropiate load balancing algorithm.

To generate log report go to dns_log directory present in home directory run the python script generate_log_report using following command:

sudo python3 generate_log_report.py