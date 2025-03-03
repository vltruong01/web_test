import qrcode

url = "https://web-test-1-jprt.onrender.com"
qr = qrcode.make(url)
qr.save("qr_code.png")  # Lưu QR code vào file
qr.show()  # Hiển thị QR code
