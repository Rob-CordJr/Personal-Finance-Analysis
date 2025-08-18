import os
import subprocess

def install_requirements():
    """Instala as dependências do requirements.txt."""
    req_file = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
    if os.path.exists(req_file):
        print("📦 Instalando dependências do requirements.txt...")
        subprocess.check_call(["pip", "install", "-r", req_file])
    else:
        print("⚠️ Arquivo requirements.txt não encontrado.")

def download_dataset():
    """Faz download do dataset de finanças pessoais via Kaggle API."""
    print("⬇️ Baixando dataset do Kaggle...")
    
    # Verifica se as credenciais da Kaggle existem
    kaggle_dir = os.path.expanduser('~/.kaggle')
    kaggle_json = os.path.join(kaggle_dir, 'kaggle.json')
    
    if not os.path.exists(kaggle_json):
        raise FileNotFoundError(
            "Arquivo kaggle.json não encontrado. "
            "Por favor, crie um token API em https://www.kaggle.com/docs/api "
            "e coloque o arquivo kaggle.json em ~/.kaggle/"
        )
    
    artifacts_dir = os.path.join(os.path.dirname(__file__), "..", "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)

    try:
        subprocess.check_call([
            "kaggle", "datasets", "download", "-d", "miadul/personal-finance-ml-dataset",
            "-p", artifacts_dir, "--unzip"
        ])
        print(f"✅ Dataset baixado e salvo em: {artifacts_dir}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao baixar o dataset: {e}")
        raise

if __name__ == "__main__":
    install_requirements()
    download_dataset()
    print("🚀 Setup concluído!")
