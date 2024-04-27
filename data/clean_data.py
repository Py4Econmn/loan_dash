import pandas as pd
import datetime as dt

# amount by branch
df = pd.read_csv('sample_loan_2309.csv')

df['IssueMonth'] = pd.to_datetime(df.IssueDate).dt.month
df['IssueYear'] = pd.to_datetime(df.IssueDate).dt.year
df['IssueYM'] = pd.to_datetime(df['IssueDate']).dt.strftime('%Y-%m')


df1 = df.groupby(['Branch','IssueYM'])['Amount'].sum().reset_index()
df1.to_csv('amount_branch_ym.csv')

# outstanding
df = pd.read_csv('sample_loan_2308.csv')
df.reset_index(inplace=True)
df.rename(columns={'index': 'loanid'},inplace=True)

# Convert "Loan Start Date" to datetime
df['IssueDate'] = pd.to_datetime(df['IssueDate'])
df['DueDate'] = pd.to_datetime(df['DueDate'])
df['duration'] = (df['DueDate'].dt.year - df['IssueDate'].dt.year) * 12 + (df['DueDate'].dt.month - df['IssueDate'].dt.month)

# Create an empty DataFrame to store the outstanding amounts over time
outstanding_df = pd.DataFrame(columns=["loanid","month","amount"])


# Iterate through each loan
for _, row in df.iterrows():
    loanid = row['loanid']
    loan_amount = row['Amount']
    issueDate = row['IssueDate']
    dueDate = row['DueDate']
    current_date = dt.date.today() + pd.DateOffset(months=-month)
   
    if dueDate < current_date:
        continue

    for month in range(12):
        # # Calculate the interest payment for the current month
        # interest_payment = outstanding_amount * interest_rate / 12

        # # Calculate the principal payment for the current month
        # principal_payment = (loan_amount / loan_term_months) - interest_payment

        # # Update the outstanding amount
        # outstanding_amount -= principal_payment

        # Add the data to the outstanding_df
        last_day_of_month = current_date + pd.offsets.MonthEnd(0)
        outstanding_df = outstanding_df.append({
            "loanid": loanid,
            "month": last_day_of_month,
            "amount": loan_amount
        }, ignore_index=True)

        # Move to the next month
        current_date = current_date + pd.DateOffset(months=1)

# Display the outstanding amounts over time
print(outstanding_df)

outstanding_df.to_csv('outstanding_2308.csv')