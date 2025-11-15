import qrcode
import os
from datetime import datetime
from meniu import meniu_aleatoriu

from http.server import SimpleHTTPRequestHandler, HTTPServer

#/////////////////////////////////////
import http.server
import socketserver

timestamp = datetime.now()
PORT = 8000 + (timestamp.hour * 100 + timestamp.minute) % 2000

Handler = http.server.SimpleHTTPRequestHandler



fp,fs,d,total=meniu_aleatoriu()
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
    <li>Fel principal: {fp.nume} - {str(fp.pret)} lei</li>
    <li>Fel secundar: {fs.nume} - {str(fs.pret)} lei</li>
    <li>Desert: {d.nume} - {str(d.pret)} lei</li>
</ul>
<h2> Total: {str(total)} lei</h2>
</body>
</html>
"""

with open(f"page_{timp_actual}.html", "w") as f:
    f.write(html_content)


qr = qrcode.QRCode(
    version=8,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data(f'http://localhost:{PORT}')
qr.make(fit=True)
timp = datetime.now().strftime("%S%M%H")
nume = f'timp{timp}.png'
print(nume)
img = qr.make_image(fill_color="black", back_color="white")
img.save(nume)

print("Scaneaza pentru a vedea meniul:")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Local host http://localhost:{PORT}")
    httpd.serve_forever()
