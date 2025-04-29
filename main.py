from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
import layoutparser as lp
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Carga de modelo YOLO
model = YOLO('modelos/yolov8n.pt')

@app.route('/analizar-plano', methods=['POST'])
def analizar_plano():
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió un archivo'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    try:
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        results = model(img)

        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    'clase': int(box.cls[0]),
                    'confianza': float(box.conf[0]),
                    'coordenadas': box.xyxy[0].tolist()
                })

        image_pil = Image.open(io.BytesIO(in_memory_file.getvalue()))
        model_lp = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config')
        layout = model_lp.detect(image_pil)

        layout_info = []
        for block in layout:
            layout_info.append({
                'tipo': block.type,
                'coordenadas': block.coordinates
            })

        return jsonify({
            'detecciones_yolo': detections,
            'estructuras_layoutparser': layout_info
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "NeuroPlan Analyzer Backend Funcionando ✅"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
