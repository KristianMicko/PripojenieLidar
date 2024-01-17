from sick_scan_tcp import SickScan
import time
import numpy as np
import socket
import re
import sys

def is_ip_or_url(input_string):
    ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
    url_pattern = r'^[a-zA-Z0-9.-]+$'
    
    if re.match(ip_pattern, input_string):
        return "IP address"
    elif re.match(url_pattern, input_string):
        return "URL"
    else:
        return "Neither"

def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.gaierror:
        return None

IP = input("zadaj IP/DNS adresu Lidar-a\n")
port = input("zadaj port\n")

result_of_check_IP_input = is_ip_or_url(IP)
if result_of_check_IP_input == "IP address":
    Pass
elif result_of_check_IP_input == "URL":
    IP = get_ip_address(IP)
else:
    print("nenaslo danu IP/DNS adresu")
    sys.exit()

def random_filename():
    local_time = time.localtime(time.time())
    formatted_time = time.strftime('%Y-%m-%d-%H-%M-%S', local_time)
    return str(formatted_time) 

sick_scan = SickScan(ip=IP, port=int(port))

try:
    while True:
        telegram = sick_scan.scan()
        try:
            angles, values = sick_scan.extract_telegram(telegram=telegram)
            x, y = sick_scan.to_cartesian(angles=angles, distances=values)

            if len(x) > 3 and len(y) > 3:
                # Vytvorenie súboru .xyz
                filename = random_filename() + '.xyz'
                with open(filename, 'w') as file:
                    for xi, yi in zip(x, y):
                        file.write(f"{xi} {yi} 0\n")
                print(f"Point cloud saved as {filename}")

        except Exception as e:
            print(e)
        time.sleep(0.1)
except KeyboardInterrupt:
    sick_scan.release()
