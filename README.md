# Surveillance-Camera

Raspberry Pi จะทำการรับค่า message จาก mqtt ถ้าเป็นข้อความตามที่ได้กำหนดไว้ จะทำการเปลี่ยน state จากสถานะ idle เป็น recording ถ้าได้รับค่าอีกรอบจะทำการหยุดอัดวิดีโอ แล้วจะทำการเปลี่ยนสถานะกลับมาเป็น idle พร้อมทำการ upload ไฟล์วิดีโอ (.h264) ขึ้น Google Drive

## Diagram ตัวอย่างการนำไปประยุกต์ใช้

<img src="/README/Micro.png">

## วิธีการติดตั้ง

- git clone `https://github.com/chattida/Surveillance-Camera.git`
- แก้ไข path ที่เก็บ Video ที่บันทึก และ topic ของ MQTT ใน `main.py`
- pip3 install paho-mqtt
- pip3 install picamera
- pip3 install pytz
- pip3 install RPi.GPIO
- ทำการติดตั้ง Rclone พร้อมกับตั้งค่าให้เรียบร้อย
- แก้ไข path และ remote ใน `sync.py`
- python3 `main.py`

---

นางสาวฉัตรธิดา แจ้งใจ รหัสนักศึกษา 61070029
