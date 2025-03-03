import qrcode

url = "https://0b14-203-159-51-249.ngrok-free.app"
qr = qrcode.make(url)
qr.save("qr_code.png")  # Lưu QR code vào file
qr.show()  # Hiển thị QR code
