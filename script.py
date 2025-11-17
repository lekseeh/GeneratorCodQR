import qrcode
import os
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
import http.server
import socketserver

#handler care redirectioneaza catre ultimul fisier html generat
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", f"/{filename}")
            self.end_headers()
        else:
            super().do_GET()


timestamp = datetime.now()
PORT = 8000 + (timestamp.hour * 100 + timestamp.minute) % 2000

#generare html cu meniu
fp_nume = input("Scrie felul principal: ")
fp_pret = float(input("Pret fel principal: "))

fs_nume = input("Scrie felul secundar: ")
fs_pret = float(input("Pret fel secundar: "))

d_nume = input("Scrie desertul: ")
d_pret = float(input("Pret desert: "))

total = fp_pret + fs_pret + d_pret
timp_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"page_{timp_actual}.html"

html_content = f"""


<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Meniul zilei</title>
</head>
<body>
<h1>Meniul zilei</h1>
<ul>
    <li>Fel principal: {fp_nume} - {str(fp_pret)} lei</li>
    <li>Fel secundar: {fs_nume} - {str(fs_pret)} lei</li>
    <li>Desert: {d_nume} - {str(d_pret)} lei</li>
</ul>
<h2> Total: {str(total)} lei</h2>
</body>
</html>
"""

with open(f"page_{timp_actual}.html", "w") as f:
    f.write(html_content)

#generare qr code
qr = qrcode.QRCode(
    version=8,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data(f'http://localhost:{PORT}/{filename}')
qr.make(fit=True)
timp = datetime.now().strftime("%S%M%H")
nume = f'qr{timp}.png'
print(nume)
img = qr.make_image(fill_color="black", back_color="white")
img.save(nume)

#pornire server
print("Scaneaza pentru a vedea meniul:")
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Local host http://localhost:{PORT}/{filename}")
    httpd.serve_forever()
