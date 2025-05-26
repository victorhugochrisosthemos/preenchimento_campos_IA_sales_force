import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from joblib import dump
import os

# Carregar os dados
dados = pd.read_csv('C:/Users/Victor/Desktop/Intelbras/testes_python/projeto_talk_desk/dados_processados.csv')

# Remover linhas onde 'corpo' é NaN
dados = dados.dropna(subset=['corpo'])

# Criar diretório para salvar os modelos se não existir
os.makedirs('modelos_treinados', exist_ok=True)

# Criar modelos para cada coluna a ser prevista
colunas_alvo = ['produto', 'motivo do caso', 'acao', 'diagnostico']
modelos = {}

for coluna in colunas_alvo:
    print(f"Treinando modelo para: {coluna}")
    
    # Remover linhas onde a coluna alvo é NaN
    dados_validos = dados.dropna(subset=[coluna])
    
    if len(dados_validos) == 0:
        print(f"Não há dados válidos para treinar o modelo de {coluna}")
        continue
    
    # Criar e treinar o pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', OneVsRestClassifier(LogisticRegression(max_iter=1000)))
    ])
    
    pipeline.fit(dados_validos['corpo'], dados_validos[coluna])
    
    # Salvar o modelo em arquivo
    nome_arquivo = f'modelos_treinados/modelo_{coluna.replace(" ", "_")}.joblib'
    dump(pipeline, nome_arquivo)
    print(f"Modelo salvo em: {nome_arquivo}")

print("\nTodos os modelos foram treinados e salvos com sucesso!")