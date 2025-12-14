import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
import qrcode
from io import BytesIO
import base64
import socket

app = FastAPI()

# --- CONFIGURARE ---
PORT_FIX = 8000
IP_HOST = "192.168.100.50"

# Stocare temporară în memorie (dicționar) pentru meniurile create
# Cheia va fi ID-ul meniului, Valoarea va fi un dict cu detaliile
menu_storage = {}


@app.get("/", response_class=HTMLResponse)
def get_form():

    html_content = """
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generator Meniu QR</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 500px; margin: 20px auto; padding: 20px; }
            input { width: 100%; padding: 8px; margin: 5px 0 15px 0; box-sizing: border-box; }
            button { width: 100%; padding: 10px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            h2 { color: #333; }
        </style>
    </head>
    <body>
        <h2>Creare Meniu Nou</h2>
        <form action="/generare" method="post">
            <label>Fel principal:</label>
            <input type="text" name="fp_nume" required>
            <label>Preț Fel principal (lei):</label>
            <input type="number" step="0.01" name="fp_pret" required>

            <label>Fel secundar:</label>
            <input type="text" name="fs_nume" required>
            <label>Preț Fel secundar (lei):</label>
            <input type="number" step="0.01" name="fs_pret" required>

            <label>Desert:</label>
            <input type="text" name="d_nume" required>
            <label>Preț Desert (lei):</label>
            <input type="number" step="0.01" name="d_pret" required>

            <button type="submit">Generează Meniu & QR</button>
        </form>
    </body>
    </html>
    """
    return html_content


@app.post("/generare", response_class=HTMLResponse)
def generate_menu(
        fp_nume: str = Form(...), fp_pret: float = Form(...),
        fs_nume: str = Form(...), fs_pret: float = Form(...),
        d_nume: str = Form(...), d_pret: float = Form(...)
):
    # Primește datele din formular, salvează meniul în memorie și afișează codul QR.
    # Calcul total
    total = fp_pret + fs_pret + d_pret

    # Generăm un ID unic simplu bazat pe numărul de elemente
    menu_id = len(menu_storage) + 1

    # Salvăm datele
    menu_storage[menu_id] = {
        "fp_nume": fp_nume, "fp_pret": fp_pret,
        "fs_nume": fs_nume, "fs_pret": fs_pret,
        "d_nume": d_nume, "d_pret": d_pret,
        "total": total
    }

    # Creare link pentru QR
    qr_link = f"http://{IP_HOST}:{PORT_FIX}/meniu/{menu_id}"

    # Generare imagine QR
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#ed0e54", back_color="#ebbecc")

    # Convertim imaginea în base64 pentru a o afișa direct în HTML fără a o salva pe disc
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Cod QR Generat</title></head>
    <body style="text-align:center; font-family: Arial;">
        <h1>Meniul a fost creat!</h1>
        <p>Scanează codul de mai jos pentru a vedea meniul:</p>
        <img src="data:image/png;base64,{img_str}" alt="QR Code" />
        <br><br>
        <p><small>Link direct: <a href="{qr_link}">{qr_link}</a></small></p>
        <br>
        <a href="/">Creează alt meniu</a>
    </body>
    </html>
    """


@app.get("/meniu/{menu_id}", response_class=HTMLResponse)
def view_menu(menu_id: int):

    #Aceasta este pagina pe care o vede clientul când scanează codul QR.
    #Datele sunt preluate din memorie pe baza ID-ului.

    menu = menu_storage.get(menu_id)

    if not menu:
        return "<h1>Meniul nu a fost găsit sau a expirat.</h1>"

    return f"""
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Meniul zilei</title>
        <style>
            body {{ font-family: 'Helvetica', sans-serif; padding: 20px; background-color: #f9f9f9; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            h1 {{ color: #d35400; text-align: center; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ padding: 10px 0; border-bottom: 1px solid #eee; font-size: 1.1em; }}
            .price {{ float: right; font-weight: bold; color: #2c3e50; }}
            h2.total {{ text-align: right; margin-top: 20px; color: #27ae60; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍽️ Meniul Zilei</h1>
            <ul>
                <li>Fel principal: <strong>{menu['fp_nume']}</strong> <span class="price">{menu['fp_pret']} lei</span></li>
                <li>Fel secundar: <strong>{menu['fs_nume']}</strong> <span class="price">{menu['fs_pret']} lei</span></li>
                <li>Desert: <strong>{menu['d_nume']}</strong> <span class="price">{menu['d_pret']} lei</span></li>
            </ul>
            <h2 class="total"> Total: {menu['total']} lei</h2>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    # Rulare server
    print(f"Server pornit. Acceseaza http://{IP_HOST}:{PORT_FIX} pentru a crea meniul.")
    uvicorn.run(app, host="0.0.0.0", port=PORT_FIX)