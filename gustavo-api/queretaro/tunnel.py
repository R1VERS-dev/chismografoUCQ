# tunnel.py
import os
from dotenv import load_dotenv
from pyngrok import ngrok, conf

load_dotenv()
token = os.getenv("NGROK_AUTH_TOKEN")
if not token:
    print("❌ NGROK_AUTH_TOKEN no está definido en .env")
    exit(1)

# Si descargaste ngrok.exe manualmente, descomenta y ajusta la línea siguiente:
# conf.get_default().ngrok_path = os.path.join(os.getcwd(), "ngrok.exe")

ngrok.set_auth_token(token)
tunnel = ngrok.connect(8000, bind_tls=True)
print(f"🔌 Ngrok tunnel disponible en: {tunnel.public_url}")

# Mantén el túnel vivo hasta que presiones ENTER
print("Presiona ENTER para detener el túnel")
input()

# Cuando presiones ENTER, cierra el túnel
ngrok.disconnect(tunnel.public_url)
print("🛑 Tunnel detenido")
