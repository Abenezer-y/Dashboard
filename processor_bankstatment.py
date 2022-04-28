from data_processing import matcher_fun, BANK

bank = BANK

# 'ledger'
# ['Date', 'Name', 'Class', 'Account', 'Category', 'Method of Payment', 'Description', 'Amount']
pattern_names = ['AMEX', 'BILL.COM', 'CAPITAL_ONE', 'HEALTH_CARE',  'LOAN', 'PAYROLL', 'SERVICE_CHARGE', 'SUBSCRIPTION','USAA']


# BILL.COM
bill_pattern_0 = [{'LOWER': 'bill.com'}, {'IS_SPACE': True}, {'LOWER': 'payables'}]
bill_pattern_1 = [{'LOWER': 'payables'}, {'LOWER': 'bill.com'}]
bill_pattern_2 = [{'LOWER': 'busonline'}, {'LOWER': 'domestic'}, {'LOWER': 'wire'}]
bill_pattern = [bill_pattern_0, bill_pattern_1, bill_pattern_2]

# PAYROLL
tax_pattern = [{'LOWER': 'tax'}, {'IS_DIGIT': True}, {'LOWER': 'gusto'}]
tax_pattern_1 = [{'LOWER': 'gusto'}, {'IS_SPACE': True}, {'LOWER': 'tax'}]
net_pattern = [{'LOWER': 'gusto'}, {'IS_SPACE': True}, {'LOWER': 'net'}]
net_pattern_1 = [{'LOWER': 'net'}, {'IS_DIGIT': True}, {'LOWER': 'gusto'}]
fee_pattern = [{'LOWER': 'fee'}, {'IS_DIGIT': True}, {'LOWER': 'gusto'}]
fee_pattern_1 = [{'LOWER': 'gusto'}, {'IS_SPACE': True}, {'LOWER': 'fee'}]
payroll_pattern = [tax_pattern, tax_pattern_1, net_pattern, net_pattern_1, fee_pattern, fee_pattern_1]

# AMEX 
amex_pattern_0 = [{'LOWER': 'amex'}, {'LOWER': 'epayment'}]
amex_pattern = [amex_pattern_0]

# SUBSCRIPTION
authnet_pattern = [{'LOWER': 'authnet'}, {'LOWER': 'gateway'}]
industrious_pattern = [{'LOWER': 'industrious'}, {'LOWER': 'tech'}]
global_pattern = [{'LOWER': 'global'}, {'LOWER': 'payments'}]
subscription_pattern = [authnet_pattern, industrious_pattern, global_pattern]

# CAPITAL_ONE
cap_one_pattern_0 = [{'LOWER': 'capital'}, {'LOWER': 'one'}]
cap_one_pattern = [cap_one_pattern_0]

# LOAN
loan_pattern_0 = [{'LOWER': 'comm'}, {'LOWER': 'loans'}]
loan_pattern_1 = [{'LOWER': 'paypal'}]
loan_pattern_2 = [{'LOWER': 'truist'}, {'LOWER': 'bank'}, {'IS_SPACE': True}, {'LOWER': 'cl'}]
loan_pattern = [loan_pattern_0, loan_pattern_1, loan_pattern_2]
# LOAN = ['LOAN', loan_pattern]
# HEALTH_CARE
healthcare_pattern_0 = [{'LOWER': 'united'}, {'LOWER': 'healthcar'}]
healthcare_pattern =[healthcare_pattern_0]


# USAA
usaa_pattern_0 = [{'LOWER': 'usaa'}, {'LOWER': 'credit'}]
usaa_pattern_1 = [{'LOWER': 'usaa.com'}]
usaa_pattern = [usaa_pattern_0, usaa_pattern_1]

# SERVICE_CHARGE
intuit_pattern = [{'LOWER': 'tran'}, {'LOWER': 'fee'}, {'LOWER': 'intuit'}]
acc_maintenace = [{'LOWER': 'account'}, {'LOWER': 'analysis'}]
service_charge_pattern = [intuit_pattern, acc_maintenace]




AMEX_list = [("AMEX", amex_pattern)]
BILL_list = [("BILL.COM", bill_pattern)]
CAPITAL_ONE_list = [("CAPITAL_ONE", cap_one_pattern)]
HEALTH_CARE_list = [("HEALTH_CARE", healthcare_pattern)]
LOAN_list = [["LOAN", loan_pattern]]
PAYROLL_list = [("PAYROLL", payroll_pattern)]
SERVICE_CHARGE_list = [("SERVICE_CHARGE", service_charge_pattern)]
SUBSCRIPTION_list = [("SUBSCRIPTION", subscription_pattern)]
USAA_list = [("USAA", usaa_pattern)]



loan_df = matcher_fun(matcher_list = LOAN_list, data = bank, account="Loan")
loan_df['Vendor'] = ["Loan Builder" for i in range(loan_df.shape[0])] 
loan_df['Invoice Date'] = [ _ for _ in loan_df['Date']] 
loan_df['Due Date'] = [ _ for _ in loan_df['Date']]  
loan_df['Process Date'] = [ _ for _ in loan_df['Date']] 
loan_df['Status'] = ["paid" for i in range(loan_df.shape[0])] 