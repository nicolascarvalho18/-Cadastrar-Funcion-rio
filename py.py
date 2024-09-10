import sqlite3
from datetime import datetime

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

# Criar tabelas
def criar_tabelas():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registro_ponto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcionario_id INTEGER,
        entrada DATETIME,
        saida DATETIME,
        FOREIGN KEY(funcionario_id) REFERENCES funcionarios(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcionario_id INTEGER,
        valor REAL,
        data DATETIME,
        FOREIGN KEY(funcionario_id) REFERENCES funcionarios(id)
    )
    ''')

    conn.commit()

# Função para cadastrar funcionários
def cadastrar_funcionario(nome):
    cursor.execute('''
    INSERT INTO funcionarios (nome)
    VALUES (?)
    ''', (nome,))
    conn.commit()
    print(f"Funcionário {nome} cadastrado com sucesso.")

# Registrar entrada do funcionário
def registrar_entrada(funcionario_id):
    entrada = datetime.now()
    cursor.execute('''
    INSERT INTO registro_ponto (funcionario_id, entrada)
    VALUES (?, ?)
    ''', (funcionario_id, entrada))
    conn.commit()
    print(f"Entrada registrada para o funcionário {funcionario_id} às {entrada}.")

# Registrar saída do funcionário
def registrar_saida(funcionario_id):
    saida = datetime.now()
    cursor.execute('''
    UPDATE registro_ponto
    SET saida = ?
    WHERE funcionario_id = ? AND saida IS NULL
    ''', (saida, funcionario_id))
    conn.commit()
    print(f"Saída registrada para o funcionário {funcionario_id} às {saida}.")

# Registrar vendas
def registrar_venda(funcionario_id, valor):
    data = datetime.now()
    cursor.execute('''
    INSERT INTO vendas (funcionario_id, valor, data)
    VALUES (?, ?, ?)
    ''', (funcionario_id, valor, data))
    conn.commit()
    print(f"Venda de R${valor:.2f} registrada para o funcionário {funcionario_id}.")

# Melhor funcionário do mês
def melhor_funcionario_do_mes():
    mes_atual = datetime.now().month
    cursor.execute('''
    SELECT f.nome, SUM(v.valor) AS total_vendas
    FROM vendas v
    JOIN funcionarios f ON v.funcionario_id = f.id
    WHERE strftime('%m', v.data) = ?
    GROUP BY f.id
    ORDER BY total_vendas DESC
    LIMIT 1
    ''', (str(mes_atual).zfill(2),))
    
    resultado = cursor.fetchone()
    if resultado:
        print(f"Melhor funcionário do mês: {resultado[0]} com R${resultado[1]:.2f} em vendas.")
    else:
        print("Nenhuma venda registrada neste mês.")

# Listar funcionários cadastrados
def listar_funcionarios():
    cursor.execute('SELECT * FROM funcionarios')
    funcionarios = cursor.fetchall()
    if funcionarios:
        print("Funcionários cadastrados:")
        for func in funcionarios:
            print(f"ID: {func[0]}, Nome: {func[1]}")
    else:
        print("Nenhum funcionário cadastrado.")

# Menu principal
def menu():
    while True:
        print("\n1. Cadastrar Funcionário")
        print("2. Registrar Entrada")
        print("3. Registrar Saída")
        print("4. Registrar Venda")
        print("5. Melhor Funcionário do Mês")
        print("6. Listar Funcionários")
        print("0. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            nome = input("Digite o nome do funcionário: ")
            cadastrar_funcionario(nome)
        
        elif escolha == '2':
            listar_funcionarios()
            funcionario_id = int(input("Digite o ID do funcionário para registrar entrada: "))
            registrar_entrada(funcionario_id)
        
        elif escolha == '3':
            listar_funcionarios()
            funcionario_id = int(input("Digite o ID do funcionário para registrar saída: "))
            registrar_saida(funcionario_id)
        
        elif escolha == '4':
            listar_funcionarios()
            funcionario_id = int(input("Digite o ID do funcionário para registrar venda: "))
            valor = float(input("Digite o valor da venda: "))
            registrar_venda(funcionario_id, valor)
        
        elif escolha == '5':
            melhor_funcionario_do_mes()
        
        elif escolha == '6':
            listar_funcionarios()
        
        elif escolha == '0':
            print("Saindo do sistema.")
            break
        
        else:
            print("Opção inválida, tente novamente.")

# Executar o sistema
if __name__ == '__main__':
    criar_tabelas()
    menu()

# Fechar conexão com o banco de dados
conn.close()
