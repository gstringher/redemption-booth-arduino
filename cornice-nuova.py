from PIL import Image


def crea_santino():
    # Crea un'immagine vuota 1000x2000 px, bianca
    base = Image.new("RGB", (1000, 2000), "white")

    # Carica 'generata.jpg' e ridimensionala a 800x1600 px
    generata = Image.open("generata.jpg").resize((800, 1600))

    # Incolla l'immagine ridimensionata alle coordinate (100, 100)
    base.paste(generata, (70, 70))

    # Carica 'cornice.png' (che può avere trasparenza)
    cornice = Image.open("frame.png").convert("RGBA")

    # Converte la base in RGBA per supportare l'alpha channel temporaneamente
    base = base.convert("RGBA")

    # Sovrapponi la cornice alla base mantenendo la trasparenza
    base.alpha_composite(cornice, dest=(0, 0))

    # Converti di nuovo in RGB per salvare in formato JPEG (che non supporta trasparenza)
    base = base.convert("RGB")

    # Salva l'immagine risultante
    base.save("santino.jpg", "JPEG")


# Esegui la funzione
crea_santino()
