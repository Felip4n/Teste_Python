import sys
import json
from processamento import ProcessadorMatriculas

def main():
    if len(sys.argv) != 3:
        print("Uso correto: python -m app <arquivo_entrada.json> <arquivo_saida.json>")
        sys.exit(1)
        
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            dados_entrada = json.load(f)
            
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada '{arquivo_entrada}' nao encontrado.")
        sys.exit(1)
        
    except json.JSONDecodeError:
        print(f"Erro: Arquivo de entrada '{arquivo_entrada}' nao contem um JSON valido.")
        sys.exit(1)
        
    if not isinstance(dados_entrada, list):
        print("Erro: O JSON de entrada deve conter uma lista de registros.")
        
    processador = ProcessadorMatriculas()
    resultado_final = processador.processar_lote(dados_entrada)
    
    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(resultado_final, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Erro ao salvar arquivo de saida: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
            