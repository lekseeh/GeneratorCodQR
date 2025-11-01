import qrcode
import os
from meniu import meniu_aleatoriu

fp,fs,d,total=meniu_aleatoriu()

with open("link.html", "r", encoding="utf-8") as f:
    html_content = f.read()
html_content = (
    html_content
    .replace("{{fel_principal}}", fp.nume)
    .replace("{{pret_principal}}", str(fp.pret))
    .replace("{{fel_secundar}}", fs.nume)
    .replace("{{pret_secundar}}", str(fs.pret))
    .replace("{{desert}}", d.nume)
    .replace("{{pre_desert}}", str(d.pret))
    .replace("{{total}}", str(total))
)

with open("link.html", "w", encoding="utf-8") as f:
    f.write(html_content)

file_path = os.path.abspath("link.html")

qr = qrcode.QRCode(
    version=8,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data(f'file://{file_path}')
qr.make()
img = qr.make_image(fill_color="black", back_color="white")
img.save('qrcode_meniu.png')

print("Scaneaza pentru a vedea meniu:", file_path)
