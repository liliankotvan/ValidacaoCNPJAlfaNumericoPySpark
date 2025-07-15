# ValidacaoCNPJAlfaNumericoPySpark

Validador de CNPJ alfanumérico baseado nas regras oficiais da Receita Federal, compatível com PySpark e Databricks. Calcula os dígitos verificadores (DV1 e DV2) usando a lógica ASCII-48 e módulo 11, conforme o formato do novo CNPJ.

---

## 🚀 Funcionalidades

- ✅ Limpeza e formatação de CNPJs com letras e números
- 🔢 Cálculo de DV1 e DV2 conforme algoritmo oficial
- 📋 Diagnóstico detalhado do status (válido, DV1 inválido, etc.)
- 🔄 Gravação opcional de logs em tabela Delta (modo update via MERGE)
- 📦 Pronto para uso em notebooks, pipelines e jobs agendados no Databricks

---

## 🧰 Requisitos

- Python 3.8+
- PySpark 3.x
- Databricks (opcional para integração com Delta Tables)

---

## 📦 Instalação

# bash
pip install git+https://github.com/seu-usuario/validador_cnpj.git
# Ou instale o pacote .whl/.zip no seu cluster Databricks

## 📄 Como usar
1. Importar o módulo
  from validador_cnpj.core import executar_validacao
2. Executar a validação
   resultado = executar_validacao(
    spark=spark,
    tabela_origem="nome_da_tabela",
    coluna_cnpj="nome_da_coluna_cnpj",
    tabela_log="tabela_de_log"  # opcional
)
print(resultado)

## 🛡️ Regras de Validação

O CNPJ deve conter exatamente 14 caracteres alfanuméricos

Os dígitos verificadores (13º e 14º caracteres) são validados conforme cálculo:

  ASCII - 48

Pesos distribuídos de acordo com o módulo 11

Diagnósticos possíveis:

"Válido"

"DV1 inválido"

"DV2 inválido"

"Ambos inválidos"

"Tamanho incorreto"

## 📁 Estrutura do projeto

ValidacaoCNPJAlfaNumericoPySpark/

├── validador_cnpj/
│   └── core.py
│   └── __init__.py
├── setup.py
├── README.md

## 🤝 Contribuição
Contribuições são bem-vindas! Para sugestões ou correções, abra um pull request ou issue no repositório.

## 📄 Licença
Este projeto é distribuído sob a licença MIT.
