import sqlite3

# Criando conexão com o banco de dados (ou criando o arquivo, se não existir)
conn = sqlite3.connect('optica.db')
cursor = conn.cursor()

# Criando a tabela de clientes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        endereco TEXT,
        telefone TEXT,
        email TEXT
    )
''')

# Criando a tabela de receitas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        esferico_esquerdo REAL,
        esferico_direito REAL,
        cilindrico_esquerdo REAL,
        cilindrico_direito REAL,
        eixo_esquerdo INTEGER,
        eixo_direito INTEGER,
        tipo_lente TEXT,
        validade DATE,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id)
    )
''')

# Comitando as mudanças e fechando a conexão
conn.commit()
conn.close()

import tkinter as tk
from tkinter import messagebox
import sqlite3

def cadastrar_cliente():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    endereco = entry_endereco.get()
    telefone = entry_telefone.get()
    email = entry_email.get()

    if not nome or not cpf:
        messagebox.showerror("Erro", "Nome e CPF são obrigatórios.")
        return

    try:
        conn = sqlite3.connect('optica.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, cpf, endereco, telefone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, cpf, endereco, telefone, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        limpar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "CPF já cadastrado.")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Criando a janela principal
root = tk.Tk()
root.title("Cadastro de Clientes - Ótica")

# Definindo os campos da interface
tk.Label(root, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(root, width=30)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="CPF:").grid(row=1, column=0, padx=10, pady=10)
entry_cpf = tk.Entry(root, width=30)
entry_cpf.grid(row=1, column=1)

tk.Label(root, text="Endereço:").grid(row=2, column=0, padx=10, pady=10)
entry_endereco = tk.Entry(root, width=30)
entry_endereco.grid(row=2, column=1)

tk.Label(root, text="Telefone:").grid(row=3, column=0, padx=10, pady=10)
entry_telefone = tk.Entry(root, width=30)
entry_telefone.grid(row=3, column=1)

tk.Label(root, text="Email:").grid(row=4, column=0, padx=10, pady=10)
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=4, column=1)

# Botão de cadastro
botao_cadastrar = tk.Button(root, text="Cadastrar Cliente", command=cadastrar_cliente)
botao_cadastrar.grid(row=5, columnspan=2, pady=20)

# Iniciando a interface gráfica
root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def buscar_clientes():
    nome_cliente = entry_nome_cliente.get()

    # Conectando ao banco de dados
    conn = sqlite3.connect('optica.db')
    cursor = conn.cursor()

    query = "SELECT * FROM clientes WHERE nome LIKE ?"
    cursor.execute(query, ('%' + nome_cliente + '%',))  # Pesquisa parcial no nome
    clientes = cursor.fetchall()

    # Limpando a lista de resultados antes de adicionar novos
    for item in treeview.get_children():
        treeview.delete(item)

    # Adicionando os resultados na árvore
    for cliente in clientes:
        treeview.insert("", "end", values=cliente)

    conn.close()

def buscar_receitas():
    # Pegando o id do cliente selecionado
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Aviso", "Selecione um cliente para consultar as receitas.")
        return

    cliente_id = treeview.item(selected_item[0])['values'][0]

    # Conectando ao banco de dados
    conn = sqlite3.connect('optica.db')
    cursor = conn.cursor()

    query = "SELECT * FROM receitas WHERE id_cliente = ?"
    cursor.execute(query, (cliente_id,))
    receitas = cursor.fetchall()

    # Limpando a lista de receitas antes de adicionar novas
    for item in treeview_receitas.get_children():
        treeview_receitas.delete(item)

    # Adicionando os resultados na árvore de receitas
    for receita in receitas:
        treeview_receitas.insert("", "end", values=receita)

    conn.close()

# Criando a janela principal
root = tk.Tk()
root.title("Consulta de Clientes e Receitas - Ótica")

# Tela de pesquisa de clientes
frame_busca_clientes = tk.LabelFrame(root, text="Buscar Clientes", padx=10, pady=10)
frame_busca_clientes.pack(padx=10, pady=10, fill="both", expand=True)

tk.Label(frame_busca_clientes, text="Nome do Cliente:").grid(row=0, column=0, padx=10, pady=10)
entry_nome_cliente = tk.Entry(frame_busca_clientes, width=30)
entry_nome_cliente.grid(row=0, column=1)

botao_buscar_clientes = tk.Button(frame_busca_clientes, text="Buscar", command=buscar_clientes)
botao_buscar_clientes.grid(row=0, column=2, padx=10)

# Árvore para exibir os clientes
columns = ("ID", "Nome", "CPF", "Endereço", "Telefone", "Email")
treeview = ttk.Treeview(frame_busca_clientes, columns=columns, show="headings", height=6)
treeview.grid(row=1, column=0, columnspan=3, pady=10)

# Definindo as colunas da árvore
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)

# Tela de pesquisa de receitas
frame_busca_receitas = tk.LabelFrame(root, text="Buscar Receitas", padx=10, pady=10)
frame_busca_receitas.pack(padx=10, pady=10, fill="both", expand=True)

botao_buscar_receitas = tk.Button(frame_busca_receitas, text="Buscar Receitas", command=buscar_receitas)
botao_buscar_receitas.pack(pady=10)

# Árvore para exibir as receitas
columns_receitas = ("ID Receita", "ID Cliente", "Esférico Esq.", "Esférico Dir.", "Cilíndrico Esq.", "Cilíndrico Dir.",
                    "Eixo Esq.", "Eixo Dir.", "Tipo de Lente", "Validade")
treeview_receitas = ttk.Treeview(frame_busca_receitas, columns=columns_receitas, show="headings", height=6)
treeview_receitas.pack(fill="both", padx=10)

# Definindo as colunas da árvore
for col in columns_receitas:
    treeview_receitas.heading(col, text=col)
    treeview_receitas.column(col, width=100)

# Iniciando a interface gráfica
root.mainloop()
