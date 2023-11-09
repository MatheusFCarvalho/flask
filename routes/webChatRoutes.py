from flask import request, jsonify, Blueprint, Flask, render_template
from flask_socketio import SocketIO

web_chat_bp = Blueprint('webChat', __name__)

# Crie um objeto Flask para a aplicação do Blueprint
web_chat_app = Flask(__name__)

# Inicialize o SocketIO na aplicação Flask
socketio = SocketIO(web_chat_app)


@web_chat_bp.route('/chat')
def chat():
    return render_template('chat.html')


@web_chat_bp.route('/pcp_chat')
def pcp_chat():
    return render_template('pcp_chat.html')

# Resto do código permanece inalterado


# Inicie a aplicação Flask
if __name__ == '__main__':
    socketio.run(web_chat_app, debug=True)


# Defina funções para manipular eventos WebSocket, como enviar e receber mensagens
@socketio.on('message')
def handle_message(message):
    # Lógica para lidar com mensagens
    print("Mensagem Recebida:", message)
    socketio.emit('message', message, broadcast=True)


@socketio.on('pcp_message')
def handle_pcp_message(message):
    # Lógica para lidar com mensagens PCP
    print("Mensagem PCP Recebida:", message)
    socketio.emit('pcp_message', message, broadcast=True)


# Inicie a aplicação SocketIO
socketio.init_app(web_chat_bp.app)

# Inicie a aplicação Flask
if __name__ == '__main__':
    socketio.run(web_chat_bp.app, debug=True)
