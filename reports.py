import pandas as pd
from db_functions import Ledger_DB, formatnum
import datetime

opening_balance =Ledger_DB[Ledger_DB['description']=='Opening Balance']['amount'].values[0]
today = datetime.datetime.today()
bank_db = Ledger_DB[(Ledger_DB['category']=='Bank - Deposit')|(Ledger_DB['category']=='Bank - Withdrawal')]
sales = Ledger_DB[Ledger_DB['category']=='Sales QuickBooks']
bills = Ledger_DB[Ledger_DB['status']=='Scheduled']

bank_db['processing_date'] = pd.to_datetime(bank_db['processing_date'])
sales['due_date'] = pd.to_datetime(sales['due_date'])
bills['due_date'] = pd.to_datetime(bills['due_date'])



def cash_flow(date_1=None, date_2=None):

    if (date_1 is None) & (date_2 is None):
        d_1 = datetime.datetime(2022,1,1,0,0,0)
        d_2 = today
    else:
        d_1 = date_1
        d_2 = date_2

    bank = bank_db[(bank_db['processing_date']>=d_1) & (bank_db['processing_date']<=d_2)]
    invoices = sales[(sales['status']=='open')|(sales['status']=='overdue')]
    payables = bills[bills['due_date']<=d_2]

    inflow = bank[bank['amount']>0]['amount'].sum()
    outflow = bank[bank['amount']<0]['amount'].sum()

    bank_balance= bank_db[bank_db['processing_date']<=d_2]['amount'].sum()

    open_invoices = invoices['amount'].sum()
    overdue_invoices = invoices[invoices['status']=='overdue']['amount'].sum()
    estimated_inflow = invoices[invoices['due_date']<=d_2]['amount'].sum()
    estimated_payments = payables['amount'].sum()
    est_balance = bank_balance + open_invoices + estimated_payments

    deiscription = ['Opening Balance', 'Cash In', 'Cash Out', 'Bank Balance', 'Open Invoices', 'Overdue Invoices', 'Estimated Payment', 'Estimated Cash In', 'Estimated Bank Balance'] 
    d2_str = f"{d_2.strftime('%B')} {d_2.strftime('%d')}, {d_2.strftime('%Y')}"
    period = ['as of January 1, 2022', '', '', 'As of ' + d2_str, '', '', 'Ending ' + d2_str, 'Ending ' + d2_str, 'Ending ' + d2_str]
    amount = [opening_balance, inflow, outflow, bank_balance, open_invoices, overdue_invoices, estimated_payments, estimated_inflow, est_balance]
    amounts = [formatnum(_, '') for _ in amount]
    cash_dict = {'Description': deiscription, 'Period': period, "Amount": amounts}

    return pd.DataFrame(cash_dict)


def over_due():
    overdue_invoices = sales[sales['status']=='overdue'][['vendor','amount', 'due_date']]
    overdue_invoices['due_date'] = overdue_invoices['due_date'].map(lambda date: str(date).split(' ')[0])
    return overdue_invoices.rename(columns={'vendor': 'Customer', 'amount': 'Amount', 'due_date': 'Due'})

def payables(d_2):
    payables = bills[bills['due_date']<=d_2]
    payables['due_date'] = payables['due_date'].map(lambda date: str(date).split(' ')[0])
    return payables[['vendor','amount', 'due_date']].rename(columns={'vendor': 'Vendor', 'amount': 'Amount', 'due_date': 'Due'})