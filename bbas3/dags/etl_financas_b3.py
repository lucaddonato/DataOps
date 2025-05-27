# Bibliotecas
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import yfinance as yf
import os
import matplotlib.pyplot as plt


DATA_PATH = '/opt/airflow/dags/data'
REPORT_PATH = '/opt/airflow/dags/reports'

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(REPORT_PATH, exist_ok=True)





# ETL
def extrair():
    df = yf.download('BBAS3.SA', start='2024-01-01', end=datetime.now().strftime('%Y-%m-%d'))
    df.to_csv(f"{DATA_PATH}/bbas3_raw.csv")



def transformar():
    df = pd.read_csv(f"{DATA_PATH}/bbas3_raw.csv", index_col=0)
    df = df.dropna()
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Média_Móvel_20'] = df['Close'].rolling(window=20).mean()
    df.to_csv(f"{DATA_PATH}/bbas3_tratado.csv")



def relatorio():
    df = pd.read_csv(f"{DATA_PATH}/bbas3_tratado.csv")
    plt.figure(figsize=(10, 6))
    plt.plot(df['Média_Móvel_20'], label='Média Móvel 20 dias', color='orange')
    plt.legend()
    plt.title('Fechamento BBAS3 com Média Móvel 20 dias')
    plt.savefig(f"{REPORT_PATH}/bbas3_report.png")



default_args = {
    'start_date': datetime(2024, 1, 1),
    'catchup': True,
}



with DAG("etl_financas_b3",
         schedule_interval='@daily',
         default_args=default_args,
         description='ETL para BBAS3 na B3',
         tags=['dataops', 'finance', 'b3']) as dag:
    

        t1 = PythonOperator(
            task_id='extrair',
            python_callable=extrair,
        )


        t2 = PythonOperator(
            task_id='transformar',
            python_callable=transformar,
        )


        t3 = PythonOperator(
            task_id='relatorio',
            python_callable=relatorio,
        )

        t1 >> t2 >> t3