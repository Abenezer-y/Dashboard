######
import pandas as pd
import datetime
from data_processing import BG_GnA, GENERAL, VOICE_NA, VOICE21, CREDITS
from data_processing import Actual, period, sum_budget, plot_line, period_actual, Account_Balance, format_num
######

# Plans
budget_gna = BG_GnA
gna_planned = sum_budget(budget_gna)

# Import Class Revenue and Expenses 
gna = GENERAL
V_NA = VOICE_NA
V21 = VOICE21
gna_COGS = gna[gna['Type']=="Expense"]
gna_REV = gna[gna['Type']=="Revenue"]

gna['Date'] = pd.to_datetime(gna['Date'])

gna_rev = None
if gna_REV['Amount'].sum() > 0:
    gna_rev = Actual(gna_REV)

# Actual COGS and Revenue
gna_cogs = Actual(gna_COGS)
V_NA_cogs = Actual(V_NA)
V21_cogs = Actual(V21)


cols = ["Account", "Q1 TOTAL", "Q2 TOTAL", "Q3 TOTAL", "Q4 TOTAL", "Yearly"]
# budget_gna = budget_gna

Q1_DF = Account_Balance(gna[gna["Date"]<=period[1]])
Q2_DF = Account_Balance(gna[(gna["Date"]>period[1]) & (gna["Date"]<=period[2])])

V_NA_DF = Account_Balance(V_NA)
V21_DF = Account_Balance(V21)
df_gen = pd.concat([Q1_DF, Q2_DF, V_NA_DF, V21_DF])

def Account_Balance_GnA(df):
    df['Q1 TOTAL'] =  df['Q1 TOTAL'].astype(str)
    df['Q1 TOTAL'] = df['Q1 TOTAL'].map(lambda Amount: float(Amount.replace(",", "")))
    df['Q2 TOTAL'] =  df['Q2 TOTAL'].astype(str)
    df['Q2 TOTAL'] = df['Q2 TOTAL'].map(lambda Amount: float(Amount.replace(",", "")))
    df['Q3 TOTAL'] =  df['Q3 TOTAL'].astype(str)
    df['Q3 TOTAL'] = df['Q3 TOTAL'].map(lambda Amount: float(Amount.replace(",", "")))
    df['Q4 TOTAL'] =  df['Q4 TOTAL'].astype(str)
    df['Q4 TOTAL'] = df['Q4 TOTAL'].map(lambda Amount: float(Amount.replace(",", "")))
    df['Yearly'] =  df['Yearly'].astype(str)
    df['Yearly'] = df['Yearly'].map(lambda Amount: float(Amount.replace(",", "")))

    accounts = df['Account'].unique()
    dict_df = {'Account': [], "Q1 TOTAL": [], "Q1 Actual": [], "Q2 TOTAL": [], "Q2 Actual": [], "Q3 TOTAL": [], "Q4 TOTAL": [], "Yearly": [], "YTD Actual": []}
    for acc in accounts:
        dict_df['Account'].append(acc) 
        dict_df['Q1 TOTAL'].append(round(df[df['Account']==acc]['Q1 TOTAL'].sum(), 2)) 
        dict_df['Q1 Actual'].append(round(Q1_DF[Q1_DF['Account']==acc]['Balance'].sum(), 2)) 
        dict_df['Q2 TOTAL'].append(round(df[df['Account']==acc]['Q2 TOTAL'].sum(), 2)) 
        dict_df['Q2 Actual'].append(round(Q2_DF[Q2_DF['Account']==acc]['Balance'].sum(), 2)) 
        dict_df['Q3 TOTAL'].append(round(df[df['Account']==acc]['Q3 TOTAL'].sum(), 2)) 
        dict_df['Q4 TOTAL'].append(round(df[df['Account']==acc]['Q4 TOTAL'].sum(), 2)) 
        dict_df['Yearly'].append(round(df[df['Account']==acc]['Yearly'].sum(), 2))
        dict_df['YTD Actual'].append(round((Q1_DF[Q1_DF['Account']==acc]['Balance'].sum()+Q2_DF[Q2_DF['Account']==acc]['Balance'].sum()), 2))  
    acc_df = pd.DataFrame(dict_df)
    return acc_df

