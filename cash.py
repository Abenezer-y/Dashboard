import pandas as pd
from data_processing import get_bank, get_sales


BANK = get_bank()
SALES = get_sales()



ob =BANK[BANK['Description']=='Opening Balance']['Amount'].values[0]
overdue = SALES[SALES['Status']=='overdue']['Total'].sum()
open_invoice = SALES[SALES['Status']=='open']['Total'].sum()
excpected_inflow = overdue + open_invoice



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

    income = bank[bank['Amount']>0.0]['Amount'].sum()
    expense = bank[bank['Amount']<0.0]['Amount'].sum()

    
    data_dict = {}
    data_dict['Description'] = ["Opening Balance", "Cash In", "Cash Out", "Open Invoice", "Overdue Invoices", "Bank Balance", "Estimated Revenue", "Estimated Payments", "Estimated Bank Balance"]
    period_string = f"For the period Begining {date_1.strftime('%B')} {date_1.strftime('%d')}, {date_1.strftime('%Y')} and Ending {date_2.strftime('%B')} {date_2.strftime('%d')}, {date_2.strftime('%Y')}"
    data_dict['Period'] = [period_string, "", "", "", "", "", "", "", ""]
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