import cv2
import numpy as np
import os
import qrcode

# === 1. Carica le immagini con controlli ===

# Carica immagine da inserire
img = cv2.imread('nature.png')
if img is None:
    raise FileNotFoundError("Errore: 'nature.png' non trovato o non leggibile")

hh, ww = img.shape[:2]

# Carica cornice con canale alfa
frame = cv2.imread('frame.png', cv2.IMREAD_UNCHANGED)
if frame is None:
    raise FileNotFoundError("Errore: 'frame.png' non trovato o non leggibile")

# === 2. Trova l’area trasparente (dove inserire l’immagine) ===

# Separa canale BGR e alpha
alpha = frame[:, :, 3]

# Soglia il canale alfa per trovare l’area trasparente
thresh = cv2.threshold(alpha, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Pulizia con morfologia
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Trova i contorni
contours = cv2.findContours(morph, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
small_contour = min(contours, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(small_contour)

# === 3. Adatta l’immagine da inserire mantenendo le proporzioni ===

# Calcola fattore di scala mantenendo aspect ratio
scale = min(w / ww, h / hh)
new_ww = int(ww * scale)
new_hh = int(hh * scale)

# Ridimensiona l’immagine da inserire
img_resized = cv2.resize(img, (new_ww, new_hh), interpolation=cv2.INTER_AREA)

# Converte in BGRA
img2 = cv2.cvtColor(img_resized, cv2.COLOR_BGR2BGRA)

# === 4. Prepara la cornice da riempire ===

# Copia della cornice
result = frame.copy()

# Calcola l’offset per centrare l’immagine dentro la finestra trovata
xoff = x + (w - new_ww) // 2
yoff = y + (h - new_hh) // 2

# Inserisce l’immagine nella cornice
result[yoff:yoff + new_hh, xoff:xoff + new_ww] = img2

# === 5. Salva solo il risultato ===

output_file = "frame_with_picture.png"
cv2.imwrite(output_file, result)


# === 6. Genera un QR code che punta al file immagine ===

def genera_qr_con_immagine(percorso_file):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Inserisce il percorso del file nel QR
    qr.add_data(percorso_file)
    qr.make(fit=True)

    # Crea l'immagine del QR
    img_qr = qr.make_image(fill='black', back_color='white')

    # Salva l'immagine QR
    qr_output = 'qr_code.png'
    img_qr.save(qr_output)

    # Mostra il QR
    img_qr.show()
    print(f"QR code generato e salvato come {qr_output}")


# Chiama la funzione per generare il QR code#
# genera_qr_con_immagine(output_file)
