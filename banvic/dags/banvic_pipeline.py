from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
import logging
import os
import shutil
import pandas as pd
 

log = logging.getLogger("airflow.task")

pasta_base = "/opt/airflow/data"
arquivo_transacoes = "/opt/airflow/input/transacoes.csv"
tabelas_originais = [
    "agencias",
    "clientes",
    "colaboradores",
    "colaborador_agencia",
    "contas",
    "propostas_credito"
]

def pegar_tabelas_sql(**kwargs):
    data_exec = kwargs["ds"]
    pasta_saida_sql = os.path.join(pasta_base, data_exec, "sql")
    os.makedirs(pasta_saida_sql, exist_ok=True)

    banco_origem = PostgresHook(postgres_conn_id="postgres_source")
    for tab in tabelas_originais:
        df_tab = banco_origem.get_pandas_df(f"SELECT * FROM {tab};")
        caminho_csv = os.path.join(pasta_saida_sql, f"{tab}.csv")
        df_tab.to_csv(caminho_csv, index=False)
        log.info(f"Tabela {tab} exportada para {caminho_csv} ok!")

def copiar_csv_transacoes(**kwargs):
    data_exec = kwargs["ds"]
    pasta_saida_csv = os.path.join(pasta_base, data_exec, "csv")
    os.makedirs(pasta_saida_csv, exist_ok=True)

    destino = os.path.join(pasta_saida_csv, "transacoes.csv")
    shutil.copy(arquivo_transacoes, destino)
    log.info(f"Arquivo de transacoes copiado pra {destino}")


def subir_para_dw(**kwargs):

    """Carregar tudo no Data Warehouse."""
    data_exec = kwargs["ds"]
    engine = create_engine("postgresql+psycopg2://dw_user:dw_pass@dw-postgres:5432/dw_database")


    # Criação de schemas caso não existam
    with engine.connect() as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw_sql;")
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw_csv;")



    # Carregamento de CSVs das tabelas SQL
    pasta_sql = os.path.join(pasta_base, data_exec, "sql")
    for tab in tabelas_originais:
        arquivo_tab = os.path.join(pasta_sql, f"{tab}.csv")
        df_tab = pd.read_csv(arquivo_tab)

        # Sobrescreve se já existir
        df_tab.to_sql(
            name=tab,
            con=engine,
            schema="raw_sql",
            if_exists="replace",
            index=False
        )
        log.info(f"{tab} carregada no schema raw_sql.")

    # Carrega CSV de transações
    caminho_trans = os.path.join(pasta_base, data_exec, "csv", "transacoes.csv")
    df_trans = pd.read_csv(caminho_trans, parse_dates=["data_transacao"])
    df_trans.to_sql(
        name="transacoes",
        con=engine,
        schema="raw_csv",
        if_exists="replace",
        index=False
    )
    log.info("Transacoes carregadas no schema raw_csv.")

# Definição da dag
with DAG(
    "desafio_banvic",
    start_date=datetime(2025, 9, 1),
    schedule_interval="35 4 * * *", 
    catchup=False,
    default_args={"owner": "caio_cesar"},
    description="Pipeline para desafio Banvic --- SQL + CSV -> DW"
) as dag:

    task_sql = PythonOperator(
        task_id="extrair_sql",
        python_callable=pegar_tabelas_sql,
    )

    task_csv = PythonOperator(
        task_id="extrair_csv",
        python_callable=copiar_csv_transacoes,
    )

    task_dw = PythonOperator(
        task_id="carregar_dw",
        python_callable=subir_para_dw,
    )
    # Apenas carrega apos concluir as tasks de extração
    [task_sql, task_csv] >> task_dw

dag = dag