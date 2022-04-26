######
import streamlit as st
import pandas as pd 
import datetime
import requests
import json
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
######
# from db_functions import API_CONNECTION, convert_to_df, week_range, payload_constructor, df_to_dict

# df.rename(columns = {'old_col1':'new_col1', 'old_col2':'new_col2'}, inplace = True)

report_tables = ['report_bank_truist', 'report_bill', 'report_quickbooks', 'report_bill', 'report_quickbooks']
plan_tables = ['plan_budget']
class_tables = ['class_w3', 'class_Voice2021', 'class_Voice2022', 'class_VoiceNA', 'class_w3']
accounts = ['acc_loan', 'acc_payables', 'acc_payroll', 'acc_receivables', 'acc_sponsership', 'accounts']

key = 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'
base_uri = 'https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta' 
file_folder = 'E:/Users/abega/Documents/Hammerton Barca/MODEV/MODEV Finance/cash flow dashboard/downloaded_files/'
export = 'E:/Users/abega/Documents/Hammerton Barca/MODEV/MODEV Finance/cash flow dashboard/export.csv'

# Get Data from API
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

def get_data(collection):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}
    findAll_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/find"
    Payload = json.dumps({"collection": collection, "database": "Modev","dataSource": "BiCluster", "filter": {}, "limit": 50000})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    return convert_to_df(response)

def submit_data(collection, doc):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}
    insert_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/insertMany"
    Payload = json.dumps({"collection": collection, "database": "Modev", "dataSource": "BiCluster", "documents": doc})
    response = requests.request("POST", insert_url, headers=headers, data=Payload)
    return response




def get_bills(df):
    initial_date = datetime.datetime(2021, 11, 30, 0, 0 , 0)
    bills = df[df['Created Date']>initial_date]
    return bills

#####################################
### Functions: Utility functions ####
def cols(df):
    return df.columns[1:]
def format(num):
    return "{:,.2f}".format(num)   
def week_range(week=1):
    WEEK  = (datetime.datetime.today().isocalendar()[1] - week)
    # as it starts with 0 and you want week to start from sunday
    startdate = time.asctime(time.strptime('2022 %d 0' % WEEK, '%Y %W %w')) 
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y') 
    dates = [startdate] 
    for i in range(1, 7): 
        day = startdate + datetime.timedelta(days=i)
        # dates.append(day.strftime('%Y-%m-%d'))
        dates.append(day)
    return dates[0], dates[len(dates)-1]
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
def get_data(collection):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}
    findAll_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/find"
    Payload = json.dumps({"collection": collection, "database": "Modev","dataSource": "BiCluster", "filter": {}})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    return convert_to_df(response)
def date_formatter(date_var):
    dt_start = date_var.strftime("%m/%d/%Y")
    dt_str = datetime.strptime(dt_start, "%m/%d/%Y")
    return dt_str

def format_num(convert_to, value):
    value = (str(value)).replace(",", "")
    if convert_to == "num":
        return float(value)
    elif convert_to == "str":
        split_value = value.split('.')
        val = float(value)
        if len(split_value) == 1:
            value = '{:,.0f}'.format(val)
            return value
        elif len(split_value) == 2:
            if (split_value[1] == '0') | (split_value[1] == '00'):
                value = '{:,.0f}'.format(val)
                return value
            else:
                return '{:,.0f}'.format(round(val, 2)) 
#####################################
#####################################

#####################################
##### Functions: Grid functions #####
j_code = JsCode("""
            function() {
                    return { color: 'red'}
               };
            """)

def Grid(df, key, h=690, p =True, jscode=None):

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=p, paginationPageSize=20, paginationAutoPageSize=True)
    gd.configure_default_column(groupable=True, editable=True)
    gd.configure_selection('single')
    grid_option =gd.build()

    if type(jscode) == dict:
        gd.configure_columns("YTD Actual", cellStyle=jscode)

        
    grid = AgGrid(df,  key=key,
                    gridOptions=grid_option,
                    allow_unsafe_jscode=True,
                    update_mode=GridUpdateMode.FILTERING_CHANGED,
                    fit_columns_on_grid_load=True, 
                    reload_data=True,
                    data_return_mode='filtered' ,
                    theme="blue", 
                    height=h)
    return grid
#####################################
#####################################

#####################################
##### Functions: Data functions #####
# Raw Imports
@st.cache(allow_output_mutation=True)
def get_bank():
    return get_data('report_bank_truist')
@st.cache(allow_output_mutation=True)
def get_bills():
    df = get_data('report_bill')
    df['Created Date'] = pd.to_datetime(df['Created Date'])
    initial_date = datetime.datetime(2021, 11, 30, 0, 0 , 0)
    bills = df[df['Created Date']>initial_date]
    return bills
@st.cache(allow_output_mutation=True)
def get_upWork():
    return get_data('report_quickbooks')
@st.cache(allow_output_mutation=True)
def get_credit():
    return get_data('report_amex')
@st.cache(allow_output_mutation=True)
def get_sales():
    return get_data('report_quickbooks')
# Budget
@st.cache(allow_output_mutation=True)
def get_budget():
    return get_data('plan_budget')
