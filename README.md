# FOR-EDUCATION-cctv_finder

ชุดเครื่องมือ Python สำหรับทดสอบความปลอดภัยบนอุปกรณ์เครือข่ายและ IoT  
เช่น IP Camera, DVR/NVR — ด้วยวิธีการ Port Scanning และ Device Fingerprinting

---

## Installation

```bash
pip install PySocks requests urllib3
```

---


## CCTV Network Finder

สแกนหาอุปกรณ์กล้องวงจรปิดในวง Subnet และระบุยี่ห้อด้วยวิธี **Fingerprinting**  
เหมาะสำหรับการสำรวจและจัดทำ Inventory ของอุปกรณ์ในระบบเครือข่ายภายใน

### หลักการทำงาน

ใช้สองวิธีร่วมกันเพื่อระบุตัวตนของอุปกรณ์:

**① Port-based Detection** — พอร์ต SDK เฉพาะทางของแต่ละแบรนด์

```
Port 8000  → Hikvision Device (SDK Port)
Port 37777 → Dahua Device (SDK Port)
Port 554   → Generic RTSP Stream
```

**② Web Fingerprinting** — วิเคราะห์ HTTP Response Header และ HTML Body

```
Server: hikvision-webs  → Hikvision
Body: "netsurveillance" → Xiongmai (XM)
Body: "uc-httpd"        → Xiongmai (XM)
```

### Signature Database

| Brand | Keywords ที่ใช้ตรวจจับ |
|---|---|
| Hikvision | `hikvision`, `hikvision-webs`, `app-http subsystem` |
| Dahua | `dahua`, `webservice`, `dmss` |
| Axis Communications | `axis`, `axis-neteye` |
| Xiongmai (XM) | `netsurveillance`, `uc-httpd` |
| Vivotek | `vivotek`, `network camera v` |

### Configuration

```python
scanner = CCTVFinder(
    subnet  = "192.168.1.",   # Subnet ที่ต้องการสแกน
    start   = 1,              # เริ่มที่ IP host นี้
    end     = 50,             # จบที่ IP host นี้
    timeout = 1.0             # วินาที / พอร์ต
)
scanner.run()
```

### ตัวอย่าง Output

```
----------------------------------------------------------------------
 CCTV-Finder v1.0 // Network Scanning Started
 Target Range : 192.168.1.1 - 192.168.1.50
 Timestamp    : 2025-01-15 14:32:01
----------------------------------------------------------------------
[+] IP: 192.168.1.10    | Ports: [80, 8000      ] | Identity: Hikvision Device (SDK)
[+] IP: 192.168.1.21    | Ports: [80, 554, 37777] | Identity: Dahua Device (SDK)
[+] IP: 192.168.1.33    | Ports: [80, 443       ] | Identity: Axis Communications (Web UI)
----------------------------------------------------------------------
Scan completed.
```

---

## Port Reference — กล้องวงจรปิด & IoT

### Web Management

| Port | Protocol | คำอธิบาย |
|---|---|---|
| 80 | HTTP | หน้า Web UI มาตรฐาน — เสี่ยงหากไม่เปลี่ยน Default Password |
| 443 | HTTPS | เวอร์ชัน Encrypted ของ Port 80 |
| 8080, 81, 82, 83, 88 | HTTP Alt | พอร์ตทางเลือก — มักถูกเปลี่ยนเพื่อหลบการสแกนอัตโนมัติ |

### Video Streaming

| Port | Protocol | คำอธิบาย |
|---|---|---|
| 554 | RTSP | ดึงภาพสดจากกล้อง — หากไม่มีรหัสผ่าน ดูได้ทันทีผ่าน VLC |
| 1935 | RTMP | สตรีมภาพไปยังแพลตฟอร์มออนไลน์ |

### Vendor-Specific SDK

| Port | Brand | คำอธิบาย |
|---|---|---|
| 8000 | Hikvision | เชื่อมต่อแอป iVMS และโปรแกรมจัดการ |
| 37777 | Dahua | รับส่งข้อมูลผ่านแอป DMSS |
| 9000, 5000 | Generic | กล้อง IP ทั่วไปจากผู้ผลิตจีน |

### Management & File Transfer

| Port | Protocol | คำอธิบาย |
|---|---|---|
| 21 | FTP | ส่งไฟล์ภาพ/วิดีโอขึ้น Storage Server |
| 22 | SSH | Remote Access แบบเข้ารหัส — ใช้งานโดยช่างเทคนิค |
| 23 | Telnet | Remote Access แบบ Plaintext — **อันตรายมาก** เสี่ยงต่อ Botnet |

---

## Legal Disclaimer

> เครื่องมือนี้จัดทำขึ้นเพื่อวัตถุประสงค์ด้าน **การศึกษา** และ **การทดสอบความปลอดภัย (Penetration Testing)** บนระบบที่คุณมีสิทธิ์เข้าถึงเท่านั้น
>
> **การใช้งานบนระบบหรืออุปกรณ์ที่ไม่ได้รับอนุญาตถือเป็นความผิดทางกฎหมาย**  
> ผู้พัฒนาไม่รับผิดชอบต่อความเสียหายหรือการกระทำที่ผิดกฎหมายทุกกรณี

---

## License

MIT License
