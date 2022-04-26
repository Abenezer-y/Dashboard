import re
from unicodedata import category
import pandas as pd
import spacy
from spacy.matcher import Matcher
import numpy as np

from data_processing import BANK, CREDITS, UpWORK, BILLS, SALES
from data_processing import submit_data

from processor_bills import paid_per_class, payables_per_class



bank = BANK

descriptions = [_ for _ in bank['Description']]


nlp = spacy.load("en_core_web_sm")



projects = ['Voice Summit 2022', 'Web3', 'G&A']
account = ["Labor", "Loan", "Marketing", "Miscellaneous", "Online Services", "Software & Subscriptions"]
category = ['Revenue', 'Receivable', 'COGS', 'NON-COGS', 'Payable']
method = ["Cash", "Credit"]




def matcher_fun(matcher_list, data=bank, account="Miscellaneous", project="G&A", category="Expense", method="Cash"):
    matcher = Matcher(nlp.vocab, validate=True)
    text_list = [_ for _ in data['Description']]
    for pattern in matcher_list:
        matcher.add(pattern[0], pattern[1])

    matched_transactions = []
    indices = []
    for text in text_list:
        doc = nlp(text)
        for match_id, start, end in matcher(doc):
            matched_transactions.append(doc.text)

    for desc in matched_transactions:
        index = data.loc[lambda df: df['Description'].str.match(desc)].index
        for i in index:
            if i in indices:
                pass
            else:
                indices.append(i)
    df = data.loc[lambda df: data.iloc[indices]] 
    df["Account"] = [account for i in range(df.shape[0])]
    df["Class"] = [project for i in range(df.shape[0])]
    df["Category"] = [category for i in range(df.shape[0])]
    df["Method"] = [method for i in range(df.shape[0])]
    return df




bill_payables = submit_data("")