# Budget
@st.cache(allow_output_mutation=True)
def get_budget_GnA():
    return get_data('budget_GnA')
# Budget
@st.cache(allow_output_mutation=True)
def get_budget_Voice22():
    return get_data('budget_Voice22')
# Budget
@st.cache(allow_output_mutation=True)
def get_budget_W3():
    return get_data('budget_W3')
# Projects
@st.cache(allow_output_mutation=True)
def get_w3():
    return get_data('class_w3')
@st.cache(allow_output_mutation=True)
def get_voice21():
    return get_data('class_Voice2021')
@st.cache(allow_output_mutation=True)
def get_voice22():
    return get_data('class_Voice2022')
@st.cache(allow_output_mutation=True)
def get_voiceNA():
    return get_data('class_VoiceNA')
@st.cache(allow_output_mutation=True)
def get_general():
    return get_data('class_general')
# Accounts
@st.cache(allow_output_mutation=True)
def get_loan():
    return get_data('acc_loan')
@st.cache(allow_output_mutation=True)
def get_payables():
    return get_data('acc_payables')
@st.cache(allow_output_mutation=True)
def get_payroll():
    return get_data('acc_payroll')
@st.cache(allow_output_mutation=True)
def get_receivables():
    return get_data('acc_receivables')
@st.cache(allow_output_mutation=True)
def get_sponsorship():
    return get_data('acc_sponsership')
@st.cache(allow_output_mutation=True)
def get_accounts():
    return get_data('accounts')
#####################################
#####################################

#####################################
########### Data Constants ##########
BILLS = get_bills()
UpWORK = get_upWork()
CREDITS = get_credit()
BANK = get_bank()
SALES = get_sales()

BUDGET = get_budget()
BG_W3 = get_budget_W3()
BG_VOICE22 = get_budget_Voice22()
BG_GnA = get_budget_GnA()

# ACCOUNTS = get_accounts()
LOAN = get_loan()
# RECEIVABLES = get_receivables()
PAYABLES = get_payables()
SPONSORSHIP = get_sponsorship()
# PAYROLL = get_payroll()

GENERAL = get_general()
VOICE21 = get_voice21()
VOICE22 = get_voice22()
VOICE_NA = get_voiceNA()
W3 = get_w3()
#####################################
#####################################

#####################################
#### Functions: Data Processing #####
def cashflow(date_1=None, date_2 = None):
    BANK['Date'] = pd.to_datetime(BANK['Date'])
    SALES['Date'] = pd.to_datetime(SALES['Date'])
    if (date_1  is None and date_2  is None):
        bank = BANK
        balance = bank['Amount'].sum()
    else:
        bank = BANK[BANK['Date']>=date_1]
        bank = bank[bank['Date']<=date_2]
        balance = BANK[BANK['Date']<=date_2]['Amount'].sum()

    ob =BANK[BANK['Description']=='Opening Balance']['Amount'].values[0]
    overdue = SALES[SALES['Status']=='overdue']['Total'].sum()
    open_invoice = SALES[SALES['Status']=='open']['Total'].sum()
    excpected_inflow = overdue + open_invoice
    income = bank[bank['Amount']>0.0]['Amount'].sum()
    expense = bank[bank['Amount']<0.0]['Amount'].sum()
    
    data_dict = {}
    data_dict['Description'] = ["Opening Balance", "Cash In", "Cash Out", "Open Invoice", "Overdue Invoices", "Bank Balance", "Estimated Revenue", "Estimated Payments", "Estimated Bank Balance"]
    opn_string = f"For the period Begining {date_1.strftime('%B')} {date_1.strftime('%d')}, {date_1.strftime('%Y')}"
    period_string = f"For the period Begining {date_1.strftime('%B')} {date_1.strftime('%d')}, {date_1.strftime('%Y')} and Ending {date_2.strftime('%B')} {date_2.strftime('%d')}, {date_2.strftime('%Y')}"
    data_dict['Period'] = [opn_string, period_string, "", "", "", "", "", "", ""]
    data_dict['Balance'] = [format_num("str", ob), format_num("str", income), format_num("str", expense), format_num("str", excpected_inflow), format_num("str", overdue), format_num("str", balance), format_num("str", 0.0), format_num("str", 0.0), format_num("str", 0.0)]
    cash_df = pd.DataFrame(data_dict)
    return cash_df

def Account_Balance(df):
    df['Amount'] =  df['Amount'].astype(str)
    df['Amount'] = df['Amount'].map(lambda Amount: float(Amount.replace(",", "")))
    accounts = df['Account'].unique()
    dict_df = {'Account': [], "Balance": []}
    for acc in accounts:
        balance = round(df[df['Account']==acc]['Amount'].sum(), 2)
        dict_df['Account'].append(acc) 
        dict_df['Balance'].append(balance) 
    acc_df = pd.DataFrame(dict_df)
    return acc_df
#####################################

