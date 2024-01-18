import sqlite3

class Produto:
    def __init__(self, codigo, nome, produto, quantidade, valor):
        self.codigo = codigo
        self.nome = nome
        self.produto = produto
        self.quantidade = quantidade
        self.valor = valor

    def exibir_informacoes(self):
        print("-------------------------")
        print(f"Código: {self.codigo}")
        print(f"Nome: {self.nome}")
        print(f"Produto: {self.produto}")
        print(f"Quantidade em Estoque: {self.quantidade}")
        print(f"Valor: R${self.valor}")
        print("-------------------------")

def adicionar_produto():
    while True:
        codigo = input("Código: ")
        nome = input("Nome: ")
        produto = input("Produto: ")
        quantidade = int(input("Quantidade: "))
        valor = float(input("Valor (use . para simbolizar número fracionado): "))
        
        cursor.execute('SELECT * FROM produtos WHERE codigo = ? OR nome = ? OR produto = ?', (codigo, nome, produto))
        produtoExistente = cursor.fetchone()

        if produtoExistente:
            print("Erro: Produto com código, nome ou produto já existente. Tente novamente!")

        else:
            cursor.execute('''
                INSERT INTO produtos (codigo, nome, produto, quantidade, valor)
                VALUES (?, ?, ?, ?, ?)
            ''', (codigo, nome, produto, quantidade, valor))
            connection.commit()

            novo_produto = Produto(codigo, nome, produto, quantidade, valor)
            estoque[codigo] = novo_produto
            print("Item Adicionado com sucesso! ")
            break

def procurarProduto():
    print("1 - Mostrar todos")
    print("2 - Procurar por código")
    todos = input("Como você deseja procurar? ")
    if todos == '1':
        cursor.execute('SELECT * FROM produtos')
        all_produto_data = cursor.fetchall()
        for produto_data in all_produto_data:
            codigo_produto = produto_data[0]
            estoque[codigo_produto] = Produto(*produto_data)
            estoque[codigo_produto].exibir_informacoes()
            
    if todos == '2':
        codigo_produto = input("Digite o código do produto para exibir informações: ")
        cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (codigo_produto,))
        produto_data = cursor.fetchone()
        if produto_data:
            estoque[codigo_produto] = Produto(*produto_data)
            estoque[codigo_produto].exibir_informacoes()
        else:
            print("Produto não encontrado.")


def editarProduto():
    qualEditar = input("Digite o código do item que deseja editar: ")
    cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (qualEditar,))
    produto_data = cursor.fetchone()

    if produto_data:
        produto_atual = Produto(*produto_data)
        produto_atual.exibir_informacoes()

        print("Opções de edição:")
        print("1 - Código")
        print("2 - Nome")
        print("3 - Produto")
        print("4 - Quantidade")
        print("5 - Valor")

        opcao = input("Escolha o que deseja editar (1-5): ")

        if opcao == '1':
            novo_codigo = input(f"Novo código ({produto_atual.codigo}): ")
            cursor.execute('UPDATE produtos SET codigo = ? WHERE codigo = ?', (novo_codigo, qualEditar))
        elif opcao == '2':
            novo_nome = input(f"Novo produto ({produto_atual.nome}): ")
            cursor.execute('UPDATE produtos SET nome = ? WHERE codigo = ?', (novo_nome, qualEditar))
        elif opcao == '3':
            novo_produto = int(input(f"Novo produto ({produto_atual.produto}): "))
            cursor.execute('UPDATE produtos SET produto = ? WHERE codigo = ?', (novo_produto, qualEditar))
        elif opcao == '4':
            nova_quantidade = input(f"Nova quantidade ({produto_atual.quantidade}): ")
            cursor.execute('UPDATE produtos SET quantidade = ? WHERE codigo = ?', (nova_quantidade, qualEditar))
        elif opcao == '5':
            novo_valor = float(input(f"Novo valor ({produto_atual.valor}): "))
            cursor.execute('UPDATE produtos SET valor = ? WHERE codigo = ?',(novo_valor, qualEditar))
        else:
            print("Opção inválida.")

        connection.commit()
        print("Produto atualizado com sucesso.")
    else:
        print("Produto não encontrado.")

def excluirProduto():
    cursor.execute('SELECT * FROM produtos')
    all_produto_data = cursor.fetchall()

    if all_produto_data:
        for produto_data in all_produto_data:
            codigo_produto = produto_data[0]
            estoque[codigo_produto] = Produto(*produto_data)
            estoque[codigo_produto].exibir_informacoes()

    qualExcluir = input("Digite o código do item que deseja excluir: ")
    cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (qualExcluir,))
    cursor.execute('SELECT * FROM produtos')
        
    if produto_data:
        produto_atual = Produto(*produto_data)
        produto_atual.exibir_informacoes()

        confirmacao = input("Tem certeza que deseja excluir este produto? (s/n): ").lower()

        if confirmacao == 's':
            cursor.execute('DELETE FROM produtos WHERE codigo = ?', (qualExcluir,))
            connection.commit()
            print("Produto excluído com sucesso.")
        else:
            print("Operação de exclusão cancelada.")
    else:
        print("Produto não encontrado.")
    
connection = sqlite3.connect('estoque.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        codigo TEXT PRIMARY KEY,
        nome TEXT,
        produto TEXT,
        quantidade INTEGER,
        valor DECIMAL(8,2)
    )
''')
connection.commit()

estoque = {}

if __name__ == '__main__':
    print("1 - Adicionar produto")
    print("2 - Procurar produto")
    print("3 - Editar produto")
    print("4 - Excluir produto")
    print("5 - Sair")

    while True:
        try:
            inicio = int(input("Escolha uma opção: "))
            
            if not isinstance(inicio, int):
                print("Escolha uma das opções acima. Tente novamente.")
                continue
            
            if inicio == 1:
                adicionar_produto()
                
            elif inicio == 2:
                procurarProduto()

            elif inicio == 3:
                editarProduto()

            elif inicio == 4:
                excluirProduto()

            elif inicio == 5:
                print("Saindo...")
                connection.close()
                exit()

            else:
                print("Opção inválida. Tente novamente.")
                
        except ValueError:
            print("Erro: Insira um número inteiro para a opção.")