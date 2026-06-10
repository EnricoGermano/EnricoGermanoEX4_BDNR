import requests
import uuid

TOKEN    = "AstraCS:DispiDxbYtNrGZRpwmAwvmNm:e767caafedeed52a8346e03ed33ce2c6b9d0d088dd777116cfb4535ee7d8a3ab"
BASE     = "https://a67c41c2-f29f-4623-88ed-88980b2111ac-us-east-2.apps.astra.datastax.com/api/rest/v2/keyspaces/default_keyspace"
HEADERS  = {"X-Cassandra-Token": TOKEN, "Content-Type": "application/json"}

def listar_produtos():
    r = requests.get(f"{BASE}/produtos/rows", headers=HEADERS)
    if r.status_code == 200:
        return r.json().get("data", [])
    return []

def selecionar_produto():
    produtos = listar_produtos()
    if not produtos:
        print("Nenhum produto cadastrado.")
        return None
    print("\nProdutos disponíveis:")
    for i, p in enumerate(produtos, 1):
        print(f"  {i}. {p.get('nome')} | Valor: {p.get('valor')} | Desc: {p.get('descricao')}")
    while True:
        try:
            op = int(input("Escolha o numero do produto: "))
            if 1 <= op <= len(produtos):
                return produtos[op - 1]
            print("Numero invalido.")
        except ValueError:
            print("Digite um numero valido.")

def insert_usuario():
    print("\n--- Inserir Usuario ---")
    cpf       = input("CPF: ")
    nome      = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email     = input("Email: ")
    cc        = input("CC: ")
    endereco  = input("Endereco: ")
    senha     = input("Senha: ")

    fav_id = fav_nome = fav_desc = fav_valor = ""
    if input("Deseja cadastrar um favorito? (s/n): ").strip().lower() == "s":
        produto = selecionar_produto()
        if produto:
            fav_id    = produto.get("id", "")
            fav_nome  = produto.get("nome", "")
            fav_desc  = produto.get("descricao", "")
            fav_valor = produto.get("valor", "")

    r = requests.post(f"{BASE}/usuarios", headers=HEADERS, json={
        "cpf": cpf, "nome": nome, "sobrenome": sobrenome,
        "email": email, "cc": cc, "endereco": endereco, "senha": senha,
        "favorito_id": fav_id, "favorito_nome": fav_nome,
        "favorito_descricao": fav_desc, "favorito_valor": fav_valor
    })
    print("Inserido." if r.status_code in [200, 201] else f"Erro: {r.text}")

def insert_vendedor():
    print("\n--- Inserir Vendedor ---")
    cnpj      = input("CNPJ: ")
    nome      = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email     = input("Email: ")
    senha     = input("Senha: ")
    r = requests.post(f"{BASE}/vendedores", headers=HEADERS, json={
        "cnpj": cnpj, "nome": nome, "sobrenome": sobrenome,
        "email": email, "senha": senha
    })
    print("Inserido." if r.status_code in [200, 201] else f"Erro: {r.text}")

def insert_produto():
    print("\n--- Inserir Produto ---")
    nome          = input("Nome: ")
    descricao     = input("Descricao: ")
    valor         = input("Valor: ")
    vendedor_cnpj = input("CNPJ do Vendedor: ")
    r = requests.post(f"{BASE}/produtos", headers=HEADERS, json={
        "id": str(uuid.uuid4()), "nome": nome,
        "descricao": descricao, "valor": valor,
        "vendedor_cnpj": vendedor_cnpj
    })
    print("Inserido." if r.status_code in [200, 201] else f"Erro: {r.text}")

def insert_pedido():
    print("\n--- Inserir Pedido ---")
    cliente_cpf = input("CPF do Cliente: ")
    produto = selecionar_produto()
    if not produto:
        return
    r = requests.post(f"{BASE}/pedidos", headers=HEADERS, json={
        "id": str(uuid.uuid4()),
        "cliente_cpf": cliente_cpf,
        "produto_id": produto.get("id")
    })
    print("Inserido." if r.status_code in [200, 201] else f"Erro: {r.text}")

def update_usuario():
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
    r = requests.put(f"{BASE}/usuarios/{cpf}", headers=HEADERS, json={campo: valor})
    print("Atualizado." if r.status_code in [200, 201] else f"Erro: {r.text}")

def delete_pedido():
    print("\n--- Deletar Pedido ---")
    r = requests.get(f"{BASE}/pedidos/rows", headers=HEADERS)
    if r.status_code != 200:
        print(f"Erro ao listar pedidos: {r.text}")
        return
    pedidos = r.json().get("data", [])
    if not pedidos:
        print("Nenhum pedido encontrado.")
        return
    print("\nPedidos:")
    for i, p in enumerate(pedidos, 1):
        print(f"  {i}. Cliente: {p.get('cliente_cpf')} | Produto: {p.get('produto_id')}")
    while True:
        try:
            op = int(input("Escolha o numero do pedido: "))
            if 1 <= op <= len(pedidos):
                pedido_id = pedidos[op - 1].get("id")
                break
            print("Numero invalido.")
        except ValueError:
            print("Digite um numero valido.")
    r = requests.delete(f"{BASE}/pedidos/{pedido_id}", headers=HEADERS)
    print("Deletado." if r.status_code in [200, 204] else f"Erro: {r.text}")

def buscar_produto():
    print("\n--- Buscar Produto ---")
    print("1. Por numero  2. Listar todos")
    op = input("Opcao: ")
    if op == "1":
        produto = selecionar_produto()
        if produto:
            print(f"  ID: {produto.get('id')} | Nome: {produto.get('nome')} | Descricao: {produto.get('descricao')} | Valor: {produto.get('valor')} | Vendedor: {produto.get('vendedor_cnpj')}")
    elif op == "2":
        produtos = listar_produtos()
        if not produtos:
            print("Nenhum produto encontrado.")
        for i, p in enumerate(produtos, 1):
            print(f"  {i}. ID: {p.get('id')} | Nome: {p.get('nome')} | Descricao: {p.get('descricao')} | Valor: {p.get('valor')} | Vendedor: {p.get('vendedor_cnpj')}")
    else:
        print("Opcao invalida.")

def menu():
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
            if sub == "1": insert_usuario()
            elif sub == "2": insert_vendedor()
            elif sub == "3": insert_produto()
            elif sub == "4": insert_pedido()
            else: print("Opcao invalida.")
        elif op == "2": update_usuario()
        elif op == "3": delete_pedido()
        elif op == "4": buscar_produto()
        elif op == "0": break
        else: print("Opcao invalida.")

if __name__ == "__main__":
    menu()