from datetime import datetime
from minereport import ipfilter
import pymongo

def data():
    ipversion = []
    motd = []
    mplayers = []
    with open("minescan.log") as f:
        lines = f.readlines()
        for line in lines:
            if "data" in line:
                ip = line.split(";")[0]
                version = line.split("name")[1].split(",")[0]
                ipversion.append(f"{ip}{version}")
                if "text" in line:
                    motd.append(line.split("text")[1].split("}")[0])
            else:
                pass
        return motd, ipversion, version

def ipfilter():
    with open("minescan.log") as f:
        lines = f.readlines()
        filtered = [ x.strip() for x in lines if "data" in x ]
        for i, line in enumerate(filtered):
            filtered[i] = line.split(";")[0]
        return [ ip.rstrip() for ip in filtered ]

def getMotd():
    with open("minescan.log", "r") as f:
        lines = f.readlines()
        filtered = [ x.strip() for x in lines if "data" in x ]
        for i, line in enumerate(filtered):


ips = ipfilter()
version = data()[1]

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mcstats"]

statsdb = db["stats"]
serversdb = db["servers"]

servers = {}

for i, ip in enumerate(ips):
    servers[ip] = { motd: "message of the day", player_count: 0 }

with open("www/static/minereport.md", "w") as report:
    dt = datetime.today().strftime("%I:%M%p %b %d %Y")

    report.write(f"""# MineScan by lockness Ko and woobi3

> {dt}

# This is a list of IP addresses that were found in the minescan.log file:

""")
    # for ip in ips:
    #         report.write("* {}\n".format(ip))
    report.write(f"""
## $ Stats

#### > Total servers found: {len(ips)}

#### > 1.18.2: {len([i for i in version if "1.18.2" in i])}

#### > 1.18.1: {len([i for i in version if "1.18.1" in i])}

#### > 1.18: {len([i for i in version if "'1.18'" in i])}

#### > 1.17.1: {len([i for i in version if "1.17.1" in i])}

#### > 1.8: {len([i for i in version if "1.8" in i])}

## $ Server list:

#### > 1.18.2:
""")
    for i in version:
        if "1.18.2" in i:
            report.write(f"* {i}\n")
    report.write(f"""
#### > 1.18.1:
""")
    for i in version:
        if "1.18.1" in i:
            report.write(f"* {i}\n")
    report.write(f"""
#### > 1.18:
""")
    for i in version:
        if "'1.18'" in i:
            report.write(f"* {i}\n")
    report.write(f"""
#### > 1.17.1:
""")
    for i in version:
        if "1.17.1" in i:
            report.write(f"* {i}\n")
            

















