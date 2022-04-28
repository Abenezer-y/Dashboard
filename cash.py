import pandas as pd
from data_processing import get_bank, get_sales, get_bills, format_num
from processor_bills import payables, paid_bills

BANK = get_bank()
SALES = get_sales()
BILLS = get_bills()


BANK['Date'] = pd.to_datetime(BANK['Date'])
SALES['Date'] = pd.to_datetime(SALES['Date'])
SALES['Due date'] = pd.to_datetime(SALES['Due date'])

SALES["Total"] = SALES["Total"].map(lambda Amount: format_num('num', Amount))



ob =BANK[BANK['Description']=='Opening Balance']['Amount'].values[0]
inflow = BANK[(BANK['Description']!='Opening Balance') & (BANK['Amount']>0.0)]
outflow = BANK[BANK['Amount']<0.0]

open = SALES[(SALES["Status"] == 'open') | (SALES["Status"] == 'overdue')]

open_invoices = SALES[(SALES["Status"] == 'open') | (SALES["Status"] == 'overdue')]['Total'].sum()
overdue_invoices = SALES[SALES["Status"] == 'overdue']['Total'].sum()

payables['Due Date'] = pd.to_datetime(payables['Due Date'])


# excpected_payment = 0.0
def estimated_cashout(credit, loan, bills):
    credit['Date'] = pd.to_datetime(credit['Date'])
    loan['Date'] = pd.to_datetime(loan['Date'])
    bills['Date'] = pd.to_datetime(bills['Date'])


#### Functions: Data Processing #####
def cashflow(date_1=None, date_2 = None):

    if (date_1  is None and date_2  is None):
        bank = BANK
        balance = bank['Amount'].sum()
    else:
        income_df = inflow[(inflow['Date']>=date_1) & (inflow['Date']<=date_2)]
        expense_df = outflow[(outflow['Date']>=date_1) & (outflow['Date']<=date_2)]
        excpected_inflow = open[open['Due date'] <= date_2]['Total'].sum()
        balance = BANK[BANK['Date']<=date_2]['Amount'].sum()
        excpected_payment = payables[(payables["Payment Status"] == "Scheduled")&(payables["Due Date"] <=date_2)]['Amount'].sum()
    income = income_df['Amount'].sum()
    expense = expense_df['Amount'].sum()
    

    est_balance = balance + excpected_inflow - excpected_payment
    data_dict = {}
    data_dict['Description'] = ["Opening Balance", "Cash In", "Cash Out", "Bank Balance", "Open Invoices", "Overdue Invoices", "Estimated Revenue", "Estimated Payments", "Estimated Bank Balance"]
    period_string = f"From {date_1.strftime('%B')} {date_1.strftime('%d')}, {date_1.strftime('%Y')} to {date_2.strftime('%B')} {date_2.strftime('%d')}, {date_2.strftime('%Y')}"
    data_dict['Period'] = ["For the period Begining Jan 01, 2022", period_string, "", f"As of {date_2.strftime('%B')} {date_2.strftime('%d')}, {date_2.strftime('%Y')}", 
    "", "", f"As of {date_2.strftime('%B')} {date_2.strftime('%d')}, {date_2.strftime('%Y')}", f"As of {date_2.strftime('%B')} {date_2.strftime('%d')}, {date_2.strftime('%Y')}", f"As of {date_2.strftime('%B')} {date_2.strftime('%d')}, {date_2.strftime('%Y')}"]
    data_dict['Balance'] = [format_num('str', ob), format_num('str', income), format_num('str', expense), format_num('str', balance), format_num('str', open_invoices), format_num('str', overdue_invoices), format_num('str', excpected_inflow), format_num('str', excpected_payment), format_num('str', est_balance)]
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