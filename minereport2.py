from datetime import datetime
from minereport import ipfilter

def data():
    ip = []
    version = []
    motd = []
    mplayers = []
    with open("minescan.log") as f:
        lines = f.readlines()
        for line in lines:
            if "data" in line:
                ip.append(line.split(";")[0])
            if "text" in line:
                print(line.split(":")[1])

print(data())
    


















# with open ("MSReport.md", "w") as report:
#     dt = datetime.today().strftime("%I:%M%p %b %d %Y")

#     report.write(f"""# MineScan by lockness Ko and woobi3

# > {dt}

# # This is a list of IP addresses that were found in the minescan.log file:

# """)
#     for ip in ips:
#             report.write("* {}\n".format(ip))
#     report.write(f"""
# ## $ Stats
# #### > Total servers:
# {len(ips)}
# {len(verdata())}
# ## $ Server list

# """)



















