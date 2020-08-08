import pymysql as sql
import pymysql.cursors as db
import sys
import matplotlib.pyplot as plt

connection = sql.connect(
    host='localhost',
    user='root',
    password='',
    db='OA',
    charset='utf8mb4',
    cursorclass=db.DictCursor
)

auth = False

def sing_in_up(option):
    ExistingUser = 0
    Autorization = False
    AdminUser = False

    if option == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')
        for res in resp:
            if nome == res['nome'] and senha == res['senha']:
                if res['nivel'] == 1:
                    pass
                elif res['nivel'] == 2:
                    AdminUser = True
                Autorization = True
                print('\nBem-vindo, {}!\n'.format(nome))
                break
            else:
                Autorization = False

        if Autorization is False:
            print('\nUsuario/Senha Incorreta\n')
    elif option == 2:
        print('Digite seus dados:\n')
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for res in resp:
            if nome == res['nome']:
                ExistingUser = 1
        
        if ExistingUser == 1:
            print('\nUsuario já existente\n')
        elif ExistingUser == 0:
            try:
                with connection.cursor() as c:
                    c.execute("insert into cadastros values ('%s','%s',1)", (nome, senha))
                    connection.commit()      
                print('\nUsuario cadastrado com sucesso!\n\n')              
            except:
                print('Ocorreu um erro durante a inserção dos dados.\nPor favor contate um administrador.\n')
    elif option == 3:
        sys.exit()
    return Autorization, AdminUser

def cadProd():
    
    nome = input('\nNome do produto a ser cadastrado: ')
    ing = input('\nDeseja cadastrar ingredientes para esse produto? (s/n): ')
    if ing == 's':
        ingredients = input('\nDigite os ingredientes: ')
    elif ing != 'n':
        ingredients = ''
    grupo = input('\nA qual categoria esse produto pertence?\n')
    preco = float(input('\nQual o valor desse produto?\n'))

    try:
        with connection.cursor() as c:
            c.execute("insert into produtos (nome, ingredientes, grupo, preco) values ('%s', '%s', '%s', '%s')" % 
                (nome, ingredients, grupo, preco))
            connection.commit()
            print('\nProduto cadastrado com sucesso\n\n')
    except:
        print('\n\nErro ao cadstrar o produto\n\n')

def catalogo():
    prod = []

    try:
        with connection.cursor() as c:
            c.execute('select * from produtos')
            pList = c.fetchall()
    except:
        print("Erro ao acessar o Banco de Dados")
    for i in pList:
        prod.append(i)
    if len(prod) != 0:
        for i in range(0, len(prod)):
            print(f'{prod[i]}\n')        
    else:
        print("Não há produtos cadastrados")

def delProd():
    idProd = int(input('\nDigite o ID do produto a ser excluido: '))

    try:
        with connection.cursor() as c:
            c.execute(f'delete from produtos where id = {idProd}')
            print('\nProduto excluido!\n')
    except :
        pass

def cadPed():
    pcad = 0
    nome = input('Produto: ')
    local = input('Endereço da entrega: ')
    obs = input('Observações: ')

    try:
        with connection.cursor() as c:
            c.execute('select * from produtos')
            prods = c.fetchall()
    except:
        print('Erro de ao conectar no Banco de Dados')

    ings = 'Nenhum'
    gp = 'Nenhum'
    for i in prods:
        p = i['nome']

        if nome.upper() == p.upper():
            pcad = 1
            ings = i['ingredientes']
            gp = i['grupo']

    if pcad == 1:
       try:
           with connection.cursor() as c:
               c.execute("insert into pedidos ( nome, ingredientes, grupo, localEntrega, observacoes )\
                        values ( '{}', '{}', '{}', '{}', '{}' )".format(nome, ings, gp, local, obs))
               connection.commit()
               print('Pedido cadastrado com sucesso!\n')
       except:
            print('Erro de ao conectar no Banco de Dados')
    else:
        print('\nProduto não cadastrado no sistema!\n')

def listOrders():
    Orders = []
    action = 0

    while action != 2:
        Orders.clear()

        try:
            with connection.cursor() as c:
                c.execute('Select * from pedidos')
                Lista = c.fetchall()   
        except :
            print("Erro ao connectar no Banco de Dados")
        
        for i in Lista:
            Orders.append(i)
        
        if len(Orders) > 0:
            for i in range(0, len(Orders)):
                print(Orders[i])
        else:
            print("Não há pedidos no momento")

        action = int(input("\nOpção 1: Finalizar Pedido\t\tOpção 2: Sair\n"))

        if action == 1:
            fim = int(input("\nID do pedido a ser finalizado: "))
            try:
                 with connection.cursor() as c:
                    c.execute(f'delete from pedidos where id = {fim}')
                    print("\nPedido Finalizado\n\n")
            except :
                print("Erro ao connectar no Banco de Dados")
            
