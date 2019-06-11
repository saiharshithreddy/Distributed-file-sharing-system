import subprocess

def getMyIp():
    global myIp
    ip_list = subprocess.check_output(
        "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' \
        | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'",
        shell=True)
    my_ips = ip_list.split()
    myIp = ','.join(my_ips)