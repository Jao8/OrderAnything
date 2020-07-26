import pymysql as sql
import pymysql.cursors as db

connection = sql.connect(
    host='localhost',
    user='root',
    password='',
    db='OA',
    charset='utf8mb4',
    cursorclass=db.DictCursor
)

auth = False

def sing_in_up():
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
                print('Bem-vindo, {}!'.format(nome))
                
        if Autorization is False:
            print('Usuario/Senha Incorreta')
    elif option == 2:
        print('Digite seus dados:\n')
        nome = input('\tDigite seu nome: ')
        senha = input('\tDigite sua senha: ')

        for res in resp:
            if nome == res['nome']:
                ExistingUser = 1
        
        if ExistingUser == 1:
            print('Usuario já existente')
        elif ExistingUser == 0:
            try:
                with connection.cursor() as c:
                    c.execute(f'insert into cadastros values (%s,%s,1)', (nome, senha))
                    connection.commit()      
                print('Usuario cadastrado com sucesso!')              
            except:
                print('Ocorreu um erro durante a inserção dos dados.\nPor favor contate um administrador.\n')
    
    return Autorization, AdminUser

while not auth:
    option = int(input('Opção 1: Login\nOpção 2: Cadastro\n\n'))

    try:
        with connection.cursor() as c:
            c.execute('select * from cadastros')
            resp = c.fetchall()
    except:
        print('DB connection error')

    auth, admin = sing_in_up()
