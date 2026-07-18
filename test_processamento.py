import pytest
from processamento import ProcessadorMatriculas

@pytest.fixture
def processador():
    return ProcessadorMatriculas()

def test_matricula_valida_aprovada(processador):
    entrada = {
        "id": 1, "nome": " Maria ", "email": "MARIA@EMAIL.COM", 
        "cpf": "123.456.789-00", "curso": "Sistemas", "valor_mensalidade": 1000, 
        "desconto_percentual": 10, "documentos_entregues": ["RG", "CPF", "COMPROVANTE_ENDERECO"]
    }
    resultado = processador.processar_registro(entrada)
    assert resultado["status"] == "APROVADA"
    assert resultado["valor_final"] == 900.0
    assert resultado["email"] == "maria@email.com"

def test_matricula_valida_documentos_faltantes(processador):
    entrada = {
        "id": 2, "nome": "João", "email": "joao@email.com", 
        "cpf": "09876543211", "curso": "Sistemas", "valor_mensalidade": 1000, 
        "documentos_entregues": ["RG"]
    }
    resultado = processador.processar_registro(entrada)
    assert resultado["status"] == "PENDENTE"
    assert "CPF" in resultado["documentos_faltantes"]
    assert "COMPROVANTE_ENDERECO" in resultado["documentos_faltantes"]

def test_email_invalido(processador):
    entrada = {
        "id": 3, "nome": "Ana", "email": "ana.com", 
        "cpf": "11122233344", "curso": "Redes", "valor_mensalidade": 500,
        "documentos_entregues": ["RG", "CPF", "COMPROVANTE_ENDERECO"]
    }
    resultado = processador.processar_registro(entrada)
    assert resultado["status"] == "REJEITADA"
    assert "E-mail com formato inválido" in resultado["erros"]

def test_cpf_duplicado(processador):
    reg1 = {
        "id": 4, "nome": "Carlos", "email": "c1@teste.com", 
        "cpf": "11111111111", "curso": "TI", "valor_mensalidade": 100
    }
    reg2 = {
        "id": 5, "nome": "Carlos Clone", "email": "c2@teste.com", 
        "cpf": "11111111111", "curso": "TI", "valor_mensalidade": 100
    }
    processador.processar_registro(reg1)
    resultado2 = processador.processar_registro(reg2)
    
    assert resultado2["status"] == "REJEITADA"
    assert "CPF duplicado" in resultado2["erros"]

def test_desconto_invalido(processador):
    entrada = {
        "id": 6, "nome": "Pedro", "email": "p@p.com", 
        "cpf": "22222222222", "curso": "TI", "valor_mensalidade": 100,
        "desconto_percentual": 150
    }
    resultado = processador.processar_registro(entrada)
    assert resultado["status"] == "REJEITADA"
    assert "Desconto deve estar entre 0 e 100" in resultado["erros"]

def test_campo_obrigatorio_ausente(processador):
    entrada = {
        "id": 7, "email": "t@t.com", "cpf": "33333333333", 
        "curso": "TI", "valor_mensalidade": 100
    }
    resultado = processador.processar_registro(entrada)
    assert resultado["status"] == "REJEITADA"