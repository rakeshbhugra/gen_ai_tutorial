from email_helper import EmailHelper
from dotenv import load_dotenv

load_dotenv()

def main():
    # Initialize email helper
    email_client = EmailHelper()
    
    print("=" * 50)
    print("Email Client Demo")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Send an email")
        print("2. Read recent emails")
        print("3. Read unread emails")
        print("4. Search emails")
        print("5. Send test email")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            # Send email
            to_email = input("To email: ")
            subject = input("Subject: ")
            body = input("Message: ")
            
            success = email_client.send_email(to_email, subject, body)
            if success:
                print("Email sent successfully!")
        
        elif choice == "2":
            # Read recent emails
            limit = input("How many emails to read? (default 5): ")
            limit = int(limit) if limit else 5
            
            emails = email_client.read_emails(limit=limit)
            
            for i, email_msg in enumerate(emails, 1):
                print(f"\n--- Email {i} ---")
                print(f"From: {email_msg['from']}")
                print(f"Subject: {email_msg['subject']}")
                print(f"Date: {email_msg['date']}")
                print(f"Body preview: {email_msg['body'][:100]}...")
        
        elif choice == "3":
            # Read unread emails
            emails = email_client.read_emails(unread_only=True, limit=10)
            
            if emails:
                for i, email_msg in enumerate(emails, 1):
                    print(f"\n--- Unread Email {i} ---")
                    print(f"From: {email_msg['from']}")
                    print(f"Subject: {email_msg['subject']}")
                    print(f"Body preview: {email_msg['body'][:100]}...")
                
                # Ask if user wants to mark as read
                mark_read = input("\nMark these as read? (y/n): ")
                if mark_read.lower() == 'y':
                    email_ids = [e['id'] for e in emails]
                    email_client.mark_as_read(email_ids)
            else:
                print("No unread emails found.")
        
        elif choice == "4":
            # Search emails
            keyword = input("Enter search keyword: ")
            from_address = input("From address (optional, press Enter to skip): ")
            
            results = email_client.search_emails(
                keyword=keyword,
                from_address=from_address if from_address else None
            )
            
            if results:
                print(f"\nFound {len(results)} matching emails:")
                for i, email_msg in enumerate(results, 1):
                    print(f"\n--- Result {i} ---")
                    print(f"From: {email_msg['from']}")
                    print(f"Subject: {email_msg['subject']}")
                    print(f"Body preview: {email_msg['body'][:100]}...")
            else:
                print("No matching emails found.")
        
        elif choice == "5":
            # Send test email
            test_email = email_client.email_address
            success = email_client.send_email(
                to_email=test_email,
                subject="Test Email from Python Email Client",
                body="This is a test email sent using the EmailHelper class.\n\nFeatures:\n- Send emails\n- Read emails\n- Search emails\n- Mark as read\n- Delete emails"
            )
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"Error: {e}")