from flask import Flask, jsonify, request
import os
import subprocess

app = Flask(__name__)

# Diretório onde os pacotes Python estão armazenados
PACKAGES_DIR = 'packages'

@app.route('/')
def home():
    return "Servidor Flask em execução!"

@app.route('/instalar/<package_name>', methods=['GET'])
def install_package(package_name):
    # Caminho completo para o arquivo do pacote
    package_path = os.path.join(PACKAGES_DIR, f"{package_name}.py")
    
    if os.path.isfile(package_path):
        try:
            # Executa o arquivo Python como um subprocesso
            subprocess.run(['python', package_path], check=True)
            return jsonify({"message": f"Pacote '{package_name}' instalado e executado com sucesso!"}), 200
        except subprocess.CalledProcessError:
            return jsonify({"message": f"Erro ao executar o pacote '{package_name}'."}), 500
    else:
        return jsonify({"message": f"Pacote '{package_name}' não encontrado."}), 404

if __name__ == '__main__':
    # Certifica-se de que o diretório de pacotes existe
    if not os.path.exists(PACKAGES_DIR):
        os.makedirs(PACKAGES_DIR)
    app.run(debug=True)