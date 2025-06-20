import sqlite3
import pandas as pd
from config import NOME_BANCO_DADOS # Reutiliza a configuração do projeto

def criar_relatorio_de_precos():
    """
    Conecta ao banco de dados, busca todos os preços registrados,
    junta com os nomes dos produtos e retorna um DataFrame do Pandas.
    """
    print(f"Conectando ao banco de dados: '{NOME_BANCO_DADOS}'...")
    
    try:
        # Conecta ao banco de dados SQLite
        conn = sqlite3.connect(NOME_BANCO_DADOS)
        print("Conexão estabelecida com sucesso!")

        # Query SQL para selecionar os dados de preços e juntar com os nomes dos produtos
        query = """
        SELECT
            p.Nome AS Produto,
            pr.SupermercadoNome AS Supermercado,
            pr.Valor,
            pr.DataColeta
        FROM Precos pr
        JOIN Produtos p ON pr.ProdutoID = p.ID
        ORDER BY pr.DataColeta DESC;
        """

        # O Pandas lê diretamente o resultado da consulta SQL para um DataFrame
        df = pd.read_sql_query(query, conn)

        # Converte a coluna de data para um formato mais legível
        if not df.empty:
            df['DataColeta'] = pd.to_datetime(df['DataColeta']).dt.strftime('%d/%m/%Y %H:%M')

        print("Relatório de preços gerado com sucesso!")
        return df

    except sqlite3.Error as e:
        print(f"Ocorreu um erro de banco de dados: {e}")
        return None # Retorna None em caso de erro
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    # Chama a função para criar o relatório
    relatorio_df = criar_relatorio_de_precos()

    # Verifica se o DataFrame foi criado e não está vazio
    if relatorio_df is not None and not relatorio_df.empty:
        print("\n--- Tabela de Preços Registrados ---")
        # .to_string() garante que todas as linhas e colunas sejam exibidas
        print(relatorio_df.to_string(index=False))
    elif relatorio_df is not None:
        print("\nNenhum preço registrado no banco de dados ainda.")
    else:
        print("\nNão foi possível gerar o relatório.")