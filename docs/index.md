# Trabalho 1 — Engenharia de Dados (SATC)

Documentação do projeto de pesquisa que compara **Apache Delta Lake** e **Apache Iceberg** sobre **PySpark**, usando o dataset **Statcast** agregado (`data/raw/statcast_data.csv`) e os notebooks em `notebooks/`.

## Conteúdo deste site

| Página | Tema |
|--------|------|
| [Contextualização](contextualizacao.md) | Objetivo do trabalho, escopo do experimento e critérios de comparação. |
| [Spark](spark.md) | Papel do Apache Spark no fluxo e integração com `src/ingestao.py`. |
| [Iceberg](iceberg.md) | Catálogo, warehouse local e cenários no `iceberg.ipynb`. |
| [Delta Lake](delta.md) | Escrita em `data/delta_statcast` e operações via API no `delta-lake.ipynb`. |

Para editar localmente: na raiz do repositório, com o ambiente ativado, use `task docs_serve` ou `mkdocs serve`.
