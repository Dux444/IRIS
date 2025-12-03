from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import platform # Importe o módulo platform
# Assumindo que seu arquivo bancodados.py está no mesmo diretório
from bancodados import criar_banco, cadastrar_usuario, validar_login, editar_senha, usuario_existe 

app = Flask(__name__)
CORS(app)

criar_banco()

# IMPORTANTE: Confirme o caminho exato para o seu executável Python
PYTHON_EXECUTABLE = "C:/Users/ander/AppData/Local/Programs/Python/Python313/python.exe" 
# O nome do script de monitoramento
WEBCAM_SCRIPT_NAME = "Monitoramento.py" 

monitoramento_process = None

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')

    if not nome or not senha:
        return jsonify({'error': 'Preencha todos os campos!'}), 400
    if usuario_existe(nome):
        return jsonify({'error': 'Usuário já cadastrado!'}), 400

    messagem = cadastrar_usuario(nome, senha)
    return jsonify({'messagem': messagem}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')

    if validar_login(nome, senha):
        return jsonify({'message': 'Login realizado com sucesso!'}), 200
    else:
        return jsonify({'error': 'Usuário ou senha incorretos.'}), 401


@app.route('/recover', methods=['POST'])
def recover():
    data = request.get_json()
    nome = data.get('nome')
    nova_senha = data.get('nova_senha')

    if not usuario_existe(nome):
        return jsonify({'error': 'Usuário não encontrado!'}), 404

    editar_senha(nome, nova_senha)
    return jsonify({'message': 'Senha atualizada com sucesso!'}), 200


@app.route('/')
def home():
    return jsonify({'status': 'API Flask rodando!'}), 200

# --- ROTAS DE CONTROLE DE MONITORAMENTO ---

@app.route('/start', methods=['POST'])
def start_monitoramento():
    global monitoramento_process

    # Verifica se o processo já está rodando (poll() retorna None se ativo)
    if monitoramento_process is None or monitoramento_process.poll() is not None:
        
        # Se o processo anterior falhou e poll() retornou um código de saída, limpa a variável
        if monitoramento_process and monitoramento_process.poll() is not None:
            monitoramento_process = None 
            
        caminho_script = os.path.abspath(WEBCAM_SCRIPT_NAME) 

        if not os.path.exists(caminho_script):
            return jsonify({'error': f'Script não encontrado: {caminho_script}'}), 500
        
        # Define flags de criação de processo para Windows para melhor controle
        flags = 0
        if platform.system() == "Windows":
            flags = subprocess.CREATE_NEW_PROCESS_GROUP

        try:
            # Popen agora usa a flag e a lista de comandos
            monitoramento_process = subprocess.Popen(
                [PYTHON_EXECUTABLE, caminho_script], 
                shell=True,
                creationflags=flags
            ) 
            return jsonify({'message': 'Monitoramento iniciado com sucesso!'}), 200
        except Exception as e:
            # CORREÇÃO CRÍTICA: Se a iniciação falhar, garanta que a variável seja limpa
            monitoramento_process = None 
            return jsonify({'error': f'Falha ao iniciar subprocesso: {str(e)}'}), 500
            
    else:
        # Resposta 400 que o App estava recebendo se o processo não foi limpo
        return jsonify({'message': 'Monitoramento já está em execução.'}), 400


@app.route ('/stop', methods=['POST'])
def stop_monitoramento():
    global monitoramento_process
    if monitoramento_process:
        try:
            # 1. Tenta encerrar normalmente
            monitoramento_process.terminate()
            
            # 2. CORREÇÃO ROBUSTA: Usa taskkill no Windows para matar o processo pelo PID e seus filhos
            if platform.system() == "Windows":
                 pid = monitoramento_process.pid 
                 # taskkill /F (força) /T (termina processo e filhos)
                 subprocess.run(f"taskkill /F /PID {pid} /T", shell=True, check=False)

            # 3. Força o fim (Fallback para sistemas não-Windows ou se taskkill falhar)
            monitoramento_process.kill()
            
        except Exception as e:
            # Se já estiver morto ou houver outro erro, apenas registra
            print(f"Erro ao encerrar subprocesso: {e}") 
        
        # Garante que a variável global seja limpa
        monitoramento_process = None
        return jsonify({'message': 'Monitoramento encerrado com sucesso!'}), 200
    else:
        return jsonify({'message': 'Nenhum monitoramento em execução.'}), 400

@app.route('/status', methods=['GET'])
def status_monitoramento():
    global monitoramento_process
    if monitoramento_process:
        if monitoramento_process.poll() is None:
            return jsonify({'status': 'em execução', 'pid': monitoramento_process.pid}), 200
        else:
            # Se o processo terminou por conta própria, limpa a variável
            monitoramento_process = None
            return jsonify({'status': 'parado - falha de subprocesso'}), 200
    else:
        return jsonify({'status': 'parado'}), 200

if __name__ == '__main__':
    # Roda o servidor principal (API de controle) na porta 5000
    app.run(host='0.0.0.0', port=5000)