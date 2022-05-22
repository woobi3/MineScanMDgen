#! /usr/bin/env python3

import re
from datetime import datetime

def ipfilter():
    with open("minescan.log") as f:
        lines = f.readlines()
        filtered = [ x.strip() for x in lines if "data" in x ]
        for i, line in enumerate(filtered):
            filtered[i] = line.split(";")[0]
        return filtered

# def verdata2():
#     with open("minescan.log") as f:
#         lines = f.readlines()
#         vers = []
#         for i, line in enumerate(lines):
#             x = re.findall(r'(([0-9]){1,2}\.){2,3}', line)
#             if x:
#                 vers.append(x[0])
#         return vers
            

ips = ipfilter()

def verdata():
    versions = ["1.18.2", "1.18.1", "1.18", "1.17.1", "1.16", "1.17", "1.8"]
    rd = []
    with open("minescan.log") as f:
        string = []
        for i in f:
            string.append(i.strip())
        for line in string:
            if f"'name': '{versions[0]}'" in line:
                rd.append(line.split(":")[4].split(",")[0])
            if f"'name': '{versions[1]}'" in line:
                rd.append(line.split(":")[4].split(",")[0])
            if f"'name': '{versions[2]}'" in line:
                rd.append(line.split(":")[4].split(",")[0])
            if f"'name': '{versions[3]}'" in line:
                rd.append(line.split(":")[4].split(",")[0])
            if f"'name': '{versions[4]}'" in line:
                rd.append(line.split(":")[4].split(",")[0])
            if f"'name': '{versions[5]}'" in line:
               rd.append(line.split(":")[4].split(",")[0])
            if f"'name': '{versions[6]}'" in line:
                rd.append(line.split(":")[4].split(",")[0])
        for l in rd:
            if l != versions:
                rd.remove(l)
        
        return rd
    
def motdf():
    #find text: in minescan log and return it to list motd
    motd = []
    with open("minescan.log") as f:
        lines = f.readlines()
        for i in lines:
            if "text:" in i:
                motd.append(i.split(":")[1])
    
        

dt = datetime.today().strftime("%I:%M%p %b %d %Y")

ips = ipfilter()
    
with open ("MSReport.md", "w") as report:
        report.write(f"""# MineScan by lockness Ko and woobi3

> {dt}

# This is a list of IP addresses that were found in the minescan.log file:

""")
        for ip in ips:
            report.write("* {}\n".format(ip))
        report.write(f"""
## $ Stats
#### > Total servers:
{len(ips)}
{len(verdata())}
## $ Server list

""")
