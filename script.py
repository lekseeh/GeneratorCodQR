import qrcode

qr = qrcode.QRCode(
    version=8,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data('https://www.formula1.com/')
qr.make()
img = qr.make_image(fill_color="#2754F5", back_color="#27E0F5")
img.save('qrcode_test2_2.png')
