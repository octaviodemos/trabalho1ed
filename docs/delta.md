# Delta

## Papel do Delta no experimento

No projeto, Delta Lake e a implementacao usada para comparar mutabilidade e auditoria contra Iceberg, sempre com o mesmo dataset e o mesmo motor Spark.

## Implementacao no repositorio

O fluxo esta em `notebooks/delta-lake.ipynb` e usa:

- leitura do arquivo `data/raw/statcast_data.csv`;
- schema e limpeza vindos de `src/ingestao.py`;
- escrita da tabela em `data/delta_statcast`.

O notebook tambem utiliza a API `DeltaTable` para executar alteracoes pontuais sem recarga completa da base.

## Cenarios executados no notebook

### 1) Carga inicial da tabela

Persistencia do dataset de arremessadores no formato Delta para criar a linha de base do experimento.

### 2) UPDATE de `velocidade_media`

Simulacao de correcao de telemetria para um jogador especifico, validando alteracao parcial de linha.

### 3) DELETE de jogador

Remocao de registro para reproduzir cenario de saneamento/sancao, mantendo historico da operacao.

## Evidencia de historico transacional

O notebook consulta `history()` da tabela Delta ao final. Isso registra cada operacao executada no experimento e serve como evidencia de auditoria para o relatorio.

## O que observamos com Delta

Dentro do escopo deste trabalho:

- API `DeltaTable` deixa update/delete diretos no PySpark;
- log transacional facilita rastreabilidade das mudancas;
- o fluxo ficou simples de reproduzir localmente em notebook.
