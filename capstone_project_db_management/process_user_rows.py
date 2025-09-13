'''
1. Read the database

2. Iterate over each row

3. check tags

4. based on tags
    1. if tag == "unprocessed":
        trigger the email flow
        update status
        
    2. if tag == "followed_up":
        trigger the follow up flow
        update status
        
    3. if tag == "reminded":
        notify human

'''


import pandas as pd
from email_agent.email_helper import EmailHelper

def update_status_in_db(customer_id, new_status):
    print(f"Updating customer {customer_id} to status {new_status}")
    
    file_path = "capstone_project_db_management/database.xlsx"
    df = pd.read_excel(file_path)

    df.loc[df['Customer ID'] == customer_id, 'User Status'] = new_status

    # write updated file back to excel sheet

    df.to_excel(file_path, index=False)

    print("Updated Tag")
    return

def triggering_unprocessed_flow():
    print("triggering unprocessed flow")

def triggering_reminder_flow():
    print("triggering reminder flow")

def notifying_human(customer_name, customer_id, amount_due, email, phone):
    # send email to human that this user needs attention
    receiver = "rakeshkbhugra@gmail.com"

    subject = f"Customer {customer_name} needs attention"

    body = f"""
    Customer {customer_name} with ID {customer_id} has an amount due of {amount_due}.
    Please reach out to them at email: {email} or phone: {phone}.
    """
    
    email_helper = EmailHelper()
    email_helper.send_email(to_email=receiver, subject=subject, body=body)

    # update tag to "notified_human"
    update_status_in_db(customer_id, "notified_human")
    
if __name__ == "__main__":
    file_path = "capstone_project_db_management/database.xlsx"
    df = pd.read_excel(file_path)

    print(df.head())

    print(df.columns)

    for idx, row in df.iterrows():
        user_status = row['User Status']
        print(row['Customer Name'], user_status)

        if user_status == "unprocessed":
            triggering_unprocessed_flow()

        elif user_status == "reminded":
            triggering_reminder_flow()

        elif user_status == "followed_up":
            notifying_human(
                row["Customer Name"], 
                row["Customer ID"], 
                row["Amount Due"], 
                row["Email"], 
                row["Phone"]
            )


        elif user_status == "notified_human":
            print("Human already notified, waiting for action")

        else:
            raise ValueError(f"Unknown user status: {user_status}")

        print("-"*40)