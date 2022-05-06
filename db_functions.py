import pandas as pd 
import requests
import json
import streamlit as st
import datetime
headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}

def formatnum(value, to='num'):
    value = str(value)
    value = value.replace("$", "")
    value = value.replace(")", "")
    value = value.replace("(", "-")
    value = value.replace(",", "")
    value = float(value)
    if to == 'num':
        return value
    else:
        return '{:,.0f}'.format(value)

def submit_data(collection, docs, headers=headers):
    insert_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/insertMany"
    Payload = json.dumps({"collection": collection, "database": "Modev", "dataSource": "BiCluster", "documents": docs})
    response = requests.request("POST", insert_url, headers=headers, data=Payload)
    return response

def get_data(collection, headers=headers):
    findAll_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/find"
    Payload = json.dumps({"collection": collection, "database": "Modev","dataSource": "BiCluster", "filter": {}, "limit":5000})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    response_json = response.json()['documents']
    df_db = pd.read_json(json.dumps(response_json))
    return df_db

def update_data(collection, condition, doc, headers=headers):
    updateOne_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/updateOne"
    Payload = json.dumps({"collection": collection, "database": "Modev","dataSource": "BiCluster", "filter": condition, "update":{"$set": doc}})
    response = requests.request("POST", updateOne_url, headers=headers, data=Payload)
    return response


st.cache(allow_output_mutation=True)
def get_ledger():
    return get_data('ledger_2022')

Ledger_DB = get_ledger()