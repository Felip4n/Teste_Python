import re
from typing import Dict, List, Any

class ProcessadorMatriculas:
    def __init__(self):
        self.cpfs_vistos = set()
        self.emails_vistos = set()
        self.docs_obrigatorios = {'RG', 'CPF', 'COMPROVANTE_ENDERECO'}
        
    def normalizar_dados(self, registro: Dict[str, Any]) -> Dict[str, Any]:
        if "nome" in registro and isinstance(registro["nome"], str):
            registro["nome"] = registro["nome"].strip()
            
            
        if "email" in registro and isinstance(registro["email"], str):
            registro["email"] = registro["email"].lower()
            
        if "cpf" in registro and isinstance(registro["cpf"], str):
            registro["cpf"] = re.sub(r'\D', '', registro["cpf"])
            
        return registro
    
    def processar_registro(self, registro: Dict[str, Any]) -> Dict[str, Any]:
        erros = []
        docs_faltantes = []
        valor_final = 0.0
        
        registro = self.normalizar_dados(registro)
        
        campos_obrigatorios = ["id", "nome", "email", "cpf", "curso", "valor_mensalidade"]
        for campo in campos_obrigatorios:
            if campo not in registro or registro[campo] is None or str(registro[campo]).strip() == "":
                erros.append(f"Campo obrigatório ausente ou vazio: {campo}")

        if erros:
            return self._montar_retorno(registro, "REJEITADA", 0.0, docs_faltantes, erros)

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", registro["email"]):
            erros.append("E-mail com formato inválido")

        if len(registro["cpf"]) != 11:
            erros.append("CPF deve conter exatamente 11 dígitos numericos")

        if registro["cpf"] in self.cpfs_vistos:
            erros.append("CPF duplicado")
        else:
            self.cpfs_vistos.add(registro["cpf"])

        if registro["email"] in self.emails_vistos:
            erros.append("E-mail duplicado")
        else:
            self.emails_vistos.add(registro["email"])

        try:
            mensalidade = float(registro["valor_mensalidade"])
            if mensalidade <= 0:
                erros.append("Valor da mensalidade deve ser maior que zero")
        except ValueError:
            erros.append("Valor da mensalidade invalido")
            mensalidade = 0.0
            
        desconto = registro.get("desconto_percentual", 0)
        try:
            desconto = float(desconto)
            if not (0 <= desconto <= 100):
                erros.append("Desconto deve estar entre 0 e 100")
        except ValueError:
            erros.append("Valor do desconto invalido")
            desconto = 0.0

        if not erros:
            valor_final = mensalidade * (1 - (desconto / 100))
            valor_final = round(valor_final, 2)

        docs_entregues = set(registro.get("documentos_entregues", []))
        docs_faltantes = list(self.docs_obrigatorios - docs_entregues)

        if erros:
            status = "REJEITADA"
        elif docs_faltantes:
            status = "PENDENTE"
        else:
            status = "APROVADA"

        return self._montar_retorno(registro, status, valor_final, docs_faltantes, erros)
    
    def _montar_retorno(self, registro: Dict, status: str, valor_final: float, 
                        docs_faltantes: List[str], erros: List[str]) -> Dict:
        return {
            "id": registro.get("id"),
            "nome": registro.get("nome", ""),
            "email": registro.get("email", ""),
            "cpf": registro.get("cpf", ""),
            "status": status,
            "valor_final": valor_final if status != "REJEITADA" else None,
            "documentos_faltantes": docs_faltantes,
            "erros": erros
        }
    
    def processar_lote(self, lista_registros: List[Dict]) -> Dict:
        matriculas_processadas = []
        resumo = {"total": 0, "aprovadas": 0, "pendentes": 0, "rejeitadas": 0}
        
        for registro in lista_registros:
            resultado = self.processar_registro(registro)
            matriculas_processadas.append(resultado)
            
            resumo["total"] += 1
            if resultado["status"] == "APROVADA":
                resumo["aprovadas"] += 1
            elif resultado["status"] == "PENDENTE":
                resumo["pendentes"] += 1
            elif resultado["status"] == "REJEITADA":
                resumo["rejeitadas"] += 1
                
        return {
            "resumo": resumo,
            "matriculas": matriculas_processadas
        }
    