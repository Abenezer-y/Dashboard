######
import streamlit as st
st.set_page_config(layout="wide")
import datetime
from class_voice22 import v22_fig, budget_v22, v22_REV, v22_COGS 
from class_w3 import  w3_fig, budget_w3, w3_REV, w3_COGS 
from class_all import  budget_All, ALL_FIG
from class_general import  gna_fig, bdg_GnA
from cash import  cashflow, estimated_cashin, estimated_cashout
from data_processing import format_num, week_range, Grid, j_code, budget_GnA, Account_Balance
from reports import cash_flow, payables, receivables
######


#####################################
######## Utility Constants ##########
headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*','api-key': 'quuKmslQouhgHNNdtya30WaRxNhXxVcvD5WJlJ0vGmsa9Z9ZccSV4eKast0OjAHb'}
jan_1 = datetime.datetime(2022, 1, 1, 0, 0, 0)
today = datetime.datetime.today()
reports = ["Cash Flow", "Budget Reconciliation",]
periods = ["Current Week", "Previous Week", "Year to Date", "Custom range"]
projects = ["All", "Voice Summit 2022", "W3", "G&A"]
indices = [1, 2, 3, 4, 5, 6, 7]
indices_yt = [0, 1, 2, 3, 4, 5, 6, 7, 8]
income = {}
receivable = {}
#####################################

###########################################################################
################################### UI ####################################

############## SIDEBAR ##############
sideBar = st.sidebar
sideBar.title("Control Panel")
report = sideBar.selectbox('Reports', options=reports)
sideBar.header("Filters")
if report == "Cash Flow":
    period = sideBar.selectbox('Period', options=periods)
    if period == "Custom range":
        Date_1 = sideBar.date_input("Begining Date")
        Date_2 = sideBar.date_input("Ending Date")
elif report == "Budget Reconciliation":
    project = sideBar.selectbox('Classes', options=projects)


############# CONTAINER #############
CONTAINER = st.container()

# CASHFLOW 
if report == 'Cash Flow':
    CONTAINER.title("MODEV Cash Flow Report")
    
    if period == 'Current Week':
        CONTAINER.header('Cash Flow Summary - Current Week')
        days = week_range(1)
        cash = cash_flow(days[0], days[1])
        Cash = Grid(cash.iloc[indices], key='key_872w1', h=208, p=False)
        col1, col2 = st.columns(2)
        with col1:
            st.write('Receivable')
            Cash = Grid(receivables(days[1]), key='key_87dd2w1', h=205, p=False)
        with col2:
            st.write('Payables')
            Cash = Grid(payables(days[1]), key='key_872scw1', h=205, p=False)
    elif period == 'Previous Week':
        CONTAINER.header('Cash Flow Summary - Previous Week')
        days = week_range(2)
        cash = cash_flow(days[0], days[1])
        Cash = Grid(cash.iloc[indices], key='key_87991',  h=208, p=False)
        col1, col2 = st.columns(2)
        with col1:
            st.write('Receivable')
            Cash = Grid(receivables(days[1]), key='key4_87ddn2w1', h=205, p=False)
        with col2:
            st.write('Payables')
            Cash = Grid(payables(days[1]), key='ke4y_87nf2scw1', h=205, p=False)
    elif period == 'Year to Date':
        CONTAINER.header('Cash Flow Summary - Year to Date')
        cash = cash_flow()
        Cash = Grid(cash.iloc[indices_yt], key='key_87dd991',  h=230, p=False)
        col1, col2 = st.columns(2)
        with col1:
            st.write('Receivable')
            Cash = Grid(receivables(today), key='key_w87ddcn2w1', h=205, p=False)
        with col2:
            st.write('Payables')
            Cash = Grid(payables(today), key='key_487naf2scw1', h=205, p=False)
    elif period == 'Custom range':
        title = f"Cash Flow Summary - {Date_1.strftime('%B')} {Date_1.strftime('%d')} , {Date_1.strftime('%Y')} to {Date_2.strftime('%B')} {Date_2.strftime('%d')}, {Date_2.strftime('%Y')}"
        CONTAINER.header(title)
        d1 = datetime.datetime(Date_1.year, Date_1.month, Date_1.day)
        d2 = datetime.datetime(Date_2.year, Date_2.month, Date_2.day)
        cash = cash_flow(d1, d2)
        Cash = Grid(cash, key='key_87drrf991',  h=260, p=False)
        col1, col2 = st.columns(2)
        with col1:
            st.write('Receivable')
            Cash = Grid(receivables(d2), key='key_87sddcn2w1', h=205, p=False)
        with col2:
            st.write('Payables')
            Cash = Grid(payables(d2), key='key_87qnaf2scw1', h=205, p=False)
#####################################

