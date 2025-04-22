import os
import streamlit as st
from model_loader import ModelLoader  # Importa o carregador dinâmico
from database.database import query_database, buscar_resposta_cache, salvar_resposta
from cache.cache import get_database_schema
from config.config import MODEL_PATH

# 🔄 Carrega o modelo (OpenChat ou GPT4All) baseado em MODEL_TYPE
model = ModelLoader()

def generate_response(user_question):
    """Gera uma resposta usando o modelo selecionado + contexto do banco de dados."""
    
    # 1. Verifica se a pergunta está vazia
    if not user_question.strip():
        return "❌ Por favor, insira uma pergunta válida."

    # 2. Busca resposta no cache (se existir)
    resposta_cache = buscar_resposta_cache(user_question)
    if resposta_cache:
        return f"📌 **Resposta recuperada do histórico:**\n\n{resposta_cache}"

    # 3. Obtém a estrutura do banco de dados
    schema = get_database_schema()
    if not schema:
        return "❌ Erro ao buscar a estrutura do banco de dados."

    # 4. Identifica a tabela relevante com base na pergunta
    table_to_query = None
    for table in schema.keys():
        if table.lower() in user_question.lower():
            table_to_query = table
            break

    # Se nenhuma tabela for encontrada, lista as disponíveis
    if not table_to_query:
        return f"📊 O banco contém as seguintes tabelas:\n" + "\n".join([f"- {table}" for table in schema.keys()])

    # 5. Consulta o banco de dados (limita a 5 registros para otimização)
    columns = ", ".join(schema[table_to_query][:5])  # Pega as primeiras 5 colunas
    query = f'SELECT {columns} FROM "{table_to_query}" ORDER BY ROWID DESC LIMIT 5;'
    result = query_database(query)

    if isinstance(result, str):
        return result  # Retorna mensagem de erro SQL (se houver)

    # 6. Prepara o prompt para o modelo (OpenChat/GPT4All)
    dados_texto = "\n".join([", ".join(map(str, row)) for row in result])
    prompt = f"""
    Você é um assistente especializado em bancos de dados. 
    Aqui estão os últimos registros da tabela '{table_to_query}':

    {dados_texto}

    Com base nesses dados, responda de forma clara e concisa:
    "{user_question}"
    """

    # 7. Gera a resposta usando o modelo carregado
    try:
        resposta = model.generate(prompt).strip()
        salvar_resposta(user_question, resposta)  # Salva no cache
        return resposta
    except Exception as e:
        return f"❌ Erro ao gerar resposta: {str(e)}"
