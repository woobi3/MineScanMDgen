from twisted.internet import reactor
from quarry.net.client import ClientFactory, ClientProtocol
import subprocess, time, multiprocessing

def HandleIP(ip):
    print(f"[INFO] Handling IP {ip}")
    with open("minescan.log", "a+") as log:
        log.write(f"\n{ip} ")

    factory = PingFactory()
    factory.connect(ip, 25565)
    reactor.run()

def HandleData(data):
    print(f"[INFO] Handling Data {data}")
    with open("minescan.log", "a+") as log:
        log.write(f"; {data}\n")

class PingProtocol(ClientProtocol):
    def status_response(self, data):
        out = data.items()
        reactor.stop()
        HandleData(out)

class PingFactory(ClientFactory):
    protocol = PingProtocol
    protocol_mode_next = "status"

class MassScan:
    def __init__(self, subnet, rate=1000):
        #sudo masscan -p25565 0.0.0.0/0 --exclude 1.1.1.1 --rate=10000
        self.command = ["bash", "-c", f"sudo masscan -p25565 {subnet} --exclude 0.0.0.0 --rate={rate} 2>/dev/null"]
    
    def scan(self, cb):
        with subprocess.Popen(self.command, stdout=subprocess.PIPE) as proc:
            while proc.poll() is None:
                ip = proc.stdout.readline().split(b' ')[5].decode("utf-8")
                p = multiprocessing.Process(target=cb, name="callback", args=(ip,))
                p.start()
                time.sleep(5)
                p.terminate()
                p.join()

def main():
    scanner = MassScan("0.0.0.0/0")

    print("[INFO] Starting scan")

    scanner.scan(HandleIP)
    
if __name__ == "__main__":
    main()
