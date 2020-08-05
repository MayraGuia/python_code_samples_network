from getpass import getpass
from netmiko import ConnectHandler

username = input('Enter your SSH username: ')
password = getpass()

with open('devices_file_1.txt') as f:
    devices_list = f.read().splitlines()
output = ""
for item in devices_list:
    parts = item.strip().split(",")
    ip = parts[0]
    sw_name = parts[1]
    int_list = []

    for i in range(2,len(parts)):
        int_list.append(parts[i])
    print ('Connecting to device ' + sw_name + " " + ip)

    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password
    }

    net_connect = ConnectHandler(**ios_device)
    output += "++++++++++++++++++ \n"
    output += sw_name + " \n"
    for interface in int_list:
        output_sw = net_connect.send_command("show ip int " + interface)
        lines = output_sw.splitlines()
        if len(lines) == 0:
            print("no output")
            output += "no output \n"
        elif "^" in lines[0]:
            print("syntax error")
            output += "syntax error \n"
        else:
            print(lines[0])
            output += lines[0] + "\n"
with open('..\\BHQ_Reports\\sw_int_report.txt', "w+") as f:
    f.write(output)