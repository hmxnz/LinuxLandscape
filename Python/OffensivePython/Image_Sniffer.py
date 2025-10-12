#/usr/bin/env python3

import os
from mitmproxy import http

# Directorio donde se guardarán las imágenes capturadas
IMAGE_DIR = "./captured_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Tipos MIME de imágenes comunes
IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml"
}

def response(flow: http.HTTPFlow) -> None:
    """
    Esta función se ejecuta cada vez que se recibe una respuesta HTTP(S).
    Intercepta imágenes y las guarda localmente.
    """
    content_type = flow.response.headers.get("content-type", "")

    # Verificar si la respuesta es una imagen
    if any(img_type in content_type for img_type in IMAGE_MIME_TYPES):
        print(f"🖼️  Imagen detectada: {flow.request.pretty_url}")
        
        # Generar nombre de archivo único
        filename = os.path.basename(flow.request.path)
        if not filename or "." not in filename:
            ext = content_type.split("/")[-1].split(";")[0]
            filename = f"image_{len(os.listdir(IMAGE_DIR))}.{ext}"

        filepath = os.path.join(IMAGE_DIR, filename)

        # Guardar imagen
        with open(filepath, "wb") as f:
            f.write(flow.response.content)
        print(f"💾 Imagen guardada: {filepath}")