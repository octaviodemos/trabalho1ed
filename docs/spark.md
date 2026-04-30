# Spark

## Papel do Spark no projeto

No nosso trabalho, o Spark e a camada comum de execucao usada tanto no experimento com Delta quanto no experimento com Iceberg.

Isso garante comparacao justa: mudamos o formato de tabela, mas mantemos o mesmo motor de processamento e o mesmo dataset.

## Como o Spark entra no fluxo

No repositorio, o Spark e usado para:

1. Ler `data/raw/statcast_data.csv` com schema controlado.
2. Aplicar cast e padronizacao de colunas via `src/ingestao.py`.
3. Escrever os dados na tabela alvo (Delta ou Iceberg).
4. Executar mutacoes SQL/API (`INSERT`, `UPDATE`, `DELETE`) para validar ACID.

## Integracao com o codigo do projeto

O arquivo `src/ingestao.py` define:

- schema esperado do Statcast;
- renomeacao de colunas de origem para o modelo do projeto;
- funcao `ler_e_limpar_dados(...)`, reutilizada nos notebooks de Delta e Iceberg.

Essa etapa padroniza os dados antes da persistencia e evita inconsistencias por inferencia automatica de tipos.

Exemplo de uso após o `SparkSession` já existir (o builder completo está em [Exemplos de código](exemplos_codigo.md) para Delta e Iceberg):

```python
import sys
from pathlib import Path

raiz = Path(".").resolve()
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))

from src.ingestao import obter_esquema_statcast, ler_e_limpar_dados

csv_path = str(raiz / "data" / "raw" / "statcast_data.csv")
schema = obter_esquema_statcast()
df_statcast = ler_e_limpar_dados(spark, csv_path)
assert len(df_statcast.columns) == len(schema.fields)
```

## Notebooks onde o Spark e executado

- `notebooks/delta-lake.ipynb`
- `notebooks/iceberg.ipynb`

Ambos inicializam `SparkSession` com configuracoes especificas do formato de tabela avaliado, mas preservam a logica base de processamento.

## Decisoes praticas da equipe

Para este projeto academico, o Spark foi mantido em um escopo objetivo:

- processamento em DataFrame e SQL;
- foco em reproducao local (WSL + `.venv`);
- prioridade para cenarios de manutencao de dados, nao para tuning avancado.
