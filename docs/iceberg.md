# Iceberg

## Papel do Iceberg no experimento

No projeto, o Iceberg representa uma das duas abordagens de tabela analitica avaliadas. O objetivo nao e cobrir todos os recursos do Iceberg, mas validar se ele atende aos cenarios ACID definidos pelo grupo sobre os dados de Statcast.

## Implementacao no repositorio

O experimento esta no notebook `notebooks/iceberg.ipynb`, com:

- configuracao do catalogo Spark `ice`;
- warehouse local em `data/iceberg_warehouse`;
- tabela `ice.baseball.statcast_arremessadores`.

A carga inicial e feita a partir de `data/raw/statcast_data.csv`, seguida pelas operacoes de mutacao.

## Cenarios executados no notebook (paridade com Delta)

### 1) UPDATE de `velocidade_media`

Correcao pontual da velocidade media para **Webb, Logan** (valor **89.2**), alinhada ao notebook `delta-lake.ipynb`.

### 2) DELETE de jogador (sancao)

Remocao da linha de **Rodón, Carlos** (predicado por `nome_jogador`), mesmo cenario de saneamento usado no Delta.

### 3) Auditoria via snapshots

Consulta a `snapshots` e `history` para evidenciar commits e linha do tempo de versoes.

## Evidencia de auditoria no projeto

Ao final do notebook, a equipe consulta o historico de snapshots para comprovar que cada operacao gera uma nova versao da tabela.

Esse trecho e central para a comparacao com Delta, pois mostra rastreabilidade das alteracoes no mesmo fluxo de estudo.

## O que observamos com Iceberg

No contexto deste trabalho:

- comandos SQL para mutacao funcionam de forma objetiva;
- snapshots facilitam validacao de historico;
- organizacao em catalogo + namespace ajuda a manter o experimento legivel.