bdg_GnA = Account_Balance_GnA(budget_gna[cols])




def return_plan(df):
    x = df['Q1 TOTAL'].sum()
    y = x + df['Q2 TOTAL'].sum()
    z = y + df['Q3 TOTAL'].sum()
    w = z + df['Q4 TOTAL'].sum()
    budgets = [0, x, y, z, w]
    return (None, budgets)

period = [datetime.datetime(2022,1,1), datetime.datetime(2022,3,31), datetime.datetime(2022,6,30), datetime.datetime(2022,9,30), datetime.datetime(2022,12,31)]
gna_planned = return_plan(bdg_GnA)

# gna_planned = sum_budget(bdg_GnA)
# Draw Plot and Update Budget
gna_fig = plot_line(period, planned=gna_planned, title="Financial Performace General and Admin", rev=gna_rev, cogs=gna_cogs)
# budget_gna = period_actual(budget_gna, gna_REV, gna_COGS, period)
# Online Services

Online_Services = ["99DESIGNS.COM", "CLICKUP", "GETCLOUDAPP.COM", "MICROSOFT", "PARCEL PLUS", "RIVERSIDE.FM", "ADDEVENT.COM", "ADOBE ACROPRO", "ADOBE CREATIVE CLOUDSAN", "BILL COM INC", "BLUESNAP US", "CIS*", 
"CUE HEALTH INC.", "DEPOSITFIX", "DISCORD", "HOSTMONSTER.COM", "EPIDEMIC SOUND", "EXPEDIA.COM", "GODADDY.COM", "GOOGLE*", "HEADLINER", "HUBSPOT INC.", "INTUIT PAYROLL", "INTUIT QUICKBOOKS", "LINKEDIN", 
"OTTER.AI", "PADDLE.NET", "PANDADOC", "SMARTSHEET", "STREAMYARD.COM", "STRIPO.EMAIL", "UNSTOPPABLEDOMAINS.CLAS", "VENMO", "TWITTER.COM", "ZAPIER.COM", "ZOOM.US"]

Software_Subscriptions = ["KENNECTED.IO", "TAROKO.TECHNOLOGY"]

bank_Subscriptions = ["AUTHNET GATEWAY", "INDUSTRIOUS TECH"]
miscellaneous = ["AMERICAN AIRLINES", "BEST BUY", "AplPay HotelTonight", "DELTA AIR LINES", "FedEx", "HERTZ CAR RENTAL", "HOTELSCOM", "MICRO CENTER", "PARK MGM", "STARBUCKS", "Interest Charge", "RENT THE RUNWAY", "RENAISSANCE"]

labor = ["Hammerton Barca", "Madisyn Bozarth", "Stacy England"]

BANK_LABOR = ["GUSTO"]
credit_payment = ["MOBILE PAYMENT"]
UpWORK_PAYMENTS = ["UPWORK"]

# General = ["ADDEVENT.COM", "03", "26", 24]

bdg_GnA['Q1 TOTAL'] = bdg_GnA['Q1 TOTAL'].map(lambda Amount: format_num("str", Amount))
bdg_GnA['Q1 Actual'] = bdg_GnA['Q1 Actual'].map(lambda Amount: format_num("str",Amount))
bdg_GnA['Q2 TOTAL'] = bdg_GnA['Q2 TOTAL'].map(lambda Amount: format_num("str",Amount))
bdg_GnA['Q2 Actual'] = bdg_GnA['Q2 Actual'].map(lambda Amount: format_num("str",Amount))
bdg_GnA['Q3 TOTAL'] = bdg_GnA['Q3 TOTAL'].map(lambda Amount: format_num("str",Amount))
bdg_GnA['Q4 TOTAL'] = bdg_GnA['Q4 TOTAL'].map(lambda Amount: format_num("str",Amount))
bdg_GnA['Yearly'] = bdg_GnA['Yearly'].map(lambda Amount: format_num("str",Amount))
bdg_GnA['YTD Actual'] = bdg_GnA['YTD Actual'].map(lambda Amount: format_num("str",Amount))