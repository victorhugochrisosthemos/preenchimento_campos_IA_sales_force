import tkinter as tk
from tkinter import scrolledtext
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


def analisar():
    texto = campo_a.get("1.0", tk.END).strip()
    
    # Pré-processar o texto
    texto_processado = preprocess_text(texto)
    
    # Limpar o campo B antes de inserir novos resultados
    campo_b.delete("1.0", tk.END)
    
    # Verificar se os modelos foram carregados
    if modelos_carregados:
        # Obter sugestões dos modelos
        sugestoes = sugerir_campos(texto_processado, modelos_carregados)
        
        # Preparar texto para exibição
        resultado = []
        for campo, valor in sugestoes.items():
            resultado.append(f"{campo}: {valor}")
        
        # Inserir resultados no campo B
        campo_b.insert(tk.END, "\n".join(resultado))
    else:
        campo_b.insert(tk.END, "Modelo nao carregou!")

def limpar():
    campo_a.delete("1.0", tk.END)
    campo_b.delete("1.0", tk.END)

janela = tk.Tk()
janela.title("PNL para preenchimento de campos obrigatorios do Talk Desk")
janela.geometry("600x400")

# Campo A com fundo azul claro
campo_a = scrolledtext.ScrolledText(janela, height=8, bg="lightblue", fg="black")
campo_a.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

# Botões com fundo cinza e texto branco
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

btn_analisar = tk.Button(frame_botoes, text="✔ Analisar", command=analisar, bg="gray", fg="white")
btn_analisar.pack(side=tk.LEFT, padx=5)

btn_limpar = tk.Button(frame_botoes, text="🖉 Limpar", command=limpar, bg="gray", fg="white")
btn_limpar.pack(side=tk.LEFT, padx=5)

# Campo B com fundo azul claro
campo_b = scrolledtext.ScrolledText(janela, height=8, bg="lightblue", fg="black")
campo_b.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

janela.mainloop()
