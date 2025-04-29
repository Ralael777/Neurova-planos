PASOS PARA USAR ESTE BACKEND EN RENDER.COM

1. Sube esta carpeta como un repositorio a tu cuenta de GitHub.

2. Entra a https://render.com, crea una cuenta si no tienes una.

3. Haz clic en "New Web Service" y selecciona "Deploy from GitHub".

4. Elige este repositorio y configura:
   - Runtime: Python 3
   - Start Command: gunicorn main:app --bind 0.0.0.0:$PORT
   - Build Command: pip install -r requirements.txt

5. Espera a que Render instale todo y te dé tu URL pública.

6. Prueba subiendo un archivo .jpg o .png a la ruta:
   https://TU-URL.onrender.com/analizar-plano