########################################################################################################
################################### Budget Utilization Calculations ####################################
# Plans
budget = BUDGET[cols(BUDGET)]
budget_w3 = BG_W3[cols(BG_W3)]
budget_v22 = BG_VOICE22[cols(BG_VOICE22)]
budget_GnA = BG_GnA[cols(BG_GnA)]

# Revenues
sponsorships = SPONSORSHIP

# Expenses
gna = GENERAL
vna = VOICE_NA
v21 = VOICE21

def per_acc(df):
    accs = df['Account'].unique()
    q1 = [(df[df['Account']==acc]['Q1 TOTAL'].map(lambda Amount: float(Amount))).sum() for acc in accs]
    q2 = [(df[df['Account']==acc]['Q2 TOTAL'].map(lambda Amount: float(Amount))).sum() for acc in accs]
    q3 = [(df[df['Account']==acc]['Q3 TOTAL'].map(lambda Amount: float(Amount))).sum() for acc in accs]
    q4 = [(df[df['Account']==acc]['Q4 TOTAL'].map(lambda Amount: float(Amount))).sum() for acc in accs]
    balance = [df[df['Account']==acc]['Yearly'].sum() for acc in accs]

    return pd.DataFrame({'Account':accs, "Q1 TOTAL":q1, 'Q2 TOTAL':q2, 'Q3 TOTAL':q3, 'Q4 TOTAL':q4, "Yearly": balance})

period = [datetime.datetime(2022,1,1), datetime.datetime(2022,3,31), datetime.datetime(2022,6,30), datetime.datetime(2022,9,30), datetime.datetime(2022,12,31)]

def sum_budget(df):
    q1 = df["Q1 TOTAL"].values
    q2 = df["Q2 TOTAL"].values
    q3 = df["Q3 TOTAL"].values
    q4 = df["Q4 TOTAL"].values
    rev = [0.0, float(q1[0]), float(q1[0])+float(q2[0]), float(q1[0])+float(q2[0])+float(q3[0]), float(q1[0])+float(q2[0])+float(q3[0])+float(q4[0]),]
    cogs = [0.0, float(q1[1]), float(q1[1])+float(q2[1]), float(q1[1])+float(q2[1])+float(q3[1]), float(q1[1])+float(q2[1])+float(q3[1])+float(q4[1]),]
    return rev, cogs

def Actual(df):
    # period = [datetime.datetime(2022,1,1), datetime.datetime(2022,3,31), datetime.datetime(2022,6,30), datetime.datetime(2022,9,30), datetime.datetime(2022,12,31)]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by="Date")
    df = df.astype({"Amount": str})
    df["Amount"] = df["Amount"].map(lambda Amount: float(Amount.replace(",", "")))
    dates = [_ for _ in df['Date'].unique()]    
    actual = [0]
    i = 0
    for date in dates:
        sum_value = df[df['Date'] == date]['Amount'].sum()
        actual.append(actual[i] + sum_value)
        i = i+1

    dates = [(_ - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's') for _ in dates]  
    dates = [datetime.datetime.utcfromtimestamp(_) for _ in dates]  
    dates.insert(0, datetime.datetime(2022,1,1))
    return actual, dates

def plot_line(period, planned, title, rev = None, cogs = None):    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    if planned[0] is not None:
        fig.add_trace(go.Scatter(x=period, y=planned[0], name="Revenue Planned"),secondary_y=False,)
    fig.add_trace(go.Scatter(x=period, y=planned[1], name="COGS Planned"),secondary_y=False,)

    if rev is not None:
        fig.add_trace(go.Scatter(x=rev[1], y=rev[0], name="Revenue Actual"),secondary_y=False,)

    if cogs is not None:
        fig.add_trace(go.Scatter(x=cogs[1], y=cogs[0], name="COGS Actual"),secondary_y=False,)

    # Add figure title
    fig.update_layout(title_text=f"<b>{title}</b>")

    # Set x-axis title
    fig.update_xaxes(title_text="<b>Period</b> ")
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Amount</b> ", secondary_y=False)

    return fig

def period_actual(df, rev, cogs, period): 
    rev = rev.astype({"Amount": str})
    rev["Amount"] = rev["Amount"].map(lambda Amount: float(Amount.replace(",", "")))
    cogs = cogs.astype({"Amount": str})
    cogs["Amount"] = cogs["Amount"].map(lambda Amount: float(Amount.replace(",", "")))
    df["Q1 Actual"] = [round(rev[rev['Date']<=period[1]]["Amount"].sum(), 2), round(cogs[cogs['Date']<=period[1]]["Amount"].sum(), 2)]
    df["Q2 Actual"] = [round(rev[(rev['Date']>period[1])&(rev['Date']<=period[2])]["Amount"].sum(), 2), round(cogs[(cogs['Date']>period[1])&(cogs['Date']<=period[2])]["Amount"].sum(), 2)]
    df["YTD Actual"] = [round(rev["Amount"].sum(), 2), round(cogs["Amount"].sum(), 2)]
    bgt_cols = ["Account", "Q1 TOTAL", "Q1 Actual", "Q2 TOTAL", "Q2 Actual", "Q3 TOTAL", "Q4 TOTAL", "Yearly", "YTD Actual"]
    return df[bgt_cols]

