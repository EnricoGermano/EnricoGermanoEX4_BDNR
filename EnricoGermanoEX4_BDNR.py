from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.io.asyncioreactor import AsyncioConnection
import uuid

def conectar():
    cluster = Cluster(
        ['127.0.0.1'],
        connection_class=AsyncioConnection,
        load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1')
    )
    session = cluster.connect('mercadolivre')
    return session, cluster

def insert_usuario(session):
    print("\n--- Inserir Usuario ---")
    cpf       = input("CPF: ")
    nome      = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email     = input("Email: ")
    cc        = input("CC: ")
    endereco  = input("Endereco: ")
    senha     = input("Senha: ")
    fav_id    = input("ID do Favorito: ")
    fav_nome  = input("Nome do Favorito: ")
    fav_desc  = input("Descricao do Favorito: ")
    fav_valor = input("Valor do Favorito: ")
    session.execute("""
        INSERT INTO usuarios (cpf, nome, sobrenome, email, cc, endereco, senha,
                              favorito_id, favorito_nome, favorito_descricao, favorito_valor)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (cpf, nome, sobrenome, email, cc, endereco, senha,
          fav_id, fav_nome, fav_desc, fav_valor))
    print("Inserido.")

def insert_vendedor(session):
    print("\n--- Inserir Vendedor ---")
    cnpj      = input("CNPJ: ")
    nome      = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email     = input("Email: ")
    senha     = input("Senha: ")
    session.execute("""
        INSERT INTO vendedores (cnpj, nome, sobrenome, email, senha)
        VALUES (%s,%s,%s,%s,%s)
    """, (cnpj, nome, sobrenome, email, senha))
    print("Inserido.")

def insert_produto(session):
    print("\n--- Inserir Produto ---")
    nome          = input("Nome: ")
    descricao     = input("Descricao: ")
    valor         = input("Valor: ")
    vendedor_cnpj = input("CNPJ do Vendedor: ")
    session.execute("""
        INSERT INTO produtos (id, nome, descricao, valor, vendedor_cnpj)
        VALUES (%s,%s,%s,%s,%s)
    """, (uuid.uuid4(), nome, descricao, valor, vendedor_cnpj))
    print("Inserido.")

def insert_pedido(session):
    print("\n--- Inserir Pedido ---")
    cliente_cpf = input("CPF do Cliente: ")
    produto_id  = input("ID do Produto (UUID): ")
    try:
        pid = uuid.UUID(produto_id)
    except ValueError:
        print("UUID invalido.")
        return
    session.execute("""
        INSERT INTO pedidos (id, cliente_cpf, produto_id)
        VALUES (%s,%s,%s)
    """, (uuid.uuid4(), cliente_cpf, pid))
    print("Inserido.")

def update_usuario(session):
    print("\n--- Atualizar Usuario ---")
    cpf = input("CPF: ")
    print("1. Nome  2. Email  3. Endereco  4. CC  5. Senha")
    op = input("Opcao: ")
    campos = {"1": "nome", "2": "email", "3": "endereco", "4": "cc", "5": "senha"}
    if op not in campos:
        print("Opcao invalida.")
        return
    campo = campos[op]
    valor = input(f"Novo {campo}: ")
    session.execute(f"UPDATE usuarios SET {campo} = %s WHERE cpf = %s", (valor, cpf))
    print("Atualizado.")

def delete_pedido(session):
    print("\n--- Deletar Pedido ---")
    pedido_id = input("ID do Pedido (UUID): ")
    try:
        pid = uuid.UUID(pedido_id)
    except ValueError:
        print("UUID invalido.")
        return
    session.execute("DELETE FROM pedidos WHERE id = %s", (pid,))
    print("Deletado.")

def buscar_produto(session):
    print("\n--- Buscar Produto ---")
    print("1. Por ID  2. Listar todos")
    op = input("Opcao: ")
    if op == "1":
        try:
            pid = uuid.UUID(input("ID (UUID): "))
        except ValueError:
            print("UUID invalido.")
            return
        rows = session.execute("SELECT * FROM produtos WHERE id = %s", (pid,))
    elif op == "2":
        rows = session.execute("SELECT * FROM produtos")
    else:
        print("Opcao invalida.")
        return
    resultados = list(rows)
    if not resultados:
        print("Nenhum produto encontrado.")
    for row in resultados:
        print(f"  ID: {row.id} | Nome: {row.nome} | Descricao: {row.descricao} | Valor: {row.valor} | Vendedor: {row.vendedor_cnpj}")

def menu():
    session, cluster = conectar()
    while True:
        print("\n=== MERCADO LIVRE ===")
        print("1. Inserir")
        print("2. Atualizar Usuario")
        print("3. Deletar Pedido")
        print("4. Buscar Produto")
        print("0. Sair")
        op = input("Opcao: ")
        if op == "1":
            print("1. Usuario  2. Vendedor  3. Produto  4. Pedido")
            sub = input("Opcao: ")
            if sub == "1": insert_usuario(session)
            elif sub == "2": insert_vendedor(session)
            elif sub == "3": insert_produto(session)
            elif sub == "4": insert_pedido(session)
            else: print("Opcao invalida.")
        elif op == "2": update_usuario(session)
        elif op == "3": delete_pedido(session)
        elif op == "4": buscar_produto(session)
        elif op == "0":
            cluster.shutdown()
            break
        else:
            print("Opcao invalida.")

if __name__ == "__main__":
    menu()