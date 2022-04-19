######
from data_processing import BG_W3, W3
from data_processing import Actual, period, sum_budget, plot_line, period_actual
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