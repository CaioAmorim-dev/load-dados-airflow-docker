# Desafio Tecnico - banvic


A pipeline desenvolvida no Airflow é responsável por extrair, carregar (EL) os dados do banco de dados fornecido para o Data Warehouse.

***O fluxo segue as seguintes etapas:***

***Extração*** – os dados são lidos diretamente do banco PostgreSQL fornecido no desafio e do arquivo CSV.

***Carga*** – os dados tratados são inseridos no Data Warehouse (dw-postgres), estruturados para consultas analíticas.

Essa automação garante que o processo de ingestão e atualização seja reprodutível, escalável e agendado pelo Airflow, permitindo análises consistentes a partir de um ambiente centralizado.

## Estrutura da pasta principal

```bash
banvic/
├── config/           # Configurações do Airflow
├── dags/             # DAG principal do desafio 
├── data/             # CSVs extraídos
├── dw-data/          # Persistência do Data Warehouse
├── input/            # CSV de transações fornecido
├── logs/             # Logs do Airflow
├── plugins/          # Plugins do Airflow 
├── postgres-data/    # Persistência do banco fonte
```

## Guia para rodar ***banvic_pipeline***

***1. Baixe o arquivo "transacoes.cvs" e "banvic.sql"no link drive a seguir:***\
https://drive.google.com/drive/folders/1mNR-rzSEBPp2_CLI4A0ew6NgGnNSGH76


coloque o arquivo banvic.sql em (banvic-source)

coloque o arquivo transacoes.csv em (banvic/input), criando a pasta input caso não exista.


***2. Verificar containers em execução antes de seguir:***\
execute em cada pasta:
```bash
docker ps
```


Todos os serviços acima devem estar ativos.

---

***2.2 Acessar interface do Airflow***

Abra o navegador em
```bash
 http://localhost:8080
```

A DAG desafio_banvic já estará disponível.

---

***2.3 Executar o pipeline***

***Manual***: clique em ***"Trigger DAG"*** para rodar imediatamente.

***Automático:*** o pipeline será disparado diariamente às 04:35, conforme agendamento.

Resultados e arquivos gerados
```bash
CSVs extraídos do SQL: /data/<data_exec>/sql/

CSV de transações: /data/<data_exec>/csv/
```

Tabelas carregadas no DW: 
```bash
 schema raw_sql (SQL) 
 shema raw_csv (CSV de transações)
 ```

 ##  visualizção dos dados

 Acesso ao Data Warehouse
 ```bash
Host:	 localhost 
Porta:	 5433
Banco:	 dw_database
Usuário: dw_user
Senha:   dw_pass
```

 Essas credenciais serão usadas para se conectar diretamente ao PostgreSQL via cliente (pgAdmin, DBeaver, etc.).  


## Requisitos técnicos atendidos

***Idempotência:*** múltiplas execuções não duplicam dados; arquivos CSV e tabelas no DW são sobrescritos se já existirem.

***Paralelismo:*** extração de SQL e CSV ocorre simultaneamente; carregamento no DW depende do sucesso das duas tarefas.

***Reprodutibilidade:*** qualquer pessoa pode executar o projeto em outro ambiente, apenas descompactando o .zip e seguindo os guias.

***Automaticidade:*** a pipiline é executada todos os dias as 4:35 da manhã desde que os dockers estejam rodando corretamente no horário

***Padrão de nomes nos arquivos CSV***
```bash
  ano-mês-dia/fonte\tabela.csv
  ```