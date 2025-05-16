import db_access
import utils
import config
from datetime import datetime # Para formatar a data de exibição

def exibir_menu_principal():
    utils.clear_screen() # Limpa a tela antes de exibir o menu
    print("\n--- Sistema de Acompanhamento de Preços ---")
    print("===========================================") 
    print("1. Ver Estatísticas de Preço de um Produto")
    print("2. Listar Todos os Produtos Cadastrados")
    print("3. Adicionar Novo Produto ao Sistema")
    print("4. Adicionar Novo Registro de Preço para um Produto")
    print("-------------------------------------------")
    print("0. Sair do Sistema")
    print("===========================================")
    return input("Escolha uma opção: ")

def gerenciar_listagem_todos_produtos():
    utils.clear_screen() # Limpa a tela
    print("\n--- Lista de Todos os Produtos Cadastrados ---")
    print("==============================================")
    produtos = db_access.listar_produtos_db()
    if not produtos:
        print("Nenhum produto cadastrado no momento.")
    else:
        for nome_produto in produtos:
            print(f"- {nome_produto.capitalize()}")
    print("-------------------------------------------")
    input("Pressione Enter para voltar ao menu...") # Pausa

def gerenciar_adicao_produto():
    utils.clear_screen() # Limpa a tela
    print("\n--- Adicionar Novo Produto ---")
    print("==============================")
    nome = input("Digite o nome do novo produto: ").lower()
    unidade = input(f"Digite a unidade para {nome.capitalize()} (ex: kg, litro, unidade): ").lower()
    sucesso, mensagem = db_access.adicionar_novo_produto_db(nome, unidade)
    print(mensagem)
    print("-------------------------------------------")
    input("Pressione Enter para voltar ao menu...") # Pausa
    
