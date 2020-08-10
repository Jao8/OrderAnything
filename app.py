from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql

Name_DB = 'OA'
Host_DB = 'localhost'
Usario_DB = 'root'
Senha_DB = ''

passKey = 'PASS123'


class AdmPanel:

    def delProd(self):
        id = int(self.tree.selection()[0])

        try:
            connection = pymysql.connect(
                host=Host_DB,
                user=Usario_DB,
                password=Senha_DB,
                db=Name_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showerror("Erro", "Erro ao fazer conexão com o Banco de Dados")

        try:
            with connection.cursor() as c:
                c.execute(f'delete from produtos where id = {id}')
                connection.commit()
        except:
            messagebox.showerror("Erro", "Erro ao buscar produtos no Banco de Dados")

        self.prodBackend()

    def delAll(self):
        if messagebox.askokcancel("Limpar Banco de Dados", "Essa operação irá excluir TODOS os produtos\n"
                                                           "A recuperação destes dados NÃO será possível!!"):
            try:
                connection = pymysql.connect(
                    host=Host_DB,
                    user=Usario_DB,
                    password=Senha_DB,
                    db=Name_DB,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except:
                messagebox.showerror("Erro", "Erro ao fazer conexão com o Banco de Dados")

            try:
                with connection.cursor() as c:
                    print('Deleted\n')
                    #c.execute('select * from produtos')
                    #connection.commit()
            except:
                messagebox.showerror("Erro", "Erro ao buscar produtos no Banco de Dados")
        else:
            print('Not Deleted')

        self.prodBackend()

    def prodBackend(self):
        try:
            connection = pymysql.connect(
                host=Host_DB,
                user=Usario_DB,
                password=Senha_DB,
                db=Name_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showerror("Erro", "Erro ao fazer conexão com o Banco de Dados")

        try:
            with connection.cursor() as c:
                c.execute('select * from produtos')
                p = c.fetchall()
        except:
            messagebox.showerror("Erro", "Erro ao buscar produtos no Banco de Dados")

        self.tree.delete(*self.tree.get_children())

        res = []

        for i in p:
            res.append(i['nome'])
            res.append(i['ingredientes'])
            res.append(i['grupo'])
            res.append(i['preco'])

            self.tree.insert('', END, values=res, iid=i['id'], tag='1')

            res.clear()

    def cadProdBackend(self):
        nome = self.nome.get()
        ings = self.ing.get()
        gp = self.gp.get()
        preco = self.preco.get()

        try:
            connection = pymysql.connect(
                host=Host_DB,
                user=Usario_DB,
                password=Senha_DB,
                db=Name_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showerror("Erro", "Erro ao fazer conexão com o Banco de Dados")

        try:
            with connection.cursor() as c:
                c.execute("insert into produtos (nome, ingredientes, grupo, preco) values ('{}','{}','{}','{}')".format(
                    nome, ings, gp,preco
                ))
                connection.commit()
        except:
            messagebox.showerror("Erro", "Erro ao buscar cadastrar produto no Banco de Dados")

        self.prodBackend()

    def cadProd(self):
        self.cad = Tk()
        self.cad.title('Cadastro de produtos')
        color = '#524f4f'
        self.cad['bg'] = color

        Label(self.cad, text='Cadastrar os produtos', bg=color, fg='white').grid(row=0, column=0, columnspan=4,
                                                                                 padx=5, pady=5)
        Label(self.cad, text='nome', bg=color, fg='white').grid(row=1, column=0, columnspan=1,
                                                                padx=5, pady=5)
        self.nome = Entry(self.cad)
        self.nome.grid(row=1, column=1, columnspan=1, padx=5, pady=5)

        Label(self.cad, text='Ingredientes', bg=color, fg='white').grid(row=2, column=0, columnspan=1,
                                                                        padx=5, pady=5)
        self.ing = Entry(self.cad)
        self.ing.grid(row=2, column=1, columnspan=1, padx=5, pady=5)

        Label(self.cad, text='Grupo', bg=color, fg='white').grid(row=3, column=0, columnspan=1,
                                                                 padx=5, pady=5)
        self.gp = Entry(self.cad)
        self.gp.grid(row=3, column=1, columnspan=1, padx=5, pady=5)

        Label(self.cad, text='Preço', bg=color, fg='white').grid(row=4, column=0, columnspan=1,
                                                                 padx=5, pady=5)
        self.preco = Entry(self.cad)
        self.preco.grid(row=4, column=1, columnspan=1, padx=5, pady=5)

        Button(self.cad, text='Cadastrar', width=17, relief='flat', bg='gray',
               highlightbackground=color, command=self.cadProdBackend).grid(row=5, column=0, padx=5, pady=5)

        Button(self.cad, text='Excluir', width=17, relief='flat', bg='gray',
               highlightbackground=color, command=self.delProd).grid(row=5, column=1, padx=5, pady=5)

        Button(self.cad, text='Atualizar', width=17, relief='flat', bg='gray',
               highlightbackground=color, command=self.prodBackend).grid(row=6, column=0, padx=5, pady=5)

        Button(self.cad, text='Excluir tudo', width=17, relief='flat', bg='gray',
               highlightbackground=color, command=self.delAll).grid(row=6, column=1, padx=5, pady=5)

        self.tree = ttk.Treeview(self.cad, selectmode='browse', column=("column1", "column2", "column3", "column4"),
                                 show='headings')
        self.tree.column('column1', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='Nome')

        self.tree.column('column2', width=300, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')

        self.tree.column('column3', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Grupo')

        self.tree.column('column4', width=80, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Preço')

        self.tree.grid(row=0, column=4, columnspan=3, rowspan=10, padx=5, pady=5)

        self.prodBackend()

        self.cad.mainloop()

    def __init__(self, u):
        self.currentUser = u

        self.root = Tk()
        self.root.title("Painel de Administração - O.A.")
        self.root.geometry('500x500')

        Button(self.root, text='Pedidos', width='20').grid(row=0, column=0, padx=5, pady=5)
        Button(self.root, text='Cadastro\nde Produtos', width='20', command=self.cadProd).grid(row=1, column=0, padx=5,
                                                                                               pady=5)

        # messagebox.showinfo('O.A.', "Bem Vindo, {}!".format(u))

        self.root.mainloop()


class LoginWindow:

    def GerPanel(self, u):
        self.root = Tk()
        self.root.title("Painel de Atendimento - O.A.")
        self.root.geometry('500x500')

        # messagebox.showinfo('O.A.', "Bem Vindo, {}!".format(u))

        self.root.mainloop()

    def cadBackEnd(self):
        key = passKey

        if self.secure_key.get() == key:
            if len(self.user.get()) <= 35:
                if len(self.password.get()) <= 50:
                    if len(self.password.get()) >= 3:
                        name = self.user.get()
                        sen = self.password.get()

                        try:
                            connection = pymysql.connect(
                                host=Host_DB,
                                user=Usario_DB,
                                password=Senha_DB,
                                db=Name_DB,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor
                            )
                        except:
                            messagebox.showerror("Erro", "Erro ao fazer conexão com o Banco de Dados")

                        try:
                            with connection.cursor() as c:
                                c.execute("insert into cadastros ( nome, senha, nivel) values ( '%s', '%s', '%s')" %
                                          (name, sen, 1))
                                connection.commit()
                            messagebox.showinfo("Cadastro", "Usuario cadastrado com sucesso")
                            self.root.destroy()
                        except:
                            messagebox.showerror("Erro", "Erro ao fazer cadastro de usuario no Banco de Dados")
                    else:
                        messagebox.showerror('Erro',
                                             "Senha muito pequena\nA senha deve conter no minimo 3 caracteres!")
                else:
                    messagebox.showerror('Erro',
                                         "Senha muito grande\nA senha deve conter no máximo 50 caracteres!")
            else:
                messagebox.showerror('Erro',
                                     "Usuario muito grande\nA senha deve conter no máximo 35 caracteres!")
        else:
            messagebox.showerror('Erro',
                                 "Chave de segurança incorreta!\nEssa operação deve ser realizada por um administrador")

    def Cad(self):
        Label(self.root, text="Chave de Segurança").grid(row=3, column=0)
        self.secure_key = Entry(self.root, show='*')
        self.secure_key.grid(row=3, column=1, pady=5, padx=10)
        Button(self.root, text="Confirmar Cadastro", width=15, command=self.cadBackEnd).grid(
            row=4, column=0, columnspan=3, pady=5, padx=10)

    def SU_Backend(self):
        try:
            connection = pymysql.connect(
                host=Host_DB,
                user=Usario_DB,
                password=Senha_DB,
                db=Name_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showerror("Erro", "Erro ao fazer conexão com o Banco de Dados")

        try:
            with connection.cursor() as c:
                c.execute('select * from cadastros')
                cads = c.fetchall()
        except:
            messagebox.showerror("Erro", "Erro ao buscar cadastro no Banco de Dados")

        self.tree.delete(*self.tree.get_children())

        res = []

        for i in cads:
            res.append(i['id'])
            res.append(i['nome'])
            res.append(i['senha'])
            res.append(i['nivel'])

            self.tree.insert("", END, values=res, iid=i['id'], tag='1')

            res.clear()

    def showUsers(self):
        self.su = Toplevel()
        self.su.resizable(False, False)
        self.su.title("Usuarios Cadastrados")

        self.tree = ttk.Treeview(self.su, selectmode='browse', column=("column1", "column2", "column3", "column4"),
                                 show='headings')
        self.tree.column('column1', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column('column2', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Nome')

        self.tree.column('column3', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Senha')

        self.tree.column('column4', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Nivel ')

        self.tree.grid(row=0, column=0, padx=5, pady=5)

        self.SU_Backend()

        self.su.mainloop()

    def Auth(self):
        auth = False
        adm = False

        try:
            connection = pymysql.connect(
                host=Host_DB,
                user=Usario_DB,
                password=Senha_DB,
                db=Name_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showerror("Erro", "Erro ao fazer conexão com o Banco de Dados")

        usuario = self.user.get()
        senha = self.password.get()

        try:
            with connection.cursor() as c:
                c.execute('select * from cadastros')
                cads = c.fetchall()
        except:
            messagebox.showerror("Erro", "Erro ao buscar cadastro no Banco de Dados")

        for i in cads:
            if usuario == i['nome'] and senha == i['senha']:
                if i['nivel'] == 1:
                    adm = False
                elif i['nivel'] == 2:
                    adm = True
                auth = True
                break
            else:
                auth = False
        if auth is True:
            self.root.destroy()
            if adm is True:
                AdmPanel(usuario)
            else:
                self.GerPanel(usuario)

        else:
            messagebox.showwarning('Acesso Negado', "Usuario/Senha Incorretas")

    def __init__(self):
        self.root = Tk()
        self.root.title("OrderAnything")
        Label(self.root, text="Faça Login").grid(row=0, column=0, columnspan=2)

        Label(self.root, text="User").grid(row=1, column=0, padx=5)
        self.user = Entry(self.root)
        self.user.grid(row=1, column=1, padx=5)

        Label(self.root, text="Senha").grid(row=2, column=0, padx=5, pady=2.5)
        self.password = Entry(self.root, show='*')
        self.password.grid(row=2, column=1, padx=5, pady=2.5)

        Button(self.root, text="Login", width=10, command=self.Auth).grid(row=5, column=0, padx=2.5, pady=2.5)
        Button(self.root, text="Cadastrar", width=17, command=self.Cad).grid(row=5, column=1)
        # Button(self.root, text="Visualizar cadastros", width=30, command=self.showUsers).grid(row=6, column=0, columnspan=2, padx=2.5, pady=2.5)

        self.root.mainloop()


LoginWindow()
