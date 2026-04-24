# Iceberg

## Papel do Iceberg no experimento

No projeto, o Iceberg representa uma das duas abordagens de tabela analitica avaliadas. O objetivo nao e cobrir todos os recursos do Iceberg, mas validar se ele atende aos cenarios ACID definidos pelo grupo sobre os dados de Statcast.

## Implementacao no repositorio

O experimento esta no notebook `notebooks/iceberg.ipynb`, com:

- configuracao do catalogo Spark `ice`;
- warehouse local em `data/iceberg_warehouse`;
- tabela `ice.baseball.statcast_arremessadores`.

A carga inicial e feita a partir de `data/raw/statcast_data.csv`, seguida pelas operacoes de mutacao.

## Cenarios executados no notebook

### 1) INSERT de registro de teste

Insercao de um arremessador sintetico para validar append e leitura imediata.

### 2) UPDATE de estatistica

Ajuste pontual em metrica de arremessador, simulando correcao de dado oficial.

### 3) DELETE de registro

Remocao de linha para reproduzir cenario de expurgo/saneamento.

## Evidencia de auditoria no projeto

Ao final do notebook, a equipe consulta o historico de snapshots para comprovar que cada operacao gera uma nova versao da tabela.

Esse trecho e central para a comparacao com Delta, pois mostra rastreabilidade das alteracoes no mesmo fluxo de estudo.

## O que observamos com Iceberg

No contexto deste trabalho:

- comandos SQL para mutacao funcionam de forma objetiva;
- snapshots facilitam validacao de historico;
- organizacao em catalogo + namespace ajuda a manter o experimento legivel.
