import pandas as pd
import requests
import datetime
import json
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import spacy

base_uri = 'https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta'
file_folder = 'E:/Users/abega/Documents/Hammerton Barca/MODEV/MODEV Finance/cash flow dashboard/downloaded_files/'

def convert_to_df(response):
    if response.ok:
        response_json = response.json()
        colomun = [_ for _ in response_json['documents'][0].keys()]
        df_data = {}
        for col in colomun:
            df_data[col] = []
        for doc in response_json['documents']:
            for col in colomun:
                df_data[col].append(doc[col])
        df = pd.DataFrame(df_data)
        return df
    else:
        return None

def df_to_dict(df):
    df.fillna(value = '0', inplace = True)
    rows = df.shape[0]
    cols = df.columns
    docs = [{} for i in range(rows)]
    for col in cols:
        values = [_ for _ in df[col]]
        for i in range(rows):
            doc = docs[i]
            if type(values[i]) != float:
                doc[col] = str(values[i])
            else:
                doc[col] = float(values[i])
    return docs


def submit_data(collection, doc):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}
    insert_url = f"{base_uri}/action/insertMany"
    Payload = json.dumps({"collection": collection, "database": "Modev", "dataSource": "BiCluster", "documents": doc})
    response = requests.request("POST", insert_url, headers=headers, data=Payload)
    return response
def get_data(collection):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}
    findAll_url = f"{base_uri}/action/find"
    Payload = json.dumps({"collection": collection, "database": "Modev","dataSource": "BiCluster", "filter": {}, "limit":5000})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    return response
    
def Update_data(filter, doc, collection):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}
    insert_url = f"{base_uri}/action/updateOne"
    Payload = json.dumps({"collection": collection, "database": "Modev","dataSource": "BiCluster", "filter": filter, "update": doc,  "upsert": True})
    response = requests.request("POST", insert_url, headers=headers, data=Payload)
    return response


AMEX = get_data('report_amex')
UPWORK = get_data('report_upwork')
BANK = get_data('report_bank_truist')
SALES = get_data('report_quickbooks')
BILLS = get_data('report_bill')

file_path_amex = file_folder + 'amex.csv'
file_path_bill_payments = file_folder + 'bill_payments.csv'
file_path_bills = file_folder + 'bills.csv'
file_path_bank = file_folder + 'truist_bank.csv'
file_path_upwork_FL = file_folder + 'upwork_FL.csv'
file_path_upwork_TR = file_folder + 'upwork_TR.csv'

file_paths = [file_path_amex, file_path_bill_payments, file_path_bills, file_path_bank, file_path_upwork_FL, file_path_upwork_TR]
file_columns = []
for path in file_paths:
    df = pd.read_csv(path)
    cols = [_ for _ in df.columns]
    file_columns.append(cols)
file_path_sales = file_folder + 'sales.xls'
df = pd.read_excel(file_path_sales, header=1)
cols = [_ for _ in df.columns]
file_columns.append(cols)