# Rastreador de Preços de Supermercado

Este é um projeto de um indexador de preços de supermercado desenvolvido em Python, utilizando SQLite para o armazenamento de dados. O objetivo é permitir o registro e a análise de preços de produtos em diferentes supermercados, auxiliando no acompanhamento da variação de custos.

## Funcionalidades Atuais

O sistema atualmente oferece as seguintes funcionalidades através de uma interface de console interativa:

1.  **Cadastro de Novos Produtos:**
    * Permite ao usuário adicionar novos produtos ao banco de dados, especificando o nome do produto (ex: "Arroz", "Leite") e sua unidade de medida (ex: "kg", "litro", "pacote").

2.  **Registro de Preços Detalhado:**
    * Possibilita o registro de preços para produtos já cadastrados.
    * Ao adicionar um preço, o usuário informa:
        * O produto (selecionado de uma lista numerada).
        * O supermercado onde o preço foi observado (selecionado de uma lista predefinida para garantir consistência).
        * O valor do preço.
        * A data da coleta do preço (com opção de usar a data atual automaticamente).

3.  **Listagem de Produtos:**
    * Exibe todos os produtos atualmente cadastrados no sistema.

4.  **Análise de Preços por Produto:**
    * Para um produto selecionado, o sistema calcula e exibe:
        * O preço mais baixo registrado.
        * O preço médio.
        * O preço mais alto registrado.
    * Essa análise considera os preços registrados nos últimos 30 dias.
    * Informa também o período (data do primeiro e último preço) coberto pela análise.
    * Permite consultas sequenciais de diferentes produtos sem retornar ao menu principal a cada consulta.

5.  **Interface de Usuário Amigável:**
    * Menu principal claro e navegação baseada em números.
    * Limpeza automática da tela do console para melhor visualização das informações.
    * Pausas estratégicas para que o usuário possa ler as informações antes de prosseguir.

## Estrutura do Projeto

O código está organizado de forma modular para facilitar a manutenção e o desenvolvimento:

* `main.py`: Ponto de entrada principal da aplicação, gerencia o fluxo do programa e a interface com o usuário.
* `db_access.py`: Contém todas as funções responsáveis pela interação com o banco de dados SQLite (operações CRUD, consultas).
* `utils.py`: Módulo para funções utilitárias, como a limpeza da tela do console.
* `config.py`: Armazena configurações globais, como o nome do arquivo do banco de dados e a lista predefinida de supermercados.
* `supermercado.db`: Arquivo do banco de dados SQLite onde os dados são armazenados (criado automaticamente na primeira execução).

## Tecnologias Utilizadas

* **Python 3:** Linguagem de programação principal.
* **SQLite3:** Sistema de gerenciamento de banco de dados leve, embutido na biblioteca padrão do Python, usado para persistência dos dados.
* Módulos Python padrão: `os`, `datetime`, `sqlite3`.

## Como Executar o Projeto

1.  **Pré-requisitos:**
    * Python 3.8 ou superior instalado e configurado no PATH do sistema.

2.  **Configuração Inicial:**
    * Certifique-se de que todos os arquivos (`main.py`, `db_access.py`, `utils.py`, `config.py`) estejam no mesmo diretório.
    * **Importante (Ao executar pela primeira vez ou após alterações na estrutura do banco):** Se o arquivo `supermercado.db` já existir de uma versão anterior com uma estrutura de tabelas diferente (por exemplo, antes da adição da coluna `SupermercadoNome` na tabela `Precos`), é recomendado **apagá-lo**. O programa recriará o arquivo `supermercado.db` automaticamente com o esquema mais recente na próxima execução.

3.  **Execução:**
    * Abra um terminal (Prompt de Comando, PowerShell, Terminal do Linux/macOS, ou o terminal integrado do seu editor de código) no diretório onde os arquivos do projeto estão localizados.
    * Execute o script principal com o comando:
        ```bash
        python main.py
        ```
    * Siga as instruções apresentadas no menu interativo do console.

## Próximas Funcionalidades Planejadas (Sugestões)

* Adicionar o conceito de "Marca" aos produtos para um rastreamento mais específico.
* Implementar uma funcionalidade para encontrar o "preço mais barato" de um produto, considerando todas as suas marcas e os diferentes supermercados.
* Permitir a edição e exclusão de produtos e registros de preços.
* Adicionar filtros às consultas de estatísticas (ex: por supermercado, por período de datas específico).
* (Avançado) Criação de uma interface gráfica (GUI) ou web para o sistema.

---
*Este README foi gerado com base no estado do projeto em 16 de maio de 2025.*