# Budget Utilization 
elif report == 'Budget Reconciliation':
    if project == 'All':
        CONTAINER.title("MODEV Planned Budget vs Actual - All Classes")
        CONTAINER.plotly_chart(ALL_FIG, use_container_width=True)
        bg_all = Grid(budget_All, key='All', h=160, p=False)
    ########
    elif project == 'G&A':
        CONTAINER.title("MODEV Planned Budget vs Actual - General and Admin")
        CONTAINER.plotly_chart(gna_fig, use_container_width=True)
        
        bg_gna = Grid(bdg_GnA, key='G&A',  p=False, h=160)
        
        st.info('Total Budget for Non Project Costs:  {:,.0f}'.format((bg_gna['data']['Yearly'].map(lambda Amount:format_num('num', Amount)).sum())))
        # Q2_DF,  Q1_DF
        with st.expander("General and Admin Costs Detail"):
            accs = budget_GnA['Account'].unique()
            c5, c6, c7, c8, c9 = st.columns(5)
            cols = ["Detail", "Yearly"]
            budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount:format_num('str', Amount))
            with c5:
                c5.write(accs[0])
                Exp_0 = Grid(budget_GnA[budget_GnA['Account']==accs[0]][cols], key=accs[0], h=400,  p=False)
                sum_value = format_num('str', (Exp_0['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum())
                st.info(f'Total Balance:  {sum_value }')
            with c6:
                c6.write(accs[1])
                # budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float((str(Amount)).replace(",", ""))))
                Exp_1 = Grid(budget_GnA[budget_GnA['Account']==accs[1]][cols], key=accs[1], h=400,  p=False)
                sum_value = format_num('str', (Exp_1['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum())
                st.info(f'Total Balance:  {sum_value }')
            with c7:
                c7.write(accs[2])
                # budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float((str(Amount)).replace(",", ""))))
                Exp_2 = Grid(budget_GnA[budget_GnA['Account']==accs[2]][cols], key=accs[2], h=400,  p=False)
                sum_value = format_num('str', (Exp_2['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum())
                st.info(f'Total Balance:  {sum_value }')
            with c8:
                c8.write(accs[3])
                # budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float((str(Amount)).replace(",", ""))))
                Exp_3 = Grid(budget_GnA[budget_GnA['Account']==accs[3]][cols], key=accs[3], h=400,  p=False)
                sum_value = format_num('str', (Exp_3['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum())
                st.info(f'Total Balance:  {sum_value }')
            with c9:
                c9.write(accs[4])
                # budget_GnA['Yearly']= budget_GnA['Yearly'].map(lambda Amount: '{:,.2f}'.format(float((str(Amount)).replace(",", ""))))
                Exp_4 = Grid(budget_GnA[budget_GnA['Account']==accs[4]][cols], key=accs[4],  h=400,  p=False)
                sum_value = format_num('str', (Exp_4['data']['Yearly'].map(lambda Amount: float((str(Amount)).replace(",", "")))).sum())
                st.info(f'Total Balance:  {sum_value }')
    ########
    elif project == 'Voice Summit 2022':

        CONTAINER.title("MODEV Planned Budget vs Actual - Voice Summit 2022")
        CONTAINER.plotly_chart(v22_fig, use_container_width=True)

        bg_v22 = Grid(budget_v22, key='Voice22',  h=85, p=False)
        c1, c2 = st.columns(2)
        with c1:
            c1.header("COGS")
            v22_COGS_df = Account_Balance(v22_COGS)
            v22_COGS_df['Balance'] = v22_COGS_df['Balance'].map(lambda Amount: format_num('str', Amount))
            V22_Exp = Grid(v22_COGS_df, key='V22_Exp', h=200, p=False)
            st.info('Total Balance:  {:,.0f}'.format((V22_Exp['data']['Balance'].map(lambda Amount: float(Amount.replace(",","")))).sum()))
        with c2:
            c2.header("Revenue")
            v22_REV['Amount'] = v22_REV['Amount'].map(lambda Amount: format_num('str', Amount))
            V22_SP = Grid(v22_REV[["Vendor", "Account", "Amount"]], key='V22_SP', h=200, p=False)
            st.info('Total Balance:  {:,.0f}'.format((V22_SP['data']['Amount'].map(lambda Amount: float(Amount.replace(",","")))).sum()))
    ########
    elif project == 'W3':

        CONTAINER.title("MODEV Planned Budget vs Actual - W3")
        CONTAINER.plotly_chart(w3_fig, use_container_width=True)

        bg_w3 = Grid(budget_w3, key='W3',  h=85, p=False, jscode=j_code)
        c3, c4 = st.columns(2)

        with c3:
            c3.header("COGS")
            cogs_w3 = Account_Balance(w3_COGS)
            cogs_w3['Balance'] = cogs_w3['Balance'].map(lambda Amount: format_num('str', Amount))
            W3_Exp = Grid(cogs_w3, key='W3_Exp', h=200, p=False)
            sum_value = format_num('num', (W3_Exp['data']['Balance']).sum())
            st.info(f'Total Balance:  {sum_value}')
            # st.info('Total Balance:  {:,.2f}'.format(W3_Exp['data']['Balance'].sum()))
        with c4:
            st.header("Revenue")
            W3_SP = Grid(w3_REV[["Vendor", "Account", "Amount"]], key='W3_SP', h=200, p=False)
            sum_value = format_num('str', (W3_SP['data']['Amount']).sum())
            st.info(f'Total Balance:  {sum_value}')
#####################################