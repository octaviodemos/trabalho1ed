# Trabalho de Pesquisa: Apache Spark com Delta Lake e Apache Iceberg

| Campo | Informação |
|--------|--------------|
| **Instituição** | SATC — Santa Catarina |
| **Disciplina** | Engenharia de Dados — 5ª Fase de Engenharia de Software |
| **Professor** | Jorge Luiz da Silva |
| **Repositório** | [github.com/octaviodemos/trabalho1ed](https://github.com/octaviodemos/trabalho1ed) |

---

### Documentação pública (MkDocs)

**Site gerado:** **[https://octaviodemos.github.io/trabalho1ed/](https://octaviodemos.github.io/trabalho1ed/)**

> **Situação atual:** o deploy depende de **`task docs_deploy`** (ou `mkdocs gh-deploy`) com permissão no repositório e do **GitHub Pages** ativado na branch configurada. Se o link retornar **404**, o site ainda não foi publicado ou o Pages não está apontando para a branch correta.

---

## Equipe

| Nome | Papel |
|------|--------|
| **Octávio** | Líder técnico e Delta Lake |
| **Ana Laura** | Apache Iceberg e MkDocs |
| **Gabriel Ribeiro** | Dataset e QA |

---

## 1. Descrição

Este trabalho acadêmico tem como **objetivo principal** implementar e comparar duas tecnologias de *table formats* sobre **Apache Spark**, utilizando **PySpark**:

- **Delta Lake** — transações ACID, versionamento e evolução de esquema em camadas de dados no data lake.
- **Apache Iceberg** — tabelas abertas com isolamento de leitura, particionamento oculto e operações de manutenção planejadas.

A comparação é feita em cenário controlado, com o mesmo conjunto de dados e operações semelhantes, para evidenciar diferenças de API, desempenho percebido e características operacionais relevantes para **Engenharia de Dados**.

---

## 2. Pré-requisitos

Antes de clonar o repositório e instalar dependências, certifique-se de ter:

| Ferramenta | Detalhes |
|------------|----------|
| **WSL2** | Recomendado no Windows para ambiente Linux consistente com o laboratório e com Spark. |
| **Python 3.11.9** | Gerenciado com **pyenv** (`pyenv install 3.11.9` se ainda não estiver instalado). |
| **Java** | **OpenJDK 17** (Spark/PySpark costumam exigir JDK compatível; verifique com `java -version`). |
| **UV** | Gerenciador de pacotes e ambientes ([documentação oficial](https://docs.astral.sh/uv/)). |

> **Dica:** O arquivo `.python-version` na raiz do repositório já fixa a versão **3.11.9** para o pyenv quando você estiver dentro da pasta do projeto.

---

## 3. Instalação e setup

Siga a ordem abaixo na raiz do projeto (após o clone).

### 3.1. Clonar o repositório

```bash
git clone https://github.com/octaviodemos/trabalho1ed
cd trabalho1ed
```

### 3.2. Definir a versão local do Python (pyenv)

```bash
pyenv local 3.11.9
```

Confirme com:

```bash
python --version
```

A saída esperada contém **Python 3.11.9**.

### 3.3. Instalar dependências com UV

O arquivo `pyproject.toml` declara, entre outras, as versões **pyspark==3.5.3** e **delta-spark==3.2.0**. Para sincronizar o ambiente virtual e o lockfile:

```bash
uv sync
```

### 3.4. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

No Windows (PowerShell), o equivalente típico é `.venv\Scripts\Activate.ps1`.

---

## 4. Estrutura do repositório

Organização alinhada a **projetos Python** com documentação e artefatos de dados separados do código principal.

| Pasta / arquivo | Conteúdo |
|-----------------|----------|
| **`/notebooks`** | Notebooks Jupyter com experimentos PySpark (Delta Lake, Iceberg e análises comparativas). |
| **`/data`** | Dados de entrada e saída. **Entrada bruta:** `data/raw/statcast_data.csv` (Statcast). **Saídas dos notebooks:** tabela Delta em **`data/delta_statcast/`**; warehouse Iceberg em **`data/iceberg_warehouse/`**; `data/warehouse/` é o diretório padrão do Spark para o catálogo local do Delta, quando usado. |
| **`/docs`** | Fontes em Markdown consumidas pelo **MkDocs** (páginas do trabalho, metodologia, resultados). |
| **`/assets`** | Recursos estáticos (imagens, diagramas, arquivos auxiliares) referenciados pela documentação ou pelos notebooks. |
| **`mkdocs.yml`** | Configuração do site de documentação. |
| **`pyproject.toml` / `uv.lock`** | Metadados do projeto e lock de dependências gerenciado pelo **UV**. |

---

## 5. Como usar (notebooks)

1. Abra a pasta do projeto no **Visual Studio Code** ou no **Cursor**.
2. Instale a extensão **Jupyter** (se ainda não estiver instalada).
3. Abra um arquivo em **`/notebooks`** (por exemplo, `delta-lake.ipynb`).
4. **Selecione o kernel** associado ao interpretador do ambiente virtual **`.venv`** (Python 3.11.9 do projeto).
5. Execute as células **de cima para baixo** na primeira execução, para garantir que caminhos e dados sejam criados na ordem correta.

> **Importante:** Mantenha o ambiente ativado (`source .venv/bin/activate`) ou configure o VS Code/Cursor para usar diretamente o Python em **`.venv/bin/python`**.

---

## 6. ⚡ Atalhos de Automação (Taskipy)

O projeto utiliza o **[Taskipy](https://github.com/taskipy/taskipy)** para centralizar comandos frequentes no `pyproject.toml`, reduzindo erros de digitação e padronizando o fluxo de trabalho da equipe. Com o ambiente virtual ativado e as dependências instaladas (`uv sync`), execute os atalhos na **raiz do repositório** com o prefixo `task`.

| Comando | Descrição |
|---------|-----------|
| **`task server`** | Abre o ambiente do **Jupyter Lab** para rodar os notebooks. |
| **`task docs_serve`** | Inicia o servidor local do **MkDocs** para pré-visualizar a documentação. |
| **`task docs_deploy`** | Realiza o **deploy** da documentação para o **GitHub Pages** (`mkdocs gh-deploy`). |
| **`task generate_data`** | Executa o script de geração de dados da **loja fictícia** (`python data/data_generator.py`). |
| **`task clean`** | Remove artefatos gerados: `data/warehouse`, `data/iceberg_warehouse`, `data/delta_statcast` e `data/tabela_vendas_delta` (cenários antigos de exemplo), além de material legado. |

> **Atenção:** O comando `task clean` apaga diretórios de dados gerados localmente. Use apenas quando quiser **reiniciar** o cenário a partir de um estado limpo.

---

## 7. Documentação (MkDocs)

### 7.1. Servir localmente

Com o ambiente ativado e dependências instaladas (`uv sync`):

```bash
mkdocs serve
```

Acesse o endereço exibido no terminal (em geral **http://127.0.0.1:8000**) para navegar pela documentação durante o desenvolvimento.

### 7.2. Documentação pública (GitHub Pages)

Publicação (normalmente pela **`gh-pages`**): execute **`task docs_deploy`** na raiz, com branch **`main`** atualizada e remoto configurado. URL esperada:

**[https://octaviodemos.github.io/trabalho1ed/](https://octaviodemos.github.io/trabalho1ed/)**

O mesmo link aparece em destaque no início deste README. Se a página não carregar, confira se o **GitHub Pages** está ativo em *Settings → Pages* e se o deploy concluiu sem erro.

> Se o repositório ou a URL do GitHub Pages mudar, atualize o link no README e no `mkdocs.yml` conforme a nova publicação.

---

## 8. Dataset e cenários nos notebooks

**Experimento principal (paridade Delta ↔ Iceberg):** estatísticas agregadas de arremessadores **MLB Statcast** em `data/raw/statcast_data.csv`, com `INSERT`/`UPDATE`/`DELETE` ilustrados nos notebooks sobre as colunas padronizadas em `src/ingestao.py` (incluindo correção de **`velocidade_media`** e remoção do registro **Rodón, Carlos**).

**Cenário complementar (loja fictícia):** dados sintéticos de vendas podem ser gerados via **`task generate_data`** para exercícios adicionais de QA, quando aplicável.

As operações sobre o Statcast permitem comparar como **Delta Lake** e **Iceberg** tratam **mutabilidade**, **histórico** e **consistência** em tabelas gerenciadas pelo Spark.

---

## 9. Referências

- **Canal DataWay BR (YouTube):** pesquisa sobre conceitos de Spark, Delta Lake e Iceberg.
- **Repositórios de exemplo (GitHub):** projetos de referência do professor — [github.com/jlsilva01/spark-delta](https://github.com/jlsilva01/spark-delta) e [github.com/jlsilva01/spark-iceberg](https://github.com/jlsilva01/spark-iceberg).
- **Material de apoio:** documento em PDF *Python para Engenharia de Dados — material de apoio.pdf*, fornecido em aula.

---

## Licença e uso acadêmico

Este repositório destina-se ao **cumprimento das exigências da disciplina** sob orientação do professor **Jorge Luiz da Silva**. Reutilize o conteúdo apenas respeitando as normas da SATC e da disciplina.
