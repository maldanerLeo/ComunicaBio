import MySQLdb

print(f"\n{45*'*'}")
print(f"{10*' '}BEM VINDO AO COMUNICABIO")
print(f"{45*'*'}\n")

while True:
    usuario = str(input("Insira o nome de usuário local do MySQL: "))
    senha = str(input("Insira a senha do usuário local do MySQL: "))
    base = str(input("Insira o nome de uma base de dados existente no MySQL: "))

    host = 'localhost'
    user = f"{usuario}"
    password = f"{senha}"
    db = f"{base}"
    port = 3306

    try:
        con = MySQLdb.connect(host, user, password, db, port)
        c = con.cursor()
        print("\nConexão estabelecida com sucesso!\n")
        break
    except:
        print("\nAlgo deu errado!\nVerifique o nome de usuário, senha ou nome do banco de dados.\n")


try:
    query = "CREATE SCHEMA `data_park`;"
    c.execute(query)
    print("Base de dados 'data_park' foi criada\n")

    n_tabela = "CREATE TABLE `data_park`.`dados` (  `id_user` INT NOT NULL AUTO_INCREMENT," \
           "  `nome` VARCHAR(100) NOT NULL,  `email` VARCHAR(70) NOT NULL," \
           "  `data_hora` DATETIME NOT NULL,  `mensagem` VARCHAR(500) NOT NULL, " \
           " `situacao` VARCHAR(50) NOT NULL,  PRIMARY KEY (`id_user`));"
    c.execute(n_tabela)
    print("A tabela data_park.dados foi criada\n")


except:
    print("Os agendamentos serão enviados para a tabela 'dados' da base 'data_park'.\n")

db = 'data_park'
con = MySQLdb.connect(host, user, password, db, port)
c = con.cursor()

def insert(values):
    global c, con
    # sintaxe para adição ->  INSERT INTO <table> (fields) VALUES (), (), ()
    query = "INSERT INTO " + "dados" + " VALUES " + ",".join(["(" + v + ")" for v in values])
    c.execute(query)
    con.commit()

def select(where):
    global c

    query = "Select " + "*" + " FROM " + "dados" + " WHERE " + where
    c.execute(query)
    return c.fetchall()

def delete(where):

    global c, con

    query = "DELETE FROM " + "dados" + " WHERE " + where
    c.execute(query)
    con.commit()

while True:
    resp = input(
        "Digite a opção desejada. \n1 - Adicionar novo agendamento."
        " \n2 - Verificar Status do agendamento. \n3 - Remover agendamento. \n4 - Sair. \nValor: ")
    try:
        resp = int(resp)
    except:
        print("\nOops, valor inválido, insira somente números!\n")

    if resp>4:
        print("\nValor inválido, insira o valor da opção deseja!\n")

    elif resp == 1:
        nome = input("Insira o nome do destinatário --> ")
        email = input("Insira o email -->  ")
        data = input("Insira a data e hora de envio (AAAA-MM-DD HH:MM:SS) --> ")
        mensagem = input("Insira a mensagem desejada --> ")
        value = [f"DEFAULT, '{nome}', '{email}', '{data}', '{mensagem}', 'Aguardando Envio'"]

        try:
            insert(value)
            print("\nDados inseridos com sucesso!")
        except:
            print("\nOops, o formato da data inserida não está correto!\n"
                  "A data de ser da seguinte forma: ANO-MÊS-DIA HORA:MINUTOS:SEGUNDOS\n")
            data = input("Insira a data e hora de envio (AAAA-MM-DD HH:MM:SS) --> ")
            value = [f"DEFAULT, '{nome}', '{email}', '{data}', '{mensagem}', 'Aguardando Envio'"]
            try:
                insert(value)
                print("\nDados inseridos com sucesso!")
            except:
                print("Data inválida pela segunda vez!\nPreencha os dados novamente.")

    elif resp == 2:
        sel_id = input("\nInsira o número de identificação do agendamento desejado --> ")
        try:
            sel_id=int(sel_id)
        except:
            print("\nOops, valor inválido, insira somente números!\n")

        selecao = select(f"id_user = {sel_id}")

        if selecao==():
            print("\nNão foram encontrados agendamentos para a ID inserida.\n")
        else:
            print(f"\nO status da mensagem do usuário {selecao[0][1]} é: {selecao[0][5]}\n")

    elif resp == 3:
        del_id = input("\nInsira o número de identificação do agendamento que você deseja remover --> ")
        try:
            del_id = int(del_id)
        except:
            print("\nOops, valor inválido, insira somente números!\n")

        selecao = select(f"id_user = {del_id}")

        if selecao == ():
            print("\nNão foram encontrados agendamentos para a ID inserida.\n")
        else:
            confirma = input(f"\nVocê está prestes a deletar o seguinte agendamento:\nNome -> {selecao[0][1]}\n"
                  f"Email-> {selecao[0][2]}\nData e Hora -> {selecao[0][3]}\nMensage ->: {selecao[0][4]}\nDeseja"
                  f" prosseguir com a exclusão?\n1 - SIM\n2 - NÃO\nResporta: ")

            try:
                confirma = int(confirma)
            except:
                   print("\nOops, valor inválido, insira somente números!\n")

            if confirma == 1:
                delete(f"id_user = {del_id}")
                print("\nAgendamento deletado!\n")
            elif confirma == 2:
                print("\nO agendamento foi mantido!\n")
            else:
                print("\nO valor inserido é diferente de 1 ou 2!\n")

    elif resp==4:
        break