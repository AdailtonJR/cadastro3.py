import tkinter as tk
from tkinter import messagebox

# Função para calcular os diâmetros
def calcular_diametro():
    try:
        # Obtendo os valores das entradas
        n1 = float(entry_ponte.get())
        n2 = float(entry_aro_horizontal.get())
        n3 = float(entry_diagonal_maior.get())
        n4 = float(entry_dnp_od.get())
        n5 = float(entry_dnp_oe.get())
        
        # Cálculos
        n6 = (n1 + n2 - (n4 * 2) + n3 + 2)
        n7 = (n1 + n2 - (n5 * 2) + n3 + 2)
        
        # Exibindo os resultados
        label_resultado_od.config(text=f'Diâmetro do OD: {n6:.2f}')
        label_resultado_oe.config(text=f'Diâmetro do OE: {n7:.2f}')
    
    except ValueError:
        # Se algum valor não for numérico
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Função para limpar os dados
def limpar_dados():
    # Limpa os campos de entrada
    entry_ponte.delete(0, tk.END)
    entry_aro_horizontal.delete(0, tk.END)
    entry_diagonal_maior.delete(0, tk.END)
    entry_dnp_od.delete(0, tk.END)
    entry_dnp_oe.delete(0, tk.END)
    
    # Limpa os resultados
    label_resultado_od.config(text="Diâmetro do OD: ")
    label_resultado_oe.config(text="Diâmetro do OE: ")

# Criando a janela principal
root = tk.Tk()
root.title("Cálculo de Diâmetro de Lentes")

# Definindo o tamanho da janela
root.geometry("400x450")

# Títulos
titulo = tk.Label(root, text="Cálculo de Diâmetro de Lentes", font=("Arial", 16))
titulo.pack(pady=10)

# Labels e campos de entrada para os dados
label_ponte = tk.Label(root, text="Ponte:")
label_ponte.pack()
entry_ponte = tk.Entry(root)
entry_ponte.pack()

label_aro_horizontal = tk.Label(root, text="Aro-Horizontal:")
label_aro_horizontal.pack()
entry_aro_horizontal = tk.Entry(root)
entry_aro_horizontal.pack()

label_diagonal_maior = tk.Label(root, text="Diagonal Maior:")
label_diagonal_maior.pack()
entry_diagonal_maior = tk.Entry(root)
entry_diagonal_maior.pack()

label_dnp_od = tk.Label(root, text="DNP OD:")
label_dnp_od.pack()
entry_dnp_od = tk.Entry(root)
entry_dnp_od.pack()

label_dnp_oe = tk.Label(root, text="DNP OE:")
label_dnp_oe.pack()
entry_dnp_oe = tk.Entry(root)
entry_dnp_oe.pack()

# Botões para realizar o cálculo e limpar dados
botao_calcular = tk.Button(root, text="Calcular", command=calcular_diametro)
botao_calcular.pack(pady=10)

botao_limpar = tk.Button(root, text="Limpar Dados", command=limpar_dados)
botao_limpar.pack(pady=10)

# Labels para exibir os resultados
label_resultado_od = tk.Label(root, text="Diâmetro do OD: ", font=("Arial", 12))
label_resultado_od.pack()

label_resultado_oe = tk.Label(root, text="Diâmetro do OE: ", font=("Arial", 12))
label_resultado_oe.pack()

# Iniciar a interface
root.mainloop()
