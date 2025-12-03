import cv2
import numpy as np
from flask import Response, Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Configuração da área de invasão (Polígono)
P1, P2, P3, P4 = (100, 100), (400, 100), (400, 400), (100, 400)
PONTOS_POLIGONO = np.array([P1, P2, P3, P4], np.int32).reshape(-1, 1, 2)

# Subtrator de fundo
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

# Variáveis de controle
contador_intrusoes = 0
AREA_MINIMA_DETECCAO = 2000
ALTURA_MIN_PESSOA = 40
PROPORCAO_MIN_LARGURA = 0.35
CAMERA_INDEX = 2 # <-- Tentativa inicial com a câmera padrão

def esta_invadido(cx, cy):
    """Verifica se o ponto está dentro da área de invasão"""
    return cv2.pointPolygonTest(PONTOS_POLIGONO, (cx, cy), False) >= 0


def gerar_frames():
    """Gera frames continuamente da webcam"""
    global contador_intrusoes
    
    # Inicializa a captura da webcam
    cap = cv2.VideoCapture(CAMERA_INDEX) 

    if not cap.isOpened():
        print(f"ERRO: Não foi possível abrir a webcam (índice {CAMERA_INDEX}).")
        # Se a câmera não abrir, retorna imediatamente
        return

    while True:
        ret, frame = cap.read()
        
        # Correção 1: Se o frame falhar na leitura (câmera desconectada), 
        # sai do loop para liberar o recurso.
        if not ret:
            print("Webcam falhou na leitura. Encerrando o stream.")
            break 

        # Processamento e Detecção de Movimento (MOG2)
        fgmask = fgbg.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        fgmask = cv2.dilate(fgmask, kernel, iterations=2)
        contornos, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contorno in contornos:
            if cv2.contourArea(contorno) < AREA_MINIMA_DETECCAO:
                continue

            (x, y, w, h) = cv2.boundingRect(contorno)
            cx, cy = x + w // 2, y + h
            cor = (0, 0, 255) 
            
            if h >= ALTURA_MIN_PESSOA and h > w * 1.2 and w > h * PROPORCAO_MIN_LARGURA:
                if esta_invadido(cx, cy):
                    contador_intrusoes += 1
                    cor = (0, 255, 0) 
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)

        # Desenha o polígono e o contador
        cv2.polylines(frame, [PONTOS_POLIGONO], True, (0, 0, 255), 2)
        cv2.putText(frame, f'Intrusoes: {contador_intrusoes}', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Codifica o frame e envia no stream MJPEG
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    # Correção 2: Garante que o recurso da câmera seja liberado ao sair do loop
    cap.release()
    print("Webcam liberada e Monitoramento.py encerrado.")


@app.route('/video_feed')
def video_feed():
    """Endpoint de vídeo em tempo real"""
    return Response(gerar_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def home():
    return jsonify({'status': 'Servidor de vídeo rodando!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)