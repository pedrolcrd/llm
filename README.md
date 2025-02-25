## **📌 Como configurar o projeto para rodar localmente em sua máquina**

1️⃣ **Clonar o repositório:**
```bash
git clone https://github.com/ronierisonmaciel/llm.git
cd llm
```

2️⃣ **Criar um `.env` com suas configurações locais:**
```bash
cp .env.example .env
```
✏️ **Editar o `.env` conforme necessário:**
```bash
nano .env
```
Ou no Windows:
```powershell
notepad .env
```

3️⃣ **Instalar dependências:**
```bash
pip install -r requirements.txt
```

4️⃣ **Executar o projeto:**
```bash
streamlit run app.py
```
