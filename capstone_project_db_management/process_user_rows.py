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

def triggering_unprocessed_flow():
    print("triggering unprocessed flow")

def triggering_reminder_flow():
    print("triggering reminder flow")

def notifying_human():
    print("notifying human")

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
            notifying_human()


        else:
            raise ValueError(f"Unknown user status: {user_status}")

        print("-"*40)