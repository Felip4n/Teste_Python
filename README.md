# Processador de Matrículas 

## Descrição
Aplicação CLI em Python para leitura, normalização, validação e processamento de um lote de solicitações de matrícula em formato JSON.

## Requisitos de Ambiente
- Python 3.9+
- `pytest` (apenas para execução dos testes automatizados)

## Como preparar o ambiente
1. Clone o repositório.
2. (Recomendado) Crie um ambiente virtual: `python -m venv venv` e ative-o.
3. Instale as dependências de teste: `pip install pytest`.

## Como executar os testes
Na raiz do projeto, execute o comando abaixo para rodar a suíte de testes automatizados:
python -m pytest test_processamento.py -v

## Como executar a aplicação
A aplicação recebe o arquivo de entrada e o de saída como parâmetros no terminal. Na raiz do projeto, utilize o comando:
python -m app entrada.json saida.json

## Uso de Inteligência Artificial

-Google Gemini

- **Onde usei:** 
  - Na montagem da estrutura base do projeto e organização dos arquivos.
  - Na criação das expressões regulares (regex) para limpar o CPF e validar o e-mail.
  - Para montar a base (boilerplate) dos testes no pytest.
  - Na geração de dados fictícios para rodar os testes.
- **Exemplos de prompts:** *"Crie uma regex simples para validar e-mail em Python"*, *"Gere alguns objetos JSON fictícios de matrículas para eu testar a aplicação"* e *"Quais casos de erro comuns eu devo prever ao calcular o desconto da mensalidade?"*.
- **O que foi rejeitado:** A IA sugeriu usar a biblioteca `pandas` para manipular os dados do JSON. Preferi ignorar e usar apenas Python puro (`dict`, `set`, `list`), porque teste pede uma solução focada em clareza e sem complexidade desnecessária.
- **Validação:** Não houve "copia e cola" cego. Revisei o código linha por linha, apliquei as tipagens (Type Hints) manualmente e rodei os testes isolados para garantir que os status (APROVADA, PENDENTE, REJEITADA) funcionassem exatamente como as regras de negócio pediam.