# Contextualizacao

## Visao geral do trabalho

Este projeto da disciplina de Engenharia de Dados compara, no mesmo cenario, como **Delta Lake** e **Apache Iceberg** se comportam sobre o **Apache Spark**.

O foco nao e explicar as tecnologias de forma enciclopedica, e sim documentar como elas foram aplicadas no experimento do grupo.

## Escopo do experimento

- dataset base: `data/raw/statcast_data.csv`;
- contexto analitico: estatisticas agregadas de arremessadores;
- engine de processamento: PySpark;
- tabelas avaliadas: uma implementacao em Delta e outra em Iceberg;
- operacoes avaliadas: `INSERT`, `UPDATE` e `DELETE`.

## Objetivo pratico

Demonstrar como manter um dataset analitico mutavel sem reprocessar o arquivo inteiro sempre que ocorrer uma correcao pontual.

No projeto, isso aparece em cenarios reais de manutencao:

- ajuste de estatistica de um jogador (update);
- remocao de linha por invalidez ou sancao (delete);
- inclusao de novo registro para validar append controlado (insert).

## Fluxo adotado no repositorio

1. Leitura do CSV bruto com schema definido em `src/ingestao.py`.
2. Padronizacao de colunas para o modelo de arremessadores.
3. Gravacao em tabela Delta ou Iceberg.
4. Execucao de cenarios ACID nos notebooks.
5. Verificacao de historico transacional (auditoria).

Em código, o núcleo comum é sempre `ler_e_limpar_dados(spark, caminho_csv)` antes de ramificar para `df.write.format("delta")` ou `CREATE TABLE ... USING iceberg` + `INSERT`, como na página [Exemplos de código](exemplos_codigo.md).

## Criterios de comparacao usados pela equipe

Durante o trabalho, a comparacao entre Delta e Iceberg considera:

- simplicidade da implementacao no notebook;
- clareza da API para operacoes de mutacao;
- rastreabilidade de alteracoes (historico/snapshots);
- impacto operacional no fluxo de estudo e reproducao.
