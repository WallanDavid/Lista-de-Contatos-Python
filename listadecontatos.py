import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class AgendaContatos:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contatos")

        self.contatos = []

        self.frame_lista = tk.Frame(root)
        self.frame_lista.pack(padx=10, pady=10)

        self.lista_contatos = tk.Listbox(self.frame_lista, width=40, height=10)
        self.lista_contatos.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = tk.Scrollbar(self.frame_lista)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_contatos.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lista_contatos.yview)

        self.frame_botoes = tk.Frame(root)
        self.frame_botoes.pack(pady=10)

        self.botao_adicionar = tk.Button(self.frame_botoes, text="Adicionar Contato", command=self.adicionar_contato)
        self.botao_adicionar.pack(side=tk.LEFT, padx=5)

        self.botao_remover = tk.Button(self.frame_botoes, text="Remover Contato", command=self.remover_contato)
        self.botao_remover.pack(side=tk.LEFT, padx=5)

        self.botao_limpar = tk.Button(self.frame_botoes, text="Limpar Lista", command=self.limpar_lista)
        self.botao_limpar.pack(side=tk.LEFT, padx=5)

        self.carregar_contatos()
        self.atualizar_lista_contatos()

        self.lista_contatos.bind("<Double-Button-1>", self.exibir_contato_detalhes)

    def adicionar_contato(self):
        nome = simpledialog.askstring("Adicionar Contato", "Nome:")
        telefone = simpledialog.askstring("Adicionar Contato", "Telefone:")
        email = simpledialog.askstring("Adicionar Contato", "E-mail:")

        if nome and telefone and email:
            contato = {"Nome": nome, "Telefone": telefone, "E-mail": email}
            self.contatos.append(contato)
            self.atualizar_lista_contatos()
            self.salvar_contatos()

    def remover_contato(self):
        selecionado = self.lista_contatos.curselection()
        if selecionado:
            indice = selecionado[0]
            self.contatos.pop(indice)
            self.atualizar_lista_contatos()
            self.salvar_contatos()

    def limpar_lista(self):
        confirmacao = messagebox.askokcancel("Limpar Lista", "Deseja realmente limpar a lista de contatos?")
        if confirmacao:
            self.contatos = []
            self.atualizar_lista_contatos()
            self.salvar_contatos()

    def atualizar_lista_contatos(self):
        self.lista_contatos.delete(0, tk.END)
        for contato in self.contatos:
            self.lista_contatos.insert(tk.END, contato["Nome"])

    def salvar_contatos(self):
        with open("contatos.json", "w") as arquivo:
            json.dump(self.contatos, arquivo)

    def carregar_contatos(self):
        try:
            with open("contatos.json", "r") as arquivo:
                self.contatos = json.load(arquivo)
        except FileNotFoundError:
            # Se o arquivo não existe, não há contatos a carregar
            pass

    def exibir_contato_detalhes(self, event):
        selecionado = self.lista_contatos.curselection()
        if selecionado:
            indice = selecionado[0]
            contato = self.contatos[indice]
            detalhes = f"Nome: {contato['Nome']}\nTelefone: {contato['Telefone']}\nE-mail: {contato['E-mail']}"
            messagebox.showinfo("Detalhes do Contato", detalhes)

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaContatos(root)
    root.mainloop()
