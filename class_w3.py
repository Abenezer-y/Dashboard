######
from data_processing import BG_W3, W3
from data_processing import Actual, period, sum_budget, plot_line, period_actual, format_num
######

# Plans
budget_w3 = BG_W3
w3_planned = sum_budget(budget_w3)

# Import Class Revenue and Expenses 
w3 = W3
w3_COGS = w3[w3['Type']=="Expense"]
w3_REV = w3[w3['Type']=="Revenue"]

# Actual COGS and Revenue
if w3_REV['Amount'].sum() > 0:
    w3_rev = Actual(w3_REV)


w3_cogs = Actual(w3_COGS)


# Draw Plot and Update Budget
w3_fig = plot_line(period, planned=w3_planned, title="Financial Performace for W3", rev=None, cogs=w3_cogs)
budget_w3 = period_actual(budget_w3, w3_REV, w3_COGS, period)
budget_w3['Q1 TOTAL'] = budget_w3['Q1 TOTAL'].map(lambda Amount: format_num("str", Amount))
budget_w3['Q1 Actual'] = budget_w3['Q1 Actual'].map(lambda Amount: format_num("str",Amount))
budget_w3['Q2 TOTAL'] = budget_w3['Q2 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_w3['Q2 Actual'] = budget_w3['Q2 Actual'].map(lambda Amount: format_num("str",Amount))
budget_w3['Q3 TOTAL'] = budget_w3['Q3 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_w3['Q4 TOTAL'] = budget_w3['Q4 TOTAL'].map(lambda Amount: format_num("str",Amount))
budget_w3['Yearly'] = budget_w3['Yearly'].map(lambda Amount: format_num("str",Amount))
budget_w3['YTD Actual'] = budget_w3['YTD Actual'].map(lambda Amount: format_num("str",Amount))