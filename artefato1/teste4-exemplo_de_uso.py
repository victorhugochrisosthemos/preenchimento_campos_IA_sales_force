from joblib import load
import os
from nltk.corpus import stopwords
import string
import unicodedata

# Função para carregar todos os modelos
def carregar_modelos():
    modelos = {}
    colunas_alvo = ['produto', 'motivo do caso', 'acao', 'diagnostico']
    
    for coluna in colunas_alvo:
        nome_arquivo = f'modelos_treinados/modelo_{coluna.replace(" ", "_")}.joblib'
        try:
            modelos[coluna] = load(nome_arquivo)
            print(f"Modelo {coluna} carregado com sucesso")
        except FileNotFoundError:
            print(f"Modelo {coluna} não encontrado")
            modelos[coluna] = None
    
    return modelos

# Função para fazer previsões
def sugerir_campos(texto_corpo, modelos):
    sugestoes = {}
    for coluna, modelo in modelos.items():
        if modelo is not None:
            try:
                sugestoes[coluna] = modelo.predict([texto_corpo])[0]
            except:
                sugestoes[coluna] = "nao foi possivel sugerir"
        else:
            sugestoes[coluna] = "modelo nao disponivel"
    return sugestoes

# Carregar modelos
modelos_carregados = carregar_modelos()

def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    # Converter para minúsculas
    text = text.lower()

    # Remover pontuação
    text = text.translate(str.maketrans('', '', string.punctuation))

    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    # Tokenização e remoção de stopwords
    try:
        stop_words = set(stopwords.words('portuguese'))
        tokens = [word for word in text.split() if word not in stop_words]
    except:
        # Fallback básico
        basic_stopwords = {'de', 'a', 'o', 'que', 'e', 'é', 'do', 'da', 'em', 'um'}
        tokens = [word for word in text.split() if word not in basic_stopwords]

    return ' '.join(tokens)

# Exemplo de uso
if modelos_carregados:
    texto_exemplo = "meu telefone não está fazendo chamadas"
    texto_exemplo = preprocess_text(texto_exemplo)
    sugestoes = sugerir_campos(texto_exemplo, modelos_carregados)
    
    print("\nSugestao para o texto inserido:")
    for campo, valor in sugestoes.items():
        print(f"{campo}: {valor}")