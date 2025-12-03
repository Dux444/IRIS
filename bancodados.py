import sqlite3
import os

#Criando BD
def criar_banco():
    if not os.path.exists('usuarios.db'):
        conexao = sqlite3.connect('usuarios.db')
        cursor = conexao.cursor()
        cursor.execute( """ 
            CREATE TABLE usuarios (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       senha TEXT NOT NULL
            );
        """)        
        conexao.commit()
        conexao.close()
        print('Banco de Dados e Tabela sendo criados com sucesso!')

# Criando Usuário
def criar_usuario(nome, senha):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO usuarios (nome, senha) VALUES (?, ?)', (nome, senha))
    conexao.commit()
    conexao.close()

#Listar Todos os Usuários
def listar_usuarios():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT id, nome FROM usuarios')
    usuarios = cursor.fetchall()
    conexao.close()

    print('\n--- Usuários Cadastrados ---')
    for usuario in usuarios:
        print (f'ID: {usuario[0]} | Nome: {usuario[1]}')
    print('----------------------------\n')

#Atualizar Senha do Usuário
def editar_senha(nome, nova_senha):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('UPDATE usuarios SET senha = ? WHERE nome = ?', (nova_senha, nome))
    conexao.commit()
    conexao.close
    print(f'Senha do usuário {nome} atualizada.')

#Remover Usuário
def remover_usuario(nome):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM usuarios WHERE nome = ?', (nome,))
    conexao.commit()
    conexao.close()
    print(f'Usuário {nome} removido.')

# Validando Login
def validar_login(usuario, senha):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?', (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado is not None 

# Verificando Usuário
def usuario_existe(nome):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
    existe = cursor.fetchone() is not None
    conexao.close()
    return existe

# CRUD tabela usuários via terminal
if __name__ == '__main__':
    criar_banco()

    while True:
        print('--- MENU ---')
        print('1 - Cadastrar novo usuário')
        print('2 - Listar usuários')
        print('3 - Editar senha do usuário')
        print('4 - Remover usuário')
        print('5 - Sair')

        escolha = int(input('Escolha um opção: '))
        if escolha == 1:
            nome = input('Nome do novo usuário: ').strip()
            senha = input('Senha: ').strip()
            criar_usuario(nome, senha)

        elif escolha == 2:
            listar_usuarios()

        elif escolha == 3:
            nome = input('Usuário para alterar senha: ').strip()
            nova_senha = input('Nova senha: ').strip()
            editar_senha(nome, nova_senha)

        elif escolha == 4:
            nome = input('Nome do usuário a remover: ').strip()
            remover_usuario(nome)

        elif escolha == 5:
            print('Saindo...')
            break

        else:
            print('Opção inválida.')

def validar_login(nome, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    resultado = cursor.fetchone()
    
    conexao.close()
    
    return resultado is not None


def cadastrar_usuario(nome, senha):
    if not nome or not senha:  # Verifica se algum campo está vazio
        return "Todos os campos são obrigatórios!"

    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))
        conexao.commit()
        conexao.close()
        return "Cadastro realizado com sucesso!"
    except sqlite3.IntegrityError:
        conexao.close()
        return "Erro ao cadastrar. Nome de usuário já está em uso."


