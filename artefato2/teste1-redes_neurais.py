import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
import string
import os
import joblib
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
import numpy as np

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = {'de', 'a', 'o', 'que', 'e', 'é', 'do', 'da', 'em', 'um', 'para'}
    tokens = [word for word in text.split() if word not in stop_words]
    return ' '.join(tokens)

def treinar_e_salvar_modelo_nn():
    # Carregar dados
    dados = pd.read_excel('C:/Users/Victor/Desktop/Intelbras/testes_python/preenchimento_dados/teste5.xlsx')

    # Verificar colunas
    required_columns = ['corpo', 'produto', 'motivo do caso', 'acao', 'diagnostico']
    if not all(col in dados.columns for col in required_columns):
        missing = [col for col in required_columns if col not in dados.columns]
        raise ValueError(f'Colunas faltando: {missing}')

    # Pré-processamento
    dados['Corpo_Processado'] = dados['corpo'].apply(preprocess_text)
    dados_filtrados = dados[dados['produto'].isin(dados['produto'].value_counts()[dados['produto'].value_counts() >= 2].index)].copy()

    # Vetorização
    vectorizer = TfidfVectorizer(max_features=370)
    X = vectorizer.fit_transform(dados_filtrados['Corpo_Processado']).toarray()

    # OneHot para targets - com sparse_output=False para matriz densa
    ohe = OneHotEncoder(sparse_output=False)
    y_encoded = ohe.fit_transform(dados_filtrados[['produto', 'motivo do caso', 'acao', 'diagnostico']])

    # Armazenar o número de classes por saída
    output_dims = [len(dados_filtrados[col].unique()) for col in ['produto', 'motivo do caso', 'acao', 'diagnostico']]
    
    # Separar saídas para arquitetura e converter para float32
    y_separated = []
    start = 0
    for dim in output_dims:
        y_separated.append(y_encoded[:, start:start+dim].astype(np.float32))
        start += dim

    # Criar rede neural com ReLU
    input_layer = Input(shape=(X.shape[1],))
    x = Dense(256, activation='relu')(input_layer)
    x = Dense(128, activation='relu')(x)

    outputs = [Dense(dim, activation='softmax', name=f'output_{i}')(x) for i, dim in enumerate(output_dims)]

    model = Model(inputs=input_layer, outputs=outputs)
    
    # Compilar com métricas para cada saída
    model.compile(optimizer=Adam(0.001),
                 loss='categorical_crossentropy',
                 metrics=['accuracy'] * len(outputs))  # Uma métrica para cada saída

    # Treinar modelo
    model.fit(X, y_separated, epochs=20, batch_size=32, verbose=1)

    # Salvar componentes
    os.makedirs('modelo_salvo', exist_ok=True)
    model.save('modelo_salvo/modelo_nn.h5')
    joblib.dump(vectorizer, 'modelo_salvo/vectorizer.joblib')
    joblib.dump(ohe, 'modelo_salvo/onehot_encoder.joblib')
    joblib.dump(output_dims, 'modelo_salvo/output_dims.joblib')

    print("Modelo de rede neural treinado e salvo com sucesso.")

if __name__ == "__main__":
    treinar_e_salvar_modelo_nn()




'''
venv_tf\Scripts\activate 

deactivate

'''