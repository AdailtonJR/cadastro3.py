import tkinter as tk
from tkinter import messagebox
import sqlite3

# Função para criar banco de dados e tabela se não existir
def criar_banco():
    conn = sqlite3.connect('otica.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL,
                        cpf TEXT NOT NULL,
                        telefone TEXT NOT NULL,
                        email TEXT,
                        data_nascimento TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas (
                        id INTEGER PRIMARY KEY,
                        cliente_id INTEGER,
                        esferico_esquerdo REAL,
                        cilindrico_esquerdo REAL,
                        eixo_esquerdo INTEGER,
                        esferico_direito REAL,
                        cilindrico_direito REAL,
                        eixo_direito INTEGER,
                        adicao REAL,
                        FOREIGN KEY (cliente_id) REFERENCES clientes (id))''')
    conn.commit()
    conn.close()

# Função para cadastrar cliente
def cadastrar_cliente():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    data_nascimento = entry_data_nascimento.get()

    if not nome or not cpf or not telefone:
        messagebox.showerror("Erro", "Nome, CPF e Telefone são obrigatórios!")
        return
    
    conn = sqlite3.connect('otica.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO clientes (nome, cpf, telefone, email, data_nascimento)
                      VALUES (?, ?, ?, ?, ?)''', (nome, cpf, telefone, email, data_nascimento))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

# Função para cadastrar receita óptica
def cadastrar_receita():
    cliente_id = entry_cliente_id.get()
    esferico_esquerdo = entry_esferico_esquerdo.get()
    cilindrico_esquerdo = entry_cilindrico_esquerdo.get()
    eixo_esquerdo = entry_eixo_esquerdo.get()
    esferico_direito = entry_esferico_direito.get()
    cilindrico_direito = entry_cilindrico_direito.get()
    eixo_direito = entry_eixo_direito.get()
    adicao = entry_adicao.get()

    if not cliente_id:
        messagebox.showerror("Erro", "ID do cliente é obrigatório!")
        return

    conn = sqlite3.connect('otica.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO receitas (cliente_id, esferico_esquerdo, cilindrico_esquerdo, eixo_esquerdo,
                      esferico_direito, cilindrico_direito, eixo_direito, adicao)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (cliente_id, esferico_esquerdo, cilindrico_esquerdo, eixo_esquerdo,
                    esferico_direito, cilindrico_direito, eixo_direito, adicao))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Receita óptica cadastrada com sucesso!")

# Função para consultar clientes
def consultar_clientes():
    conn = sqlite3.connect('otica.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    resultado.delete(1.0, tk.END)  # Limpar resultados anteriores
    for cliente in clientes:
        resultado.insert(tk.END, f"{cliente[1]} - {cliente[2]} - {cliente[3]}\n")

# Função para consultar receita óptica de um cliente
def consultar_receita():
    cliente_id = entry_cliente_id_receita.get()

    if not cliente_id:
        messagebox.showerror("Erro", "ID do cliente é obrigatório!")
        return

    conn = sqlite3.connect('otica.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM receitas WHERE cliente_id = ?''', (cliente_id,))
    receita = cursor.fetchone()
    conn.close()

    if receita:
        resultado_receita.delete(1.0, tk.END)  # Limpar resultados anteriores
        resultado_receita.insert(tk.END, f"Cliente ID: {cliente_id}\n")
        resultado_receita.insert(tk.END, f"Esférico Esquerdo: {receita[2]}\n")
        resultado_receita.insert(tk.END, f"Cilíndrico Esquerdo: {receita[3]}\n")
        resultado_receita.insert(tk.END, f"Eixo Esquerdo: {receita[4]}\n")
        resultado_receita.insert(tk.END, f"Esférico Direito: {receita[5]}\n")
        resultado_receita.insert(tk.END, f"Cilíndrico Direito: {receita[6]}\n")
        resultado_receita.insert(tk.END, f"Eixo Direito: {receita[7]}\n")
        resultado_receita.insert(tk.END, f"Adição: {receita[8]}\n")
    else:
        messagebox.showinfo("Erro", "Receita não encontrada para este cliente.")

# Interface gráfica
root = tk.Tk()
root.title("Cadastro de Óptica")

# Criar banco de dados
criar_banco()

# Labels e campos para cadastro de cliente
label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

label_cpf = tk.Label(root, text="CPF:")
label_cpf.grid(row=1, column=0)
entry_cpf = tk.Entry(root)
entry_cpf.grid(row=1, column=1)

label_telefone = tk.Label(root, text="Telefone:")
label_telefone.grid(row=2, column=0)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=2, column=1)

