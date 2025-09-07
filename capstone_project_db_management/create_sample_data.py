import pandas as pd
from datetime import datetime, timedelta
import random

main_db_data = {
    'Customer ID': ['CUST001', 'CUST002', 'CUST003', 'CUST004', 'CUST005', 
                    'CUST006', 'CUST007', 'CUST008', 'CUST009', 'CUST010',
                    'CUST011', 'CUST012', 'CUST013', 'CUST014', 'CUST015',
                    'CUST016', 'CUST017', 'CUST018', 'CUST019', 'CUST020'],
    'Customer Name': ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Lisa Chen', 'David Brown',
                      'Emma Davis', 'Alex Kumar', 'Rachel Green', 'Tom Anderson', 'Maya Patel',
                      'James Lee', 'Nina Rodriguez', 'Kevin Zhang', 'Sophie Miller', 'Ryan Taylor',
                      'Isabella Martinez', 'Oliver Harris', 'Charlotte Clark', 'Lucas Walker', 'Mia Thompson'],
    'Email': ['john.smith@email.com', 'sarah.j@company.com', 'mike.wilson@startup.in', 
              'lisa.chen@tech.com', 'd.brown@business.co', 'emma.davis@corp.in',
              'alex.kumar@startup.com', 'rachel.g@email.com', 'tom.anderson@biz.in',
              'maya.patel@tech.co.in', 'james.lee@enterprise.com', 'nina.r@digital.io',
              'kevin.zhang@cloud.net', 'sophie.m@design.co', 'ryan.taylor@media.in',
              'isabella.m@ecomm.com', 'oliver.h@consulting.org', 'charlotte.c@finance.io',
              'lucas.w@health.tech', 'mia.t@education.net'],
    'Phone': [f'+91-98765432{i:02d}' for i in range(10, 30)],
    'Service Type': ['Web Development', 'Digital Marketing', 'App Development', 'SEO Services', 'Consulting',
                     'Website Redesign', 'Mobile App', 'Social Media', 'E-commerce', 'Cloud Services',
                     'Data Analytics', 'UI/UX Design', 'Content Writing', 'Video Production', 'Branding',
                     'API Development', 'Database Design', 'Security Audit', 'Performance Optimization', 'Training'],
    'Amount Due': [25000, 15000, 45000, 8000, 35000, 22000, 55000, 12000, 38000, 28000,
                   42000, 18000, 9500, 32000, 16000, 48000, 26000, 34000, 19000, 11000],
    'Due Date': ['2025-09-05', '2025-09-10', '2025-08-28', '2025-09-15', '2025-09-03',
                 '2025-09-12', '2025-08-30', '2025-09-20', '2025-09-08', '2025-09-18',
                 '2025-09-07', '2025-09-14', '2025-09-22', '2025-09-11', '2025-09-16',
                 '2025-09-09', '2025-09-13', '2025-09-19', '2025-09-06', '2025-09-21'],
    'User Status': ['unprocessed', 'reminded', 'followed_up', 'unprocessed', 'reminded',
                    'unprocessed', 'followed_up', 'unprocessed', 'reminded', 'unprocessed',
                    'reminded', 'followed_up', 'unprocessed', 'reminded', 'unprocessed',
                    'followed_up', 'reminded', 'unprocessed', 'followed_up', 'unprocessed'],
    'Last Contact': ['2025-08-30', '2025-09-02', '2025-09-01', '2025-08-25', '2025-08-28',
                     '2025-08-20', '2025-08-29', '2025-08-15', '2025-09-01', '2025-08-22',
                     '2025-09-03', '2025-09-04', '2025-08-18', '2025-09-05', '2025-08-27',
                     '2025-09-02', '2025-08-31', '2025-08-24', '2025-09-01', '2025-08-19'],
    'Payment Status': ['pending', 'pending', 'overdue', 'pending', 'pending',
                       'pending', 'overdue', 'pending', 'pending', 'pending',
                       'pending', 'pending', 'pending', 'overdue', 'pending',
                       'overdue', 'pending', 'pending', 'overdue', 'pending'],
    'Follow Up Required': ['yes', 'yes', 'no', 'yes', 'yes', 
                          'yes', 'no', 'yes', 'yes', 'yes',
                          'yes', 'no', 'yes', 'no', 'yes',
                          'no', 'yes', 'yes', 'no', 'yes']
}

sample_upload_data = {
    'Customer ID': ['CUST021', 'CUST022', 'CUST023', 'CUST024', 'CUST025'],
    'Customer Name': ['Andrew Martinez', 'Julia Roberts', 'Chris Evans', 'Emma Watson', 'Robert Lee'],
    'Email': ['andrew.m@tech.start', 'julia.r@creative.co', 'chris.e@enterprise.io', 
              'emma.w@digital.net', 'robert.l@cloud.tech'],
    'Phone': [f'+91-98765432{i:02d}' for i in range(30, 35)],
    'Service Type': ['Machine Learning', 'Graphic Design', 'DevOps', 'Content Strategy', 'Blockchain'],
    'Amount Due': [65000, 24000, 38000, 15000, 72000],
    'Due Date': ['2025-09-25', '2025-09-28', '2025-10-01', '2025-10-05', '2025-10-08'],
    'User Status': ['unprocessed', 'unprocessed', 'unprocessed', 'unprocessed', 'unprocessed'],
    'Last Contact': ['2025-09-06', '2025-09-06', '2025-09-07', '2025-09-07', '2025-09-08'],
    'Payment Status': ['pending', 'pending', 'pending', 'pending', 'pending'],
    'Follow Up Required': ['yes', 'yes', 'yes', 'yes', 'yes']
}

df_main = pd.DataFrame(main_db_data)
df_main.to_excel('capstone_project_db_management/database.xlsx', index=False)
print("Created database.xlsx with 20 records")

df_sample = pd.DataFrame(sample_upload_data)
df_sample.to_excel('capstone_project_db_management/sample_upload.xlsx', index=False)
print("Created sample_upload.xlsx with 5 records")

print("\nDatabase preview:")
print(df_main.head())
print(f"\nTotal database records: {len(df_main)}")

print("\nSample upload preview:")
print(df_sample)
print(f"\nTotal sample records: {len(df_sample)}")