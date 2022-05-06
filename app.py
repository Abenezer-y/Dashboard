######
from lib2to3.pgen2.token import GREATER
import streamlit as st
import pandas as pd 
import datetime
import requests
import json
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
import plotly.graph_objects as go
import time
import plotly.express as px
from data_processing import format, week_range, convert_to_df, Grid, get_data, date_formatter, budget, budget_w3, budget_v22, budget_GnA, get_bills, Account_Balance
from data_processing import cashflow, get_upWork, get_credit, get_bank, get_data, get_sales, get_ledger, get_accounts, get_loan, get_receivables, get_payables, get_sponsorship, get_payroll, get_general, get_voice21, get_voice22, get_voiceNA, get_w3
#####################################

#####################################
########### Data Constants ##########
BILLS = get_bills()
UpWORK = get_upWork()
CREDITS = get_credit()
BANK = get_bank()
SALES = get_sales()
LEDGER = get_ledger()
ledger_col = [ _ for _ in LEDGER.columns][1:]
# BUDGET = get_budget()

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
    data_dict['Balance'] = ['{:,.2f}'.format(ob), '{:,.2f}'.format(income), '{:,.2f}'.format(expense), '{:,.2f}'.format(excpected_inflow), '{:,.2f}'.format(overdue), '{:,.2f}'.format(balance), 0.0, 0.0, 0.0]
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
##### Functions: Data Submition #####
def submit_income(doc):
    insertOne_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/insertOne"
    Payload = json.dumps({"collection": "income", "database": "Modev","dataSource": "BiCluster", "document": doc})
    response = requests.request("POST", insertOne_url, headers=headers, data=Payload)
    return response
def submit_receivable(doc):
    insertOne_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/insertOne"
    Payload = json.dumps({"collection": "receivables", "database": "Modev","dataSource": "BiCluster", "document": doc})
    response = requests.request("POST", insertOne_url, headers=headers, data=Payload)
    return response
#####################################
#####################################

#####################################
######## Options Constants ##########
reports = ["Cash Flow", "Budget Reconciliation", "Expenses", "Classes", "Accounts"]
periods = ["Current Week", "Previous Week", "Year to Date"]
projects = ["All", "Voice Summit 2022", "W3", "G&A"]
indices = [1, 2, 3, 4, 5]
income = {}
receivable = {}
jan_1 = datetime.datetime(2022,1,1,0,0,0)
today = datetime.datetime.today()
#####################################
#####################################


###########################################################################
################################### UI ####################################

#####################################
############## SIDEBAR ##############
reports = ["Cash Flow", "Budget Reconciliation", "Expenses", "Classes", "Accounts"]
periods = ["Current Week", "Previous Week", "Year to Date"]
projects = ["All", "Voice Summit 2022", "W3", "G&A"]

sideBar = st.sidebar
sideBar.title("Control Panel")
report = sideBar.selectbox('Reports', options=reports)
sideBar.header("Filters")
project = sideBar.selectbox('Projects', options=projects)
period = sideBar.selectbox('Period', options=periods)
#####################################
#####################################
CONTAINER = st.container()


#####################################
############# CASHFLOW ##############
if report == 'Cash Flow':
    CONTAINER.title("MODEV Cash Flow Dashboard Draft")
    CONTAINER.header('Cash Flow Summary')

    if period == 'Current Week':
        days = week_range(1)
        cash = cashflow(days[0], days[1])
        Cash = Grid(cash.iloc[indices], key='key_872w1', h=400)

    elif period == 'Previous Week':
        days = week_range(2)
        cash = cashflow(days[0], days[1])
        Cash = Grid(cash.iloc[indices], key='key_87991',  h=400)

    elif period == 'Year to Date':
        cash = cashflow(jan_1, today)
        Cash = Grid(cash, key='key_87dd991',  h=550)
#####################################
#####################################

#####################################
############## BUDGET ###############