def stat():

    prods = []
    prods.clear()

    try:
        with connection.cursor() as c:
            c.execute('Select * from produtos')
            p = c.fetchall()
    except :
        print("Erro de conexão com o Banco de Dados")

    try:
        with connection.cursor() as c:
            c.execute('Select * from estatisticaVendido')
            sold = c.fetchall()
    except :
        print("Erro de conexão com o Banco de Dados")

    opt = int(input("\nOpção 1: Busca por Nome\
                    \tOpção 2: Busca por Grupo\
                    \n\nOpção 0: Sair\n\n"))
    
    if opt == 1:
        opt2 = int(input("\nOpção 1: Filtra por Valor\tOpção 2: Filtrar por Quantidade\n"))
        
        if opt2 == 1:
            for i in p:
                prods.append(i['nome'])
            
            val = []
            val.clear()
            for j in range(0, len(prods)):
                sum_val = -1
                for i in sold:
                    if i['nome'] == prods[j]:
                        sum_val += i['preco']
                if sum_val == -1:
                    val.append(0)
                elif sum_val > 0:
                    val.append(sum_val + 1)

            plt.plot(prods, val)
            plt.ylabel("QTD vendido em R$")
            plt.xlabel("Produtos")    
            plt.show() 

        if opt2 == 2:
            gp = []
            gp.clear()

            try:
                with connection.cursor() as c:
                    c.execute('Select * from produtos')
                    cat = c.fetchall()
            except :
                print("Erro de conexão com o Banco de Dados")
            
            try:
                with connection.cursor() as c:
                    c.execute('Select * from estatisticaVendido')
                    soldGP = c.fetchall()
            except :
                print("Erro de conexão com o Banco de Dados")
            
            for i in cat:
                gp.append(i['nome'])    
            
            gp = sorted(set(gp))
            
            qtdF = []
            qtdF.clear()

            for j in range(0, len(gp)):
                
                qtd = 0
                for i in soldGP:
                    if gp[j] == i['nome']:
                        qtd += 1
                qtdF.append(qtd)    

            plt.plot(gp, qtdF)
            plt.ylabel("Qtd Vendida")
            plt.xlabel("produtos")
            plt.show()
    elif opt == 2:
        opt2 = int(input("\nOpção 1: Filtra por Valor\tOpção 2: Filtrar por Quantidade\n"))
        
        if opt2 == 1:

            cat = []
            cat.clear()

            for i in p:
                cat.append(i['grupo'])
            
            val = []
            val.clear()
            for j in range(0, len(cat)):
                sum_val = -1
                for i in sold:
                    if i['grupo'] == cat[j]:
                        sum_val += i['preco']
                if sum_val == -1:
                    val.append(0)
                elif sum_val > 0:
                    val.append(sum_val + 1)

            plt.plot(cat, val)
            plt.ylabel("QTD vendido em R$")
            plt.xlabel("Produtos")    
            plt.show() 

    if opt2 == 2:
            gp = []
            gp.clear()

            try:
                with connection.cursor() as c:
                    c.execute('Select * from produtos')
                    cat = c.fetchall()
            except :
                print("Erro de conexão com o Banco de Dados")
            
            try:
                with connection.cursor() as c:
                    c.execute('Select * from estatisticaVendido')
                    soldGP = c.fetchall()
            except :
                print("Erro de conexão com o Banco de Dados")
            
            for i in cat:
                gp.append(i['grupo'])    
            
            gp = sorted(set(gp))
            
            qtdF = []
            qtdF.clear()

            for j in range(0, len(gp)):
                
                qtd = 0
                for i in soldGP:
                    if gp[j] == i['grupo']:
                        qtd += 1
                qtdF.append(qtd)    

            plt.plot(gp, qtdF)
            plt.ylabel("Qtd Vendida")
            plt.xlabel("produtos")
            plt.show()

while not auth:
    option = int(input('\nOpção 1: Login\nOpção 2: Cadastro\nOpção 3: Sair\n\n'))

    try:
        with connection.cursor() as c:
            c.execute('select * from cadastros')
            resp = c.fetchall()
    except:
        print('DB connection error')

    auth, admin = sing_in_up(option)

if auth:
    opt = 100

    if admin:
        while opt != 0:
            opt = int(input('\nOpção 1: Cadastro de produtos\
                            \tOpção 2: Listar catálogo de produtos\
                            \nOpção 3: Cadastrar Pedidos    \
                            \tOpção 4: Listar pedidos\
                            \nOpção 5: Relatorio            \
                            \n\nOpção 0: Sair\n\n'))

            if opt == 1:
                cadProd()
            elif opt == 2:
                catalogo()
                o = input('\n Deseja deletar um produto? (s/N) ')
                if o == 's':
                    delProd()
                else:
                    continue
            elif opt == 3:
                cadPed()
            elif opt == 4:
                listOrders()
            elif opt == 5:
                stat()
    else:
        while opt != 0:
            opt = int(input('\nOpção 1: Listar pedidos\
                            \nOpção 2: Criar pedido\
                            \n\nOpção 0: Sair\n\n'))

            if opt == 1:
                listOrders()
            elif opt == 2:
                cadPed()

    
