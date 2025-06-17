try:
    import network
except Exception:
    pass
import time

class Connector:

    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        
    def connect_to_wifi(self):
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(self.ssid, self.password)
        print(f"connecting to {self.ssid} ...")

        timeout = 10  # seconds
        start = time.time()
        while not wifi.isconnected():
            if time.time() - start > timeout:
                raise RuntimeError("wifi-connection failed")
            time.sleep(0.1)

        print("Connected. IP-address:", wifi.ifconfig()[0])
        return wifi
