import re
from unicodedata import category
import pandas as pd
# import spacy
# from spacy.matcher import Matcher
import numpy as np

from data_processing import BANK, CREDITS, UpWORK, BILLS, SALES
from data_processing import submit_data, matcher_fun

from processor_bills import paid_per_class, payables_per_class
from processor_bankstatment import AMEX_list, BILL_list, CAPITAL_ONE_list, HEALTH_CARE_list, LOAN_list, PAYROLL_list, SERVICE_CHARGE_list, SUBSCRIPTION_list, USAA_list

# descriptions = [_ for _ in bank['Description']]


nlp = spacy.load("en_core_web_sm")

bank = BANK

# projects = ['Voice Summit 2022', 'Web3', 'G&A']
# account = ["Labor", "Loan", "Marketing", "Miscellaneous", "Online Services", "Software & Subscriptions"]
# category = ['Revenue', 'Receivable', 'COGS', 'NON-COGS', 'Payable']
# method = ["Cash", "Credit"]

# Loan
loan_df = matcher_fun(matcher_list = LOAN_list, data = bank, account="Loan")
loan_df['Vendor'] = ["Loan Builder" for i in range(loan_df.shape[0])] 
loan_df['Invoice Date'] = [ _ for _ in loan_df['Date']] 
loan_df['Due Date'] = [ _ for _ in loan_df['Date']]  
loan_df['Process Date'] = [ _ for _ in loan_df['Date']] 
loan_df['Status'] = ["paid" for i in range(loan_df.shape[0])] 

# Amex Payment
amex_df = matcher_fun(matcher_list = AMEX_list, data = bank, account="Credit Card Payment")
amex_df['Vendor'] = ["AMEX" for i in range(amex_df.shape[0])] 
amex_df['Invoice Date'] = [ _ for _ in amex_df['Date']] 
amex_df['Due Date'] = [ _ for _ in amex_df['Date']]  
amex_df['Process Date'] = [ _ for _ in amex_df['Date']] 
amex_df['Status'] = ["paid" for i in range(amex_df.shape[0])] 

# Bill.com 
pattern_df = matcher_fun(matcher_list = BILL_list, data = bank, account="Vendors from Bill.com")
pattern_df['Vendor'] = ["BILL.COM Vendors" for i in range(pattern_df.shape[0])] 
pattern_df['Invoice Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Due Date'] = [ _ for _ in pattern_df['Date']]  
pattern_df['Process Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Status'] = ["paid" for i in range(pattern_df.shape[0])] 

pattern_df = matcher_fun(matcher_list = CAPITAL_ONE_list, data = bank, account="Credit Card Payment")
pattern_df['Vendor'] = ["CAPITAL ONE" for i in range(pattern_df.shape[0])] 
pattern_df['Invoice Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Due Date'] = [ _ for _ in pattern_df['Date']]  
pattern_df['Process Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Status'] = ["paid" for i in range(pattern_df.shape[0])] 


pattern_df = matcher_fun(matcher_list = USAA_list, data = bank, account="Credit Card Payment")
pattern_df['Vendor'] = ["USAA" for i in range(pattern_df.shape[0])] 
pattern_df['Invoice Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Due Date'] = [ _ for _ in pattern_df['Date']]  
pattern_df['Process Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Status'] = ["paid" for i in range(pattern_df.shape[0])] 

pattern_df = matcher_fun(matcher_list = HEALTH_CARE_list, data = bank, account="Health Care")
pattern_df['Vendor'] = ["UNITED HEALTHCARE" for i in range(pattern_df.shape[0])] 
pattern_df['Invoice Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Due Date'] = [ _ for _ in pattern_df['Date']]  
pattern_df['Process Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Status'] = ["paid" for i in range(pattern_df.shape[0])] 

pattern_df = matcher_fun(matcher_list = PAYROLL_list, data = bank, account="Labor")
pattern_df['Vendor'] = ["Peter Erickson" for i in range(pattern_df.shape[0])] 
pattern_df['Invoice Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Due Date'] = [ _ for _ in pattern_df['Date']]  
pattern_df['Process Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Status'] = ["paid" for i in range(pattern_df.shape[0])] 

pattern_df = matcher_fun(matcher_list = SERVICE_CHARGE_list, data = bank, account="Service Charge")
pattern_df['Vendor'] = ["Truist" for i in range(pattern_df.shape[0]-2)]  + ["INTUIT" for i in range(2, pattern_df.shape[0])]
pattern_df['Invoice Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Due Date'] = [ _ for _ in pattern_df['Date']]  
pattern_df['Process Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Status'] = ["paid" for i in range(pattern_df.shape[0])] 

pattern_df = matcher_fun(matcher_list = SUBSCRIPTION_list, data = bank, account="Subscriptions")
pattern_df['Vendor'] = ["Subscription Fees" for i in range(pattern_df.shape[0])] 
pattern_df['Invoice Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Due Date'] = [ _ for _ in pattern_df['Date']]  
pattern_df['Process Date'] = [ _ for _ in pattern_df['Date']] 
pattern_df['Status'] = ["paid" for i in range(pattern_df.shape[0])] 










columns = ["Class", "Category", "Account", "Vendor", "Description", "Method", "Amount", "Invoice Date", "Due Date", "Status", "Process Date"]

# bill_payables = submit_data("")