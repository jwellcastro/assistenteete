import tkinter as tk 
from tkinter import scrolledtext
from tkinter import ttk
from ttkthemes import ThemedTk
import requests

# Função para enviar mensagem para a API
def send_message(event=None):  # Permite uso com botão ou tecla Enter
    user_message = entry.get()  # Pega o texto digitado
    if not user_message.strip():
        display_message("Assistente", "Não entendi. Por favor, insira uma pergunta válida.", "assistente")
        return

    display_message("Você", user_message, "usuario")  # Mostra a mensagem do usuário na área de texto
    entry.delete(0, tk.END)  # Limpa o campo de entrada

    try:
        # Faz a requisição para a API
        response = requests.post("http://127.0.0.1:5000/chat", json={"message": user_message})
        if response.status_code == 200:
            assistant_response = response.json().get("response", "Erro ao obter resposta.")
        else:
            assistant_response = f"Erro: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        assistant_response = f"Erro ao se conectar com a API: {e}"

    display_message("Assistente", assistant_response, "assistente")

# Função para exibir mensagens no chat
def display_message(sender, message, sender_type):
    chat_box.config(state=tk.NORMAL)

    # Estilizando a exibição das mensagens
    if sender_type == "usuario":
        chat_box.insert(tk.END, "=" * 50 + "\n")  # Linha tracejada após a mensagem do usuário
        chat_box.insert(tk.END, f"{sender}: ", 'usuario')
        chat_box.insert(tk.END, f"{message}\n")
        chat_box.insert(tk.END, "=" * 50 + "\n")  # Linha tracejada após a mensagem do usuário
    else:
        chat_box.insert(tk.END, f"{sender}: ", 'assistente')
        chat_box.insert(tk.END, f"{message}\n")
        chat_box.insert(tk.END, "\n" * 2)  # Adiciona um espaçamento maior após a resposta do assistente

    chat_box.config(state=tk.DISABLED)  # Impede edição manual do chat
    chat_box.yview(tk.END)  # Rola para a última mensagem

# Função para limpar o chat
def clear_chat():
    chat_box.config(state=tk.NORMAL)  # Permite edição temporária
    chat_box.delete(1.0, tk.END)  # Limpa todo o conteúdo do chat
    chat_box.config(state=tk.DISABLED)  # Impede edição manual do chat

# Configuração da janela principal com tema
root = ThemedTk(theme="breeze")  # Usando o tema 'breeze', que é claro
root.title("Assistente ETE")

# Definir um tamanho fixo para a janela e desabilitar a redimensionabilidade
root.geometry("500x450")  # Define um tamanho fixo
root.resizable(False, False)  # Desabilita o redimensionamento da janela

root.config(bg="#F0F8FF")  # Fundo amarelo claro

# Área de exibição do chat
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=60, height=20, font=("Arial", 10), bg="#DCDCDC", fg="black")
chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Definindo o estilo para o campo de entrada (entry) usando style
style = ttk.Style()
style.configure("TEntry",
                fieldbackground="#BBDEFB",  # Azul clarinho
                foreground="#000080",       # Azul escuro para o texto
                font=("Arial", 14))

# Campo de entrada para o usuário
entry = ttk.Entry(root, width=50, style="TEntry")
entry.grid(row=1, column=0, padx=10, pady=10)
entry.bind("<Return>", send_message)  # Vincula a tecla Enter à função

# Botão de envio
send_button = ttk.Button(root, text="Enviar", command=send_message)
send_button.grid(row=1, column=1, padx=5, pady=10)

# Botão de limpar
clear_button = ttk.Button(root, text="Limpar", command=clear_chat)
clear_button.grid(row=2, column=1, columnspan=2, pady=10)  # Coloca o botão na linha 2

# Estilos para o texto
chat_box.tag_configure("usuario", foreground="blue", font=("Arial", 10, "bold"))
chat_box.tag_configure("assistente", foreground="green", font=("Arial", 10, "bold"))

# Inicia a interface
root.mainloop()
