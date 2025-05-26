import tkinter as tk
from tkinter import scrolledtext, messagebox
import joblib
import os
import sys
import tensorflow as tf
import string
import unicodedata
import numpy as np

class PredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neurito Intelbras")
        self.root.geometry("600x400")

        # Inicializar variáveis
        self.vectorizer = None
        self.encoders = None  # Agora será um dicionário de encoders
        self.model = None
        self.target_cols = ['produto', 'motivo do caso', 'acao', 'diagnostico']  # Definindo as colunas alvo

        # Tentar carregar o modelo
        if not self.carregar_modelo():
            sys.exit(1)

        # Criar interface
        self.criar_interface()

    def carregar_modelo(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'modelo_salvo')

            self.vectorizer = joblib.load(os.path.join(model_path, 'vectorizer.joblib'))
            self.encoders = joblib.load(os.path.join(model_path, 'encoders.joblib'))  # Carrega o dicionário de encoders
            self.model = tf.keras.models.load_model(os.path.join(model_path, 'modelo_nn.h5'))
            
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o modelo: {e}")
            return False

    def criar_interface(self):
        #  6eaa5e
        #  #008000
        #  b7d5ac
        # Campo de entrada com fundo azul claro
        self.campo_a = scrolledtext.ScrolledText(self.root, height=8, bg="#6eaa5e", fg="black")
        self.campo_a.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        # Botões com fundo cinza e texto branco
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=5)

        btn_analisar = tk.Button(frame_botoes, text="✔ Analisar", command=self.analisar_texto, bg="#b7d5ac", fg="#14870c")
        btn_analisar.pack(side=tk.LEFT, padx=5)

        btn_limpar = tk.Button(frame_botoes, text="🖉 Limpar", command=self.limpar, bg="#b7d5ac", fg="#14870c")
        btn_limpar.pack(side=tk.LEFT, padx=5)

        # Campo de saída com fundo azul claro
        self.campo_b = scrolledtext.ScrolledText(self.root, height=8, bg="#6eaa5e", fg="black")
        self.campo_b.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    def preprocess_text(self, text):
        if not isinstance(text, str):
            return ""

        # Converter para minúsculas
        text = text.lower()

        # Remover pontuação
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Normalizar caracteres
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

        # Tokenização e remoção de stopwords
        stop_words = {'de', 'a', 'o', 'que', 'e', 'é', 'do', 'da', 'em', 'um', 'para'}
        tokens = [word for word in text.split() if word not in stop_words]

        return ' '.join(tokens)

    def analisar_texto(self):
        texto = self.campo_a.get("1.0", tk.END).strip()
        
        if len(texto) < 10:
            messagebox.showwarning("Texto curto", "Por favor, insira um texto com pelo menos 10 caracteres.")
            return

        try:
            # Limpar o campo B antes de inserir novos resultados
            self.campo_b.delete("1.0", tk.END)
            
            texto_processado = self.preprocess_text(texto)
            texto_vetorizado = self.vectorizer.transform([texto_processado])
            
            # Fazer predição - agora retorna uma lista de arrays (um para cada saída)
            predicoes = self.model.predict(texto_vetorizado)
            
            # Decodificar cada saída separadamente
            resultado = []
            for i, col in enumerate(self.target_cols):
                # Obter o índice da classe predita
                classe_idx = np.argmax(predicoes[i][0])
                # Decodificar usando o LabelEncoder correspondente
                valor_decodificado = self.encoders[col]['label'].inverse_transform([classe_idx])[0]
                resultado.append(f"{col}: {valor_decodificado}")
            
            # Inserir resultados no campo B
            self.campo_b.insert(tk.END, "\n".join(resultado))
            
        except Exception as e:
            self.campo_b.insert(tk.END, f"Erro ao analisar: {str(e)}")

    def limpar(self):
        self.campo_a.delete("1.0", tk.END)
        self.campo_b.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PredictorApp(root)
    root.mainloop()