def gerenciar_adicao_preco_manual():
    utils.clear_screen()
    print("\n--- Adicionar Novo Registro de Preço ---")
    print("========================================")

    produtos_disponiveis = db_access.listar_produtos_db()

    if not produtos_disponiveis:
        print("Nenhum produto cadastrado. Adicione um produto antes de registrar preços.")
        input("Pressione Enter para voltar ao menu...")
        return

    print("\nProdutos disponíveis:")
    mapa_escolha_produto = {}
    for i, nome_produto in enumerate(produtos_disponiveis):
        print(f"{i+1}. {nome_produto.capitalize()}")
        mapa_escolha_produto[str(i+1)] = nome_produto
    
    print("-------------------------------------------")

    produto_selecionado_nome = None
    while True:
        escolha_numero_produto = input("Digite o NÚMERO do produto para adicionar o preço (ou '0' para voltar): ")
        if escolha_numero_produto == '0':
            return 
        produto_selecionado_nome = mapa_escolha_produto.get(escolha_numero_produto)
        if produto_selecionado_nome:
            break
        else:
            print("Opção de produto inválida. Tente novamente.")

    utils.clear_screen()
    print(f"--- Adicionar Preço para: {produto_selecionado_nome.capitalize()} ---")
    print("==================================================")

    produto_id = db_access.obter_produto_id_por_nome(produto_selecionado_nome)
    if produto_id is None:
        print(f"Erro: Não foi possível encontrar o ID para '{produto_selecionado_nome}'.")
        input("Pressione Enter para voltar ao menu...")
        return

    # Selecionar Supermercado
    print("\nSupermercados disponíveis:")
    mapa_escolha_supermercado = {}
    for i, nome_supermercado in enumerate(config.LISTA_SUPERMERCADOS):
        print(f"{i+1}. {nome_supermercado}")
        mapa_escolha_supermercado[str(i+1)] = nome_supermercado
    print("-------------------------------------------")
    
    supermercado_selecionado_nome = None
    while True:
        escolha_numero_supermercado = input("Digite o NÚMERO do supermercado (ou '0' para cancelar adição de preço): ")
        if escolha_numero_supermercado == '0':
            print("Adição de preço cancelada.")
            input("Pressione Enter para voltar ao menu...")
            return
        supermercado_selecionado_nome = mapa_escolha_supermercado.get(escolha_numero_supermercado)
        if supermercado_selecionado_nome:
            break
        else:
            print("Opção de supermercado inválida. Tente novamente.")
    
    utils.clear_screen()
    print(f"--- Adicionar Preço para: {produto_selecionado_nome.capitalize()} ---")
    print(f"--- Supermercado: {supermercado_selecionado_nome} ---")
    print("==================================================")

    while True:
        try:
            valor_str = input(f"Digite o valor do preço (ex: 10.99): R$ ")
            valor = float(valor_str)
            if valor < 0:
                print("O valor do preço não pode ser negativo.")
            else:
                break
        except ValueError:
            print("Valor inválido. Por favor, digite um número (ex: 10.99 ou 10).")

    data_coleta_iso = ""
    while True:
        # Exibe a data atual no formato dd/mm/yyyy
        formato_data_usuario = "%d/%m/%Y"
        data_sugerida_usr = datetime.now().strftime(formato_data_usuario)
        data_usr_str = input(f"Digite a data da coleta no formato {data_sugerida_usr} (ou deixe em branco para hoje): ")
        
        if not data_usr_str: 
            data_coleta_obj = datetime.now()
            data_coleta_iso = data_coleta_obj.strftime("%Y-%m-%d %H:%M:%S") 
            break
        else:
            try:
                data_coleta_obj = datetime.strptime(data_usr_str, formato_data_usuario)
                data_coleta_obj = data_coleta_obj.replace(hour=datetime.now().hour, minute=datetime.now().minute, second=datetime.now().second)
                data_coleta_iso = data_coleta_obj.strftime("%Y-%m-%d %H:%M:%S")
                break
            except ValueError:
                print(f"Formato de data inválido. Use {data_sugerida_usr}.")
    
    sucesso, mensagem = db_access.adicionar_preco_db(produto_id, valor, data_coleta_iso, supermercado_selecionado_nome)
    
    utils.clear_screen()
    print(f"--- Resultado da Adição de Preço ---")
    print("====================================")
    print(f"Produto: {produto_selecionado_nome.capitalize()}")
    print(f"Supermercado: {supermercado_selecionado_nome}")
    print(mensagem)
    if sucesso:
        data_confirmacao_usr = datetime.strptime(data_coleta_iso, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")
        print(f"Detalhes: Valor R$ {valor:.2f}, Data {data_confirmacao_usr}")
    
    print("-------------------------------------------")
    input("Pressione Enter para voltar ao menu principal...")

def gerenciar_estatisticas_produto():
    while True: # Loop principal
        utils.clear_screen() # Limpa a tela a cada nova iteração de consulta de produto
        print("\n--- Ver Estatísticas de Produto ---")
        print("===================================")
        produtos_disponiveis = db_access.listar_produtos_db()

        if not produtos_disponiveis:
            print("Nenhum produto cadastrado para exibir estatísticas.")
            input("Pressione Enter para voltar ao menu...")
            return 

        print("\nProdutos disponíveis para consulta:")
        mapa_escolha_produto = {}
        for i, nome_produto in enumerate(produtos_disponiveis):
            print(f"{i+1}. {nome_produto.capitalize()}")
            mapa_escolha_produto[str(i+1)] = nome_produto
        
        print("-------------------------------------------")
        escolha_numero = input("Digite o NÚMERO do produto (ou '0' para voltar ao menu): ")
        
        if escolha_numero == '0':
            break 
        
        produto_selecionado_nome = mapa_escolha_produto.get(escolha_numero)

        if produto_selecionado_nome:
            utils.clear_screen() # Limpa a tela antes de mostrar as estatísticas
            unidade, preco_medio, preco_min, preco_max, data_primeiro_preco_db, data_ultimo_preco_db = \
                db_access.obter_estatisticas_produto_detalhado(produto_selecionado_nome)
            
            print(f"\n--- Análise de Preços para: {produto_selecionado_nome.capitalize()} ({unidade}) ---")
            print("================================================================================")
            if unidade: 
                if preco_medio is not None: 
                    str_primeiro_preco_usr = datetime.strptime(data_primeiro_preco_db, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y') if data_primeiro_preco_db else "N/D"
                    str_ultimo_preco_usr = datetime.strptime(data_ultimo_preco_db, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y') if data_ultimo_preco_db else "N/D"

                    if data_primeiro_preco_db and data_ultimo_preco_db:
                         print(f"Período com preços (últimos 30 dias): de {str_primeiro_preco_usr} a {str_ultimo_preco_usr}")
                    else:
                         print("Período com preços (últimos 30 dias): Não há dados suficientes.")
                    print("--------------------------------------------------------------------------------")
                    print(f"Preço mais baixo: R$ {preco_min:.2f}")
                    print(f"Preço médio:      R$ {preco_medio:.2f}")
                    print(f"Preço mais alto:  R$ {preco_max:.2f}")
                    print("--------------------------------------------------------------------------------")
                else: 
                    print(f"\nNão foram encontrados registros de preços para {produto_selecionado_nome.capitalize()} ({unidade}) nos últimos 30 dias.")
            else: 
                print(f"\nProduto '{produto_selecionado_nome.capitalize()}' não encontrado (erro ao buscar detalhes).")
            
            print("\nPara uma nova consulta, pressione Enter.")
            print("Ou digite '0' na próxima tela de seleção para voltar ao menu principal.")
            input("Pressione Enter para continuar...")
        else:
            print("Opção inválida. Por favor, digite um número da lista.")
            input("Pressione Enter para tentar novamente...")

        utils.clear_screen() # Opcional: Para limpar antes de voltar ao menu
    print("Voltando ao menu principal...")

def main():
    db_access.inicializar_db() # Garante que o DB e tabelas existam e preenche produtos iniciais se necessário

    # Código para popular PREÇOS aleatórios inicialmente.
    # Função só funciona se em db_access estiver com o IMPORT RANDOM (ex: popular_precos_iniciais_aleatorios),
    # Pode chamá-la aqui depois dela verificar, por exemplo:
    # if db_access.verificar_se_precos_estao_vazios(): # Função hipotética em db_access
    #     print("Populando preços iniciais aleatórios...")
    #     db_access.popular_precos_iniciais_aleatorios()

    while True:
        escolha = exibir_menu_principal()
        if escolha == '1':
            gerenciar_estatisticas_produto()
        elif escolha == '2':
            gerenciar_listagem_todos_produtos()
        elif escolha == '3': 
            gerenciar_adicao_produto()
        elif escolha == '4':
            gerenciar_adicao_preco_manual() 
        elif escolha == '0':
            utils.clear_screen() # Limpa a tela uma última vez antes de sair
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
    
    
    