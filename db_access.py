import sqlite3
from datetime import datetime, timedelta
# import random # Descomente se for usar a biblioteca random neste arquivo (ex: para popular preços)
from config import NOME_BANCO_DADOS # Importa o nome do BD

def listar_produtos_db():
    """Retorna uma lista com os nomes de todos os produtos cadastrados, ordenados alfabeticamente."""
    conn = None # Inicializa conn como None para o bloco finally
    try:
        conn = sqlite3.connect(NOME_BANCO_DADOS)
        cursor = conn.cursor()
        cursor.execute("SELECT Nome FROM Produtos ORDER BY Nome ASC")
        lista_produtos = [row[0] for row in cursor.fetchall()]
        return lista_produtos
    except sqlite3.Error as e:
        print(f"Erro ao listar produtos do banco de dados: {e}")
        return [] # Retorna lista vazia em caso de erro
    finally:
        if conn:
            conn.close()

def obter_estatisticas_produto_detalhado(nome_produto):
    """
    Busca estatísticas de um produto nos últimos 30 dias.
    Retorna: unidade, preco_medio, preco_min, preco_max, data_primeiro_preco_db, data_ultimo_preco_db.
    Retorna None para os valores de preço/data se não houver dados de preço.
    As datas (data_primeiro_preco_db, data_ultimo_preco_db) são strings no formato YYYY-MM-DD HH:MM:SS.
    """
    conn = None # Inicializa conn como None
    unidade_produto = None # Inicializa para o caso de erro antes da primeira atribuição
    try:
        conn = sqlite3.connect(NOME_BANCO_DADOS)
        cursor = conn.cursor()
        
        # Primeiro, busca o ID e a Unidade do produto
        cursor.execute("SELECT ID, Unidade FROM Produtos WHERE Nome = ?", (nome_produto,))
        produto_row = cursor.fetchone()

        if not produto_row:
            return None, None, None, None, None, None # Produto não encontrado

        produto_id = produto_row[0]
        unidade_produto = produto_row[1]

        data_limite_iso = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            SELECT AVG(Valor), MIN(Valor), MAX(Valor), MIN(DataColeta), MAX(DataColeta)
            FROM Precos
            WHERE ProdutoID = ? AND DataColeta >= ?
        """, (produto_id, data_limite_iso))
        
        estatisticas = cursor.fetchone()

        if estatisticas and estatisticas[0] is not None: # AVG (estatisticas[0])
            preco_medio, preco_min, preco_max, data_primeiro_preco_db, data_ultimo_preco_db = estatisticas
            return unidade_produto, preco_medio, preco_min, preco_max, data_primeiro_preco_db, data_ultimo_preco_db
        else: # Não há preços nos últimos 30 dias ou produto não tem preços
            return unidade_produto, None, None, None, None, None 
            
    except sqlite3.Error as e:
        print(f"Erro ao obter estatísticas do produto '{nome_produto}': {e}")
        # Tenta retornar unidade se já obteve, caso contrário None para unidade também
        return unidade_produto if unidade_produto else None, None, None, None, None, None
    finally:
        if conn:
            conn.close()

def inicializar_db():
    """Cria as tabelas do banco de dados se não existirem e popula produtos iniciais."""
    conn = None
    try:
        conn = sqlite3.connect(NOME_BANCO_DADOS)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Produtos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT UNIQUE NOT NULL,
                Unidade TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Precos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ProdutoID INTEGER NOT NULL,
                Valor REAL NOT NULL,
                DataColeta TEXT NOT NULL,     -- Formato YYYY-MM-DD HH:MM:SS
                SupermercadoNome TEXT,        -- NOVA COLUNA
                FOREIGN KEY (ProdutoID) REFERENCES Produtos (ID)
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM Produtos")
        if cursor.fetchone()[0] == 0:
            produtos_iniciais = [
                ("arroz", "kg"), ("feijão", "kg"), ("leite", "litro"),
                ("pão", "pacote"), ("ovo", "dúzia"), ("carne", "kg"),
                ("frango", "kg"), ("banana", "kg")
            ]
            cursor.executemany("INSERT INTO Produtos (Nome, Unidade) VALUES (?, ?)", produtos_iniciais)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def adicionar_novo_produto_db(nome, unidade):
    conn = None 
    try:
        conn = sqlite3.connect(NOME_BANCO_DADOS)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Produtos (Nome, Unidade) VALUES (?, ?)", (nome, unidade))
        conn.commit()
        return True, f"Produto '{nome.capitalize()}' adicionado com sucesso!"
    except sqlite3.IntegrityError: 
        return False, f"Erro: Produto '{nome.capitalize()}' já existe no banco de dados."
    except sqlite3.Error as e:
        print(f"Erro ao adicionar novo produto: {e}")
        return False, f"Ocorreu um erro sqlite ao adicionar o produto: {e}"
    except Exception as e: 
        print(f"Ocorreu um erro inesperado ao adicionar produto: {e}")
        return False, f"Ocorreu um erro inesperado ao adicionar o produto: {e}"
    finally:
        if conn:
            conn.close()
            
def adicionar_preco_db(produto_id, valor, data_coleta_iso, supermercado_nome): # Novo parâmetro
    """
    Adiciona um novo registro de preço para um produto específico.
    A data_coleta_iso deve estar no formato 'YYYY-MM-DD HH:MM:SS'.
    Retorna (True, "Mensagem de sucesso") ou (False, "Mensagem de erro").
    """
    conn = None
    try:
        conn = sqlite3.connect(NOME_BANCO_DADOS)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Precos (ProdutoID, Valor, DataColeta, SupermercadoNome) VALUES (?, ?, ?, ?)",
                       (produto_id, valor, data_coleta_iso, supermercado_nome)) # Adicionado supermercado_nome
        conn.commit()
        return True, "Registro de preço adicionado com sucesso!"
    except sqlite3.Error as e:
        print(f"Erro ao adicionar preço ao banco de dados: {e}")
        return False, f"Erro ao adicionar preço: {e}"
    finally:
        if conn:
            conn.close()
            
def obter_produto_id_por_nome(nome_produto):
    conn = None
    try:
        conn = sqlite3.connect(NOME_BANCO_DADOS)
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM Produtos WHERE Nome = ?", (nome_produto,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        return None
    except sqlite3.Error as e:
        print(f"Erro ao buscar ID do produto '{nome_produto}': {e}")
        return None
    finally:
        if conn:
            conn.close()                       

# Função para popular preços aleatórios (que usa o 'import random'),
# def popular_precos_iniciais_aleatorios():
#     import random # Verificar se o IMPORT RANDOM está ativa no topo ou descomentar aqui
#     conn = sqlite3.connect(NOME_BANCO_DADOS)
#     cursor = conn.cursor()
#     try:
#         cursor.execute("SELECT ID, Nome FROM Produtos")
#         produtos_db = cursor.fetchall()
#         if not produtos_db:
#             print("Nenhum produto no banco para popular preços.")
#             return

#         # Exemplo simples de faixa de preço (poderia ser mais elaborado)
#         faixas_preco_exemplo = {
#             "arroz": (8, 15), "feijão": (5, 10), "leite": (3, 6),
#             "pão": (6, 10), "ovo": (8, 14), "carne": (25, 50),
#             "frango": (12, 25), "banana": (3, 7)
#         }

#         for produto_id, nome_produto in produtos_db:
#             min_val, max_val = faixas_preco_exemplo.get(nome_produto.lower(), (1, 2)) # Faixa padrão
#             for i in range(30): # AQUI ADICONA 30 PREÇOS PARA CADA
#                 preco = round(random.uniform(min_val, max_val), 2)
#                 data_coleta = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
#                 cursor.execute("INSERT INTO Precos (ProdutoID, Valor, DataColeta) VALUES (?, ?, ?)",
#                                (produto_id, preco, data_coleta))
#         conn.commit()
#         print("Dados de preços aleatórios iniciais populados.")
#     except sqlite3.Error as e:
#         print(f"Erro ao popular preços aleatórios: {e}")
#     finally:
#         if conn:
#             conn.close()