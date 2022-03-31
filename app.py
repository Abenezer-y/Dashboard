import streamlit as st
import pandas as pd 
from datetime import datetime
import requests
import json
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
import plotly.graph_objects as go


headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}

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


def Grid(df, key, h=750):
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(groupable=True)
    gd.configure_selection('single')
    grid_option =gd.build()
    grid = AgGrid(df,  key=key,
                    gridOptions=grid_option,
                    update_mode=GridUpdateMode.MODEL_CHANGED,
                    fit_columns_on_grid_load=True, 
                    theme="material", 
                    height=h, 
                    width='100%')
    return grid

@st.cache
def get_bills():
    findAll_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/find"
    Payload = json.dumps({"collection": "bills", "database": "Modev","dataSource": "BiCluster", "filter": {}})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    return convert_to_df(response)

@st.cache
def get_upwork():
    findAll_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/find"
    Payload = json.dumps({"collection": "upwork", "database": "Modev","dataSource": "BiCluster", "filter": {}})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    return convert_to_df(response)


@st.cache
def get_bank():
    findAll_url = "https://data.mongodb-api.com/app/data-wqlxh/endpoint/data/beta/action/find"
    Payload = json.dumps({"collection": "bankStatement", "database": "Modev","dataSource": "BiCluster", "filter": {}})
    response = requests.request("POST", findAll_url, headers=headers, data=Payload)
    return convert_to_df(response)

bills = get_bills()
upWork = get_upwork()
bank = get_bank()



# df = pd.read_json(data)
# Default values 
today = datetime.today()
opening_balance = 148136.99
toDay = today.strftime('%m/%d/%Y')

# Selector options 
reports = ["Cash Flow", "Budget Reconciliation", "Loan Manager"]
periods = ["Current Week", "Current Month", "Year to Date"]
projects = ["All", "Voice Summit 2022", "W3", "G&A"]

# imported files path
credit_card = './card.csv'
bill = './bill.csv'
# upWork = './upWork.csv'
bank = pd.read_csv('./bank_clean.csv')
budget_path = './budget.xlsx'

# Title bar Data
income = "{:,.2f}".format(bank[bank['Amount']>0].Amount.sum())
withdrawals = "{:,.2f}".format(bank[bank['Amount']<0].Amount.sum())
bal_calc = opening_balance + bank[bank['Amount']>0].Amount.sum() + bank[bank['Amount']<0].Amount.sum()
balance = "{:,.2f}".format(bal_calc)



data = {"Line Item":[], "Budget": [], "Account": []}






# UI Section
sideBar = st.sidebar
sideBar.title("Control Panel")

report = sideBar.selectbox('Reports', options=reports)
container_0 = st.container()



if report == 'Cash Flow':
    container_0.title("Modev Cash Flow Dashboard Draft")
    c1, c2, c3, = container_0.columns(3)
    with c1:
        st.metric(label="Bank Balance", value=balance)
    with c2:
        st.metric(label="Cash In (YTD)", value=income)
    with c3:
        st.metric(label="Cash Out (YTD)", value=withdrawals)

    container_0.header('Cash Flow Summary')
    c4, c5, c6 = container_0.columns(3)
    start = c4.date_input("Reporting period", today) 
    end = c5.date_input('to', today)
    dt_start = start.strftime("%m/%d/%Y")
    start_dt = datetime.strptime(dt_start, "%m/%d/%Y")
    dt_end = end.strftime("%m/%d/%Y")
    end_dt = datetime.strptime(dt_end, "%m/%d/%Y")
    c6.selectbox('Project', options=projects)
    bank['Date'] = pd.to_datetime(bank['Date'])

    # bank['Date'] = bank['Date'].map(lambda date: datetime.strptime(date, '%m/%d/%Y').date())
    # bank = bank[(bank['Date']>= period) and (bank['Date']>= end)]
    # if (period == today) & (end == today):
    bank = bank[(bank["Date"]>=start_dt) & (bank["Date"]<=end_dt)]
    income = "{:,.2f}".format(bank[bank['Amount']>0].Amount.sum())
    withdrawals = "{:,.2f}".format(bank[bank['Amount']<0].Amount.sum())
# Cash Flow Table Data
    cash_flow = {"Description": [f'Cash In: For the period {dt_start} to {dt_end}'  , 
                                          f'Cash Out: For the period {dt_start} to {dt_end}', 
                                          'Open Invoices', 
                                          'Overdue Invoices', 
                                          'EST. Cash out until end of month', 
                                          f'Bank Balance {toDay}'], 
                        "Balance": [income, 
                                    withdrawals, 
                                    '0', 
                                    '0', 
                                    '0', 
                                   balance]}
    
    cf_df = pd.DataFrame(cash_flow)
    Grid(cf_df, key='key_0', h=400)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[_ for _ in bank[bank['Amount']>0]['Date']], y=[_ for _ in bank[bank['Amount']>0]['Amount']], fill='tozeroy')) # fill down to xaxis
    fig.add_trace(go.Scatter(x=[_ for _ in bank[bank['Amount']<0]['Date']], y=[_ for _ in bank[bank['Amount']<0]['Amount']], fill='tozeroy')) # fill to trace0 y
    st.plotly_chart(fig, use_container_width=True)
    
    # fig.show()
    # st.table(cash_flow["Data"])
    # tonexty


elif report == "Budget Reconciliation":
    budget_df = pd.read_excel(budget_path, sheet_name="Modev Budget")
    revenue = budget_df[budget_df['Account Type'] == "Revenue"][['Total Budget']].sum()
    expense = budget_df[budget_df['Account Type'] == "Expense"][['Total Budget']].sum()
    diff = revenue["Total Budget"].sum() - expense["Total Budget"].sum()
    container_0.title("Modev Annual Budget")
    c7, c8, c9, = container_0.columns(3)
    with c7:
        st.metric(label="Revenue", value=revenue)
    with c8:
        st.metric(label="Costs", value=expense)
    with c9:
        st.metric(label="Earning", value=str(diff))

    container_0.header('Budget Plan')

    c10, c11 = container_0.columns(2)
    budget = c10.selectbox('Projects',options=['Company', 'Voice Summit 2022', 'W3'])
    bug_per = c11.selectbox('Period',options=['Annual', 'Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4'])

    budget_df['Total Budget'] = budget_df['Total Budget'].map(lambda Amount: "$ {:,.2f}".format(Amount))
    AgGrid(budget_df[['Project Class', 'Description', 'Q1', 'Q2', 'Q3', 'Q4', 'Total Budget']], editable=True, fit_columns_on_grid_load=True)
  


elif report == "Loan Manager":
    container_0.title("Modev Annual Budget")
    container_0.header('Budget Plan')
    file = container_0.selectbox('Files',options=['Bills', 'Upwork', 'Bank Statement', 'Credit'])
    if file == "Bills":
        with container_0:
            col = ["Date", 'Class', 'Vendor', 'Amount', 'Status']
            Grid(bills[col], key='key_1')

    elif file == "Upwork":
        with container_0:
            # col = ["Date", 'Class', 'Vendor', 'Amount', 'Status']
            Grid(upWork, key='key_2')




        
    # df_template = pd.DataFrame(
    # '',
    # index=range(3),
    # columns=["Class", "Account Name", "Account Type", "Balance"])

    # with st.form('example form') as f:
    #     st.header('Example Form')
    #     response = AgGrid(df_template, editable=True, fit_columns_on_grid_load=True)
    #     st.form_submit_button()

    # grid = AgGrid(response['data'])
    # # grid