elif report == "Budget Reconciliation":
    file_path_budget = 'E:/Users/abega/Documents/Hammerton Barca/MODEV/MODEV Finance/cash flow dashboard/Data/Budget/budget.xlsx'
    budget_sheet = pd.read_excel(file_path_budget, sheet_name=['All', 'W3', 'Voice22', 'GnA'])
    CONTAINER.title("Budget Management")
    if project == "All":
        with CONTAINER:
            df = budget_sheet['All']
            df['Q1 TOTAL'] = df['Q1 TOTAL'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Q2 TOTAL'] = df['Q2 TOTAL'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Q3 TOTAL'] = df['Q3 TOTAL'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Q4 TOTAL'] = df['Q4 TOTAL'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Yearly'] = df['Yearly'].map(lambda Amount: '{:,.2f}'.format(Amount))
            All = Grid(budget_sheet['All'], key='All', h=400)
            # st.info('Total Balance:  {:,.2f}'.format(bills['data']['Amount'].sum()))
        # if st.button('Export CSV'):
        #     bills['data'].to_csv("export.csv") 
    elif project == "Voice Summit 2022":
        with CONTAINER:

            sp_v22 = SPONSORSHIP[SPONSORSHIP['Class'] == 'Voice Summit 2022']
            sp_v22['Amount'] = pd.to_numeric(sp_v22['Amount'])
            exp_acc = Account_Balance(VOICE22)
            budget_sheet['Voice22']['Q1 Actual'] = [sp_v22['Amount'].sum(), exp_acc['Balance'].sum()]
            budget_sheet['Voice22']['YTD Actual'] = [sp_v22['Amount'].sum(), exp_acc['Balance'].sum()]

            budget_sheet['Voice22']['Q1 Delta'] = [(budget_sheet['Voice22']['Q1 TOTAL'].values[0] - budget_sheet['Voice22']['Q1 Actual'].values[0]), (budget_sheet['Voice22']['Q1 TOTAL'].values[1] - budget_sheet['Voice22']['Q1 Actual'].values[1])]
            budget_sheet['Voice22']['Yearly Delta'] = [(budget_sheet['Voice22']['Yearly'].values[0] - budget_sheet['Voice22']['YTD Actual'].values[0]), (budget_sheet['Voice22']['Yearly'].values[1] - budget_sheet['Voice22']['YTD Actual'].values[1])]
            

            col = ['Account', 'Q1 TOTAL', 'Q1 Actual', 'Q1 Delta', 'Q2 TOTAL', 'Q3 TOTAL', 'Q4 TOTAL', 'Yearly', 'YTD Actual', 'Yearly Delta']
            df = budget_sheet['Voice22'][col]
            df['Q1 TOTAL'] = df['Q1 TOTAL'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Q1 Actual'] = df['Q1 Actual'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Q1 Delta'] = df['Q1 Delta'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Q2 TOTAL'] = df['Q2 TOTAL'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Q3 TOTAL'] = df['Q3 TOTAL'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Q4 TOTAL'] = df['Q4 TOTAL'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Yearly'] = df['Yearly'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['YTD Actual'] = df['YTD Actual'].map(lambda Amount: '{:,.2f}'.format(Amount))
            df['Yearly Delta'] = df['Yearly Delta'].map(lambda Amount: '{:,.2f}'.format(Amount))

            # df_pivot = budget_sheet['Voice22'].pivot(columns='Account', values='Yearly')
            # fig = px.line(df_pivot, x="Sponsorship", y="COGS", title='Life expectancy in Canada')
            # CONTAINER.plotly_chart(fig, use_container_width=True, sharing="streamlit")
            Voice22 = Grid(df, key='Voice22', h=300)
            
            c1, c2 = CONTAINER.columns(2)
            with c1:
                st.header("Expense Accounts")
                V22_Exp = Grid(Account_Balance(VOICE22), key='V22_Exp', h=400)
                st.info('Total Balance:  {:,.2f}'.format(V22_Exp['data']['Balance'].sum()))
            with c2:
                st.header("Sponsorships")
                V22_SP = Grid(sp_v22[['Customer', 'Amount']], key='V22_SP', h=400)
                st.info('Total Balance:  {:,.2f}'.format(V22_SP['data']['Amount'].sum()))

    elif project == "W3":
        sp_W3 = SPONSORSHIP[SPONSORSHIP['Class'] == 'W3']
        sp_W3['Amount'] = pd.to_numeric(sp_W3['Amount'])
        exp_W3 = Account_Balance(W3)
        budget_sheet['W3']['Q1 Actual'] = [sp_W3['Amount'].sum(), exp_W3['Balance'].sum()]
        budget_sheet['W3']['YTD Actual'] = [sp_W3['Amount'].sum(), exp_W3['Balance'].sum()]
        col = ['Account', 'Q1 TOTAL', 'Q1 Actual', 'Q2 TOTAL', 'Q3 TOTAL', 'Q4 TOTAL', 'Yearly', 'YTD Actual']
        with CONTAINER:
            grid_w3 = Grid(budget_sheet['W3'][col], key='W3', h=300)
            c1, c2 = CONTAINER.columns(2)
            with c1:
                st.header("Expense Accounts")
                Exp_W3 = Grid(exp_W3, key='exp_W3', h=400)
                st.info('Total Balance:  {:,.2f}'.format(Exp_W3['data']['Balance'].sum()))
            with c2:
                st.header("Sponsorships")
                W3_SP = Grid(sp_W3[['Customer', 'Amount']], key='sp_W3', h=400)
                st.info('Total Balance:  {:,.2f}'.format(W3_SP['data']['Amount'].sum()))

    elif project == "G&A":
        with CONTAINER:
            GnA = Grid(budget_sheet['GnA'], key='GnA')
#####################################
#####################################

#####################################
############## BUDGET ###############
elif report == "Expenses":
    CONTAINER.title("Modev Expenses")
    file = CONTAINER.selectbox('',options=['Bills', 'Upwork', 'Bank Statement', 'Credit', 'Sales', 'Payables', "Loan", 'Receivables', 'Ledger'])
    if file == "Bills":
        with CONTAINER:
            col_0 = ["PROCESS DATE", 'Created Date','Class', 'Chart of account', 'Vendor', "Invoice Number",'Amount', "Payment Status", "Due Date", 'Approval Status']
            bills = Grid( BILLS, key='Bills', p=False)
            # st.info('Total Balance:  {:,.2f}'.format(bills['data']['Amount'].sum()))
        if st.button('Export CSV'):
            bills['data'].to_csv("export.csv") 
        
    elif file == "Upwork":
        with CONTAINER:
            col = ["Date", 'Class', 'Description', "Contract",'Amount']
            up_work = Grid(UpWORK, key='Upwork')
            # st.info('Total Balance:  {:,.2f}'.format(up_work['data']['Amount'].sum()))
        if st.button('Export CSV'):
            up_work['data'].to_csv("export.csv") 
    elif file == "Bank Statement":
        with CONTAINER:
            col = ["Date", "Transaction", 'Description', 'Amount']
            BANK['Date'] = pd.to_datetime(BANK['Date'])
            bank_stm = Grid(BANK, key='Bank', p=False)
            # st.info('Total Balance:  {:,.2f}'.format(bank_stm['data']['Amount'].sum()))
        if st.button('Export CSV'):
            bank_stm['data'].to_csv("export.csv")    
    elif file == 'Sales':
        with CONTAINER:
            credit_stm = Grid(SALES, key='Sales')
            # st.info('Total Balance:  {:,.2f}'.format(credit_stm['data']['Amount'].sum()))
            if st.button('Export CSV'):
                credit_stm['data'].to_csv("export.csv") 
    elif file == 'Loan':
        with CONTAINER:
            credit_stm = Grid(LOAN, key='Loan')
            # st.info('Total Balance:  {:,.2f}'.format(credit_stm['data']['Amount'].sum()))
    elif file == 'Credit':
        with CONTAINER:
            credit_stm = Grid(CREDITS, key='Credit', p=False)
            st.info('Total Balance:  {:,.2f}'.format(credit_stm['data']['Amount'].sum()))
            if st.button('Export CSV'):
                credit_stm['data'].to_csv("export.csv") 
    elif file == 'Payables':
        with CONTAINER:
            credit_stm = Grid(PAYABLES, key='Payables')
            # st.info('Total Balance:  {:,.2f}'.format(credit_stm['data']['Amount'].sum()))
    elif file == 'Receivables':
        with CONTAINER:
            credit_stm = Grid(SALES, key='Receivables')
            # st.info('Total Balance:  {:,.2f}'.format(credit_stm['data']['Amount'].sum()))
    elif file == 'Ledger':
        with CONTAINER:
            credit_stm = Grid(LEDGER[ledger_col], key='Ledger', p=False)
            # st.info('Total Balance:  {:,.2f}'.format(credit_stm['data']['Amount'].sum()))
    
#####################################
#####################################

#####################################
############## BUDGET ###############
elif report == "Classes":
    classes = CONTAINER.selectbox('Classes',options=['Voice22', 'W3', 'Voice21', 'VoiceNA', "G&A"])
    if classes == "Voice22":
        with CONTAINER:
            Voice22 = Grid( VOICE22, key='VOICE22')
            # st.info('Total Balance:  {:,.2f}'.format(Voice22['data']['Amount'].sum()))
    elif classes == "W3":
        with CONTAINER:
            Voice22 = Grid( W3, key='W3')
    elif classes == "Voice21":
        with CONTAINER:
            Voice22 = Grid( VOICE21, key='Voice21')
    elif classes == "VoiceNA":
        with CONTAINER:
            Voice22 = Grid( VOICE_NA, key='VoiceNA')
    elif classes == "G&A":
        with CONTAINER:
            Voice22 = Grid( GENERAL, key='G&A')
#####################################
#####################################

#####################################
############## BUDGET ###############
elif report == "Accounts":
    CONTAINER.title("Recivabels Management")
    with st.form("my_form_receivable"):
        c20, c21, c22 = CONTAINER.columns(3)
        date = c20.date_input("Date", datetime.datetime(2022, 1, 1))
        c21.empty()
        due = c22.date_input("Due Date", datetime.datetime(2022, 12, 31))
        customer = c20.text_input('Name', 'Cash source')
        ref = c21.text_input('Ref.', 'Invoice Number, etc...')
        amount = c22.text_input('Amount', '0.00')
        class_name = c20.selectbox('Class', ('Voice Summit', 'W3'))
        c21.empty()
        acc = c22.selectbox('Account', ('Sponsorship', 'Other'))
        submitted = st.form_submit_button("Check")
        if submitted:
            st.write("Date:", date, "-  Customer:", customer,"-  Ref:", ref, "-  Class:", class_name,"-  Account:", acc, "-  Amount:", amount, "-  Due Date:", due)
    if st.button('Comfirm and Submit'):
        receivable["Date"] = str(date)
        receivable["Customer"] = str(customer)
        receivable["Ref"] = str(ref)  
        receivable["Class"] = str(class_name) 
        receivable["Account"] = str(acc) 
        receivable["Amount"] = float(amount) 
        receivable["Due"] = str(due) 
        response = submit_receivable(receivable)
        if response.ok:
            st.info('Success')
        else:
            st.info('Failed')
    # col = ['Date', 'Customer', 'Class', 'Amount', 'Due']
    # rc_grid = Grid(receivables[col], key='key_123')
#####################################
#####################################