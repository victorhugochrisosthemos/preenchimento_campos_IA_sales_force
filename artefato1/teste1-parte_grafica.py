import tkinter as tk
from tkinter import scrolledtext

def analisar():
    texto = campo_a.get("1.0", tk.END).strip()
    tokens = texto.split()


    #--------Aqui manipula o texto

    tokens.append("Teste")


    #--------------------------------------
    
    campo_b.delete("1.0", tk.END)
    campo_b.insert(tk.END, "\n".join(tokens))

def limpar():
    campo_a.delete("1.0", tk.END)
    campo_b.delete("1.0", tk.END)

janela = tk.Tk()
janela.title("Reconhecedor de linguagem regular")
janela.geometry("600x400")

# Campo A com fundo azul claro
campo_a = scrolledtext.ScrolledText(janela, height=8, bg="lightblue", fg="black")
campo_a.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

# Botões com fundo cinza e texto branco
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

btn_analisar = tk.Button(frame_botoes, text="✔ analisar", command=analisar, bg="gray", fg="white")
btn_analisar.pack(side=tk.LEFT, padx=5)

btn_limpar = tk.Button(frame_botoes, text="🖉 limpar", command=limpar, bg="gray", fg="white")
btn_limpar.pack(side=tk.LEFT, padx=5)

# Campo B com fundo azul claro
campo_b = scrolledtext.ScrolledText(janela, height=8, bg="lightblue", fg="black")
campo_b.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

janela.mainloop()
