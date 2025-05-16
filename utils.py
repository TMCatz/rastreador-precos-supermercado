import os

def clear_screen():
    """Limpa a tela do console, compatível com Windows, macOS e Linux."""
    # Para Windows
    if os.name == 'nt':
        _ = os.system('cls') # O '_' é para suprimir a saída do linter sobre valor de retorno não utilizado
    # Para macOS e Linux
    else:
        _ = os.system('clear')