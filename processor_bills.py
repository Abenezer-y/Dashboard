from data_processing import  get_bills
import pandas as pd
import datetime




def class_classifier(df):
    classes = [_ for _ in df['Class'].unique()]
    class_expenses = {}

    for project in classes:
        class_expenses[project] = df[df['Class'] == project].drop_duplicates(subset=["Description", "Vendor", "Account", "Class", "Amount"])

        if project == 'Split':
            class_expenses[project]['Amount'] = class_expenses[project]['Amount'].map(lambda Amount: Amount/2)

    return class_expenses



bills = get_bills()
bills.rename(columns={'Invoice Amount ':'Amount', 'Invoice Number': 'Description', 'PROCESS DATE': 'Date', 'Chart of account': "Account"}, inplace=True)


dec_15 = datetime.datetime(2021, 11, 30)
dec_31 = datetime.datetime(2021, 12, 31)


bills['Created Date'] =pd.to_datetime(bills['Created Date'])
bills['Invoice Date'] =pd.to_datetime(bills['Invoice Date'])
bills['Due Date'] =pd.to_datetime(bills['Due Date'])


bill_df = bills[bills["Created Date"]>=dec_15]
bill_df['Amount'] = bill_df['Amount'].map(lambda Amount: float(Amount.replace(",", "")))
bill_df['Method'] = ['Cash' for i in range(bill_df.shape[0])]
bill_df['Type'] = ['Expense' for i in range(bill_df.shape[0])]



paid_bills = bill_df[(bill_df["Payment Status"] == "Paid") & (bill_df["Date"] != "0") & (bill_df["PAYMENT STATUS"] != 'Voided')]
paid_bills['Date'] =pd.to_datetime(paid_bills['Date'])
paid_bills = paid_bills[paid_bills['Date']>=dec_31]

# paid_per_class = class_classifier(paid_bills)

payables = bill_df[(bill_df["Approval Status"] != 'Denied') & (bill_df["Approval Status"] != 'Unassigned')]
payables = payables[(payables["Payment Status"] == "Scheduled") | (payables["Payment Status"] == 'Unpaid')]

# payables_per_class = class_classifier(payables)

