import socket
import sys
from datetime import datetime
import requests
import urllib3

# ปิดคำเตือนเรื่อง SSL เวลากล้องใช้ใบรับรองแบบ Self-Signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CCTVFinder:

    def __init__(self, subnet: str, start: int = 1, end: int = 50, timeout: float = 1.0):
        self.subnet = subnet
        self.start_ip = start
        self.end_ip = end
        self.timeout = timeout

        # พอร์ตสำคัญของระบบกล้องวงจรปิดและตัวบันทึก (NVR/DVR)
        self.target_ports = [80, 443, 554, 8000, 37777]

        # ตรวจสอบยี่ห้อกล้อ
        self.signatures = {
            "Hikvision": ["hikvision", "hikvision-webs", "app-http subsystem", "8000"],
            "Dahua": ["dahua", "webservice", "dmss", "37777"],
            "Axis Communications": ["axis", "axis-neteye"],
            "Xiongmai (XM)": ["netsurveillance", "uc-httpd"],
            "Vivotek": ["vivotek", "network camera v"]
        }

    def _get_web_fingerprint(self, ip: str, port: int) -> str:
        """ส่ง HTTP Request เพื่อวิเคราะห์ยี่ห้อกล้องจาก Header และ HTML Content"""
        protocol = "https" if port == 443 else "http"
        url = f"{protocol}://{ip}:{port}"
        
        try:
            response = requests.get(url, timeout=self.timeout, verify=False)
            server_header = response.headers.get("Server", "").lower()
            html_body = response.text.lower()
            
            for brand, keywords in self.signatures.items():
                for keyword in keywords:
                    if keyword in server_header or keyword in html_body:
                        return brand
            return "Unknown Web Device"
            
        except requests.exceptions.RequestException:
            return "Web UI (No Response)"

    def scan_device(self, ip: str):
        """ตรวจสอบพอร์ตและแยกแยะประเภทอุปกรณ์รายตัว"""
        open_ports = []
        device_type = None

        for port in self.target_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(self.timeout)
                    if s.connect_ex((ip, port)) == 0:
                        open_ports.append(port)
                        
                        # แยกแยะค่ายเบื้องต้นจากพอร์ตเฉพาะทาง (SDK)
                        if port == 8000:
                            device_type = "Hikvision Device (SDK)"
                        elif port == 37777:
                            device_type = "Dahua Device (SDK)"
                        elif port == 554 and not device_type:
                            device_type = "Generic RTSP Stream"
                            
                        # วิเคราะห์ข้อมูลหน้าเว็บเพิ่มเติม
                        if port in [80, 443] and not device_type:
                            fingerprint = self._get_web_fingerprint(ip, port)
                            if fingerprint != "Unknown Web Device":
                                device_type = f"{fingerprint} (Web UI)"
            except Exception:
                pass

        if open_ports:
            detected_as = device_type if device_type else "Unknown Network Device"
            ports_str = ", ".join(str(p) for p in open_ports)
            print(f"[+] IP: {ip:<15} | Ports: [{ports_str:<15}] | Identity: {detected_as}")

    def run(self):
        """เริ่มกระบวนการสแกนตามช่วง IP ที่กำหนดไว้"""
        print("-" * 70)
        print(f" CCTV-Finder | Inwzer007 ")
        print(f" Target Range : {self.subnet}{self.start_ip} - {self.subnet}{self.end_ip}")
        print(f" Timestamp    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)

        try:
            for i in range(self.start_ip, self.end_ip + 1):
                target_ip = f"{self.subnet}{i}"
                self.scan_device(target_ip)
                
        except KeyboardInterrupt:
            print("\n[!] Scan interrupted by user. Exiting...")
            sys.exit(0)

        print("-" * 70)
        print("Scan completed.")


if __name__ == "__main__":
    # ตั้งค่าวงเครือข่ายและช่วง IP ที่ต้องการสแกนใช้งานจริงตรงนี้
    scanner = CCTVFinder(subnet="192.168.1.", start=1, end=50)
    scanner.run()