label_email = tk.Label(root, text="E-mail:")
label_email.grid(row=3, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=3, column=1)

label_data_nascimento = tk.Label(root, text="Data de Nascimento:")
label_data_nascimento.grid(row=4, column=0)
entry_data_nascimento = tk.Entry(root)
entry_data_nascimento.grid(row=4, column=1)

btn_cadastrar_cliente = tk.Button(root, text="Cadastrar Cliente", command=cadastrar_cliente)
btn_cadastrar_cliente.grid(row=5, column=0, columnspan=2)

# Labels e campos para cadastro de receita óptica
label_cliente_id = tk.Label(root, text="ID do Cliente:")
label_cliente_id.grid(row=6, column=0)
entry_cliente_id = tk.Entry(root)
entry_cliente_id.grid(row=6, column=1)

label_esferico_esquerdo = tk.Label(root, text="Esférico Esquerdo:")
label_esferico_esquerdo.grid(row=7, column=0)
entry_esferico_esquerdo = tk.Entry(root)
entry_esferico_esquerdo.grid(row=7, column=1)

label_cilindrico_esquerdo = tk.Label(root, text="Cilíndrico Esquerdo:")
label_cilindrico_esquerdo.grid(row=8, column=0)
entry_cilindrico_esquerdo = tk.Entry(root)
entry_cilindrico_esquerdo.grid(row=8, column=1)

label_eixo_esquerdo = tk.Label(root, text="Eixo Esquerdo:")
label_eixo_esquerdo.grid(row=9, column=0)
entry_eixo_esquerdo = tk.Entry(root)
entry_eixo_esquerdo.grid(row=9, column=1)

label_esferico_direito = tk.Label(root, text="Esférico Direito:")
label_esferico_direito.grid(row=10, column=0)
entry_esferico_direito = tk.Entry(root)
entry_esferico_direito.grid(row=10, column=1)

label_cilindrico_direito = tk.Label(root, text="Cilíndrico Direito:")
label_cilindrico_direito.grid(row=11, column=0)
entry_cilindrico_direito = tk.Entry(root)
entry_cilindrico_direito.grid(row=11, column=1)

label_eixo_direito = tk.Label(root, text="Eixo Direito:")
label_eixo_direito.grid(row=12, column=0)
entry_eixo_direito = tk.Entry(root)
entry_eixo_direito.grid(row=12, column=1)

label_adicao = tk.Label(root, text="Adição:")
label_adicao.grid(row=13, column=0)
entry_adicao = tk.Entry(root)
entry_adicao.grid(row=13, column=1)

btn_cadastrar_receita = tk.Button(root, text="Cadastrar Receita", command=cadastrar_receita)
btn_cadastrar_receita.grid(row=14, column=0, columnspan=2)

# Resultado da consulta de clientes
resultado = tk.Text(root, width=50, height=10)
resultado.grid(row=15, column=0, columnspan=2)

btn_consultar = tk.Button(root, text="Consultar Clientes", command=consultar_clientes)
btn_consultar.grid(row=16, column=0, columnspan=2)

# Labels e campos para consultar receita óptica
label_cliente_id_receita = tk.Label(root, text="ID do Cliente para Receita:")
label_cliente_id_receita.grid(row=17, column=0)
entry_cliente_id_receita = tk.Entry(root)
entry_cliente_id_receita.grid(row=17, column=1)

btn_consultar_receita = tk.Button(root, text="Consultar Receita", command=consultar_receita)
btn_consultar_receita.grid(row=18, column=0, columnspan=2)

# Resultado da consulta de receita óptica
resultado_receita = tk.Text(root, width=50, height=10)
resultado_receita.grid(row=19, column=0, columnspan=2)

root.mainloop()
