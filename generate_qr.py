# generate_qr.py
import qrcode
from PIL import Image

# Votre URL Streamlit (remplacez par votre URL réelle)
# Pour développement local
streamlit_url = "https://ai-logic-lab.streamlit.app/"

# Pour déploiement cloud (Streamlit Cloud, Hugging Face, etc.)
# streamlit_url = "https://votre-app.streamlit.app"

# Créer le QR code
qr = qrcode.QRCode(
    version=1,  # Taille du QR (1-40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,  # Taille de chaque boîte en pixels
    border=4,     # Bordure (minimum 4)
)

qr.add_data(streamlit_url)
qr.make(fit=True)

# Créer l'image QR
qr_image = qr.make_image(fill_color="black", back_color="white")

# Sauvegarder l'image
qr_image.save("streamlit_qr.png")

# Pour un QR plus stylisé avec logo
def create_styled_qr(url, logo_path=None):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Haute correction pour logo
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Créer l'image QR
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Ajouter un logo si fourni
    if logo_path:
        logo = Image.open(logo_path)
        
        # Calculer la taille du logo (max 30% du QR)
        logo_size = int(qr_img.size[0] * 0.3)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Positionner le logo au centre
        pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
        qr_img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)
    
    return qr_img

# QR avec logo
# qr_with_logo = create_styled_qr(streamlit_url, "logo.png")
# qr_with_logo.save("streamlit_qr_styled.png")