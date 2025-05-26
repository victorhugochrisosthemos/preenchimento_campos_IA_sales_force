import pandas as pd
from nltk.corpus import stopwords
import string
import unicodedata


# Carregar os dados
dados = pd.read_excel('C:/Users/Victor/Desktop/Intelbras/testes_python/projeto_talk_desk/teste5.xlsx')

# [10416 rows x 5 columns]
# ['produto', 'corpo', 'motivo do caso', 'acao', 'diagnostico']

# Função de pré-processamento melhorada
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

def limpar_texto(texto):
    if isinstance(texto, str):
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto
    return texto

# Aplicar pré-processamento
dados['corpo'] = dados['corpo'].apply(preprocess_text)
dados['motivo do caso'] = dados['motivo do caso'].apply(limpar_texto)
dados['acao'] = dados['acao'].apply(limpar_texto)
dados['diagnostico'] = dados['diagnostico'].apply(limpar_texto)

print(dados)
print(dados.columns.tolist())

# Salvar o DataFrame como CSV
dados.to_csv('C:/Users/Victor/Desktop/Intelbras/testes_python/projeto_talk_desk/dados_processados.csv', index=False, encoding='utf-8-sig')
