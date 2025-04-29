from dotenv import load_dotenv
import os

load_dotenv()

# 📌 Carrega .env automaticamente (faça apenas uma vez no startup, em utils.py ou logo no app)
# Caminhos defaults podem ser sobrescritos por variáveis de ambiente.
DB_PATH        = os.getenv("DB_PATH",        "banco_padrao.db")
CACHE_DB_PATH  = os.getenv("CACHE_DB_PATH",  "cache_respostas.db")
MODEL_PATH     = os.getenv("MODEL_PATH",     "modelo.pkl")
MODEL_TYPE     = os.getenv("MODEL_TYPE",     "gpt4all")        # openchat | gpt4all | deepseek
OPENCHAT_MODEL = os.getenv("OPENCHAT_MODEL", "openchat/openchat_3.5")
