from datetime import datetime
import os
from dotenv import load_dotenv
import requests
import pymongo

load_dotenv()

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

def getMotd(ip):
    print(f"[INFO] Getting motd for {ip}")
    with open("minescan.log", "r") as f:
        lines = f.readlines()
        filtered = [ x.strip() for x in lines if "data" in x ]
        for i, line in enumerate(filtered):
            ip_ = line.split(";")[0].rstrip()
            if ip == ip_:
                a = line.split(";")[1].lstrip()
                try:
                    return [ x.replace("(", "").replace(")", "") for x in a[12:-2].split("), (") ][0].split("text':")[1][2:-2]
                except:
                    print(f"[WARN] Failed to parse motd for {ip}")
                    return "A Minecraft Server"

def getPlayerCount(ip):
    print(f"[INFO] Getting player count for {ip}")
    with open("minescan.log", "r") as f:
        lines = f.readlines()
        filtered = [ x.strip() for x in lines if "data" in x ]
        for i, line in enumerate(filtered):
            ip_ = line.split(";")[0].rstrip()
            if ip == ip_:
                a = line.split(";")[1].lstrip()
                try:
                    return int([ x.replace("(", "").replace(")", "") for x in a[12:-2].split("), (") ][1].split("online':")[1].split(",")[0][1:])
                except:
                    print(f"[WARN] Failed to parse player count for {ip}")
                    return 0

def getVersion(ip):
    print("[INFO] Getting version info for {ip}")
    with open("minescan.log", "r") as f:
        lines = f.readlines()
        filtered = [ x.strip() for x in lines if "data" in x ]
        for i, line in enumerate(filtered):
            ip_ = line.split(";")[0].rstrip()
            if ip == ip_:
                a = line.split(";")[1].lstrip()
                try:
                    return [ x.replace("(", "").replace(")", "") for x in a[12:-2].split("), (") ][2].split("{")[1].split(": ")[1].split(",")[0][1:-1]
                except:
                    print(f"[WARN] Failed to parse version info for {ip}")
                    return "-1"


ips = ipfilter()
version = data()[1]

client = pymongo.MongoClient("mongodb://root:password@localhost:27017/")
db = client["mcstats"]

statsdb = db["stats"]
serversdb = db["servers"]

servers = []

for i, ip in enumerate(ips):
    print(f"[INFO] Handling ip {ip}")
    
    IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")

    #ipinfo = requests.get(f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}").json()

    ipinfo = {"city": "", "country": "", "region": "", "timezone": ""}

    city = ipinfo["city"]
    country = ipinfo["country"]
    region = ipinfo["region"]

    loc = f"{country}, {region}, {city}"

    servers.append({ 'ip': ip, 'version' : getVersion(ip), 'motd': getMotd(ip), 'player_count': getPlayerCount(ip), 'timezone': ipinfo["timezone"], 'location': loc })

print("[INFO] Clearing server collection")
serversdb.drop()
print("[INFO] Inserting data into server collection")
serversdb.insert_many(servers)

print("[INFO] Calculating stats")
total_servers = len(ips)
versions = {
    "1.18.2": len([i for i in version if "1.18.2" in i]),
    "1.18.1": len([i for i in version if "1.18.1" in i]),
    "1.18"  : len([i for i in version if "'1.18'" in i]),
    "1.17.1": len([i for i in version if "1.17.1" in i]),
    "1.8"   : len([i for i in version if "1.8" in i]),
    "1.12.1": len([i for i in version if "1.12.1" in i])
}

player_mean = sum([ x['player_count'] for x in servers ])/len(servers)

players = {
    "mean"  : player_mean,
    "min"   : min([ x['player_count'] for x in servers ]),
    "max"   : max([ x['player_count'] for x in servers ])
}

print("[INFO] Clearing stats collection")
statsdb.drop()
print("[INFO] Inserting data into stats collection")
statsdb.insert_many([versions, players])

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

#### > 1.18.2: {versions['1.18.2']}

#### > 1.18.1: {versions['1.18.1']}

#### > 1.18: {versions['1.18']}

#### > 1.17.1: {versions['1.17.1']}

#### > 1.8: {versions['1.8']}

#### > 1.12.1: {versions['1.12.1']}

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
