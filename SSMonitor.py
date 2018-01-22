#!/usr/bin/python3

import socket
import os
import ast

cli = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
try:
    cli.bind('/tmp/shadowsocks-client.sock')  # address of the client
    cli.connect('/var/run/shadowsocks-manager.sock')  # address of Shadowsocks manager
except Exception as e:
    print("FAILED")
    print(e)
    cli.close()
    os.system("rm /tmp/shadowsocks-client.sock")
    exit()

# Check connection
cli.send(b'ping')
print(cli.recv(1506))  # You'll receive 'pong'

data = {
    "2016": 0,
    "2017": 0,
    "2018": 0,
    "2019": 0,
    "2020": 0,
    "2021": 0
}

while True:
    try:
        message = ast.literal_eval(cli.recv(1506).decode('ascii')[6:])  # when data is transferred on Shadowsocks, you'll receive stat info every 10 seconds
        for key in message:
            data[key] += message[key]
        os.system("cp ./shadowsocks_statistic.html ./shadowsocks_statistic.back")
        os.system("rm ./shadowsocks_statistic.html")
        os.system("touch ./shadowsocks_statistic.html")
        with open("./shadowsocks_statistic.html", "w") as f:
            f.write("<html><head></head><body>")
            for key in data:
                f.write("<p> {}: {} MB\n </p>".format(key, data[key] / (1024 * 1024)))
            f.write("</body></html>")
        print(message)
        print(data)
    except KeyboardInterrupt as e:
        print("SHUT DOWN")
        cli.close()
        os.system("rm /tmp/shadowsocks-client.sock")
        exit()

