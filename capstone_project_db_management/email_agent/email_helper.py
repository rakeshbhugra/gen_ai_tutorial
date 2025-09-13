import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class EmailHelper:
    def __init__(self, email_address: str = None, password: str = None):
        """
        Initialize EmailHelper with credentials.
        
        Args:
            email_address: Gmail address (defaults to env variable)
            password: App password for Gmail (defaults to env variable)
        """
        self.email_address = email_address or os.getenv("EMAIL_ADDRESS", "rakeshkbhugra@gmail.com")
        self.password = password or os.getenv("EMAIL_APP_PASSWORD")
        
        if not self.password:
            raise ValueError("Email password not provided. Set EMAIL_APP_PASSWORD in .env file")
        
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
    
    def send_email(self, 
                   to_email: str, 
                   subject: str, 
                   body: str, 
                   cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None,
                   html: bool = False) -> bool:
        """
        Send an email using Gmail SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text or HTML)
            cc: List of CC recipients
            bcc: List of BCC recipients
            html: Whether body is HTML content
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.email_address
            message["To"] = to_email
            message["Subject"] = subject
            
            if cc:
                message["Cc"] = ", ".join(cc)
            
            # Attach body
            content_type = "html" if html else "plain"
            message.attach(MIMEText(body, content_type))
            
            # Combine all recipients
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            # Connect and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.password)
                server.send_message(message, to_addrs=recipients)
            
            print(f"✅ Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Authentication failed. Check your email and app password.")
            return False
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def read_emails(self, 
                    folder: str = "INBOX", 
                    limit: int = 10,
                    unread_only: bool = False,
                    search_criteria: Optional[str] = None) -> List[Dict]:
        """
        Read emails from Gmail using IMAP.
        
        Args:
            folder: Email folder to read from (INBOX, Sent, etc.)
            limit: Maximum number of emails to retrieve
            unread_only: Only fetch unread emails
            search_criteria: Custom IMAP search criteria
            
        Returns:
            List of email dictionaries with subject, from, date, and body
        """
        emails = []
        
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.password)
            mail.select(folder)
            
            # Build search criteria
            if search_criteria:
                criteria = search_criteria
            elif unread_only:
                criteria = 'UNSEEN'
            else:
                criteria = 'ALL'
            
            # Search for emails
            _, messages = mail.search(None, criteria)
            email_ids = messages[0].split()
            
            # Get the latest emails up to limit
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            email_ids.reverse()  # Most recent first
            
            for email_id in email_ids:
                _, msg = mail.fetch(email_id, '(RFC822)')
                
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        
                        # Extract email details
                        email_data = {
                            'id': email_id.decode(),
                            'subject': msg['subject'],
                            'from': msg['from'],
                            'to': msg['to'],
                            'date': msg['date'],
                            'body': self._get_email_body(msg)
                        }
                        
                        emails.append(email_data)
            
            mail.close()
            mail.logout()
            
            print(f"✅ Retrieved {len(emails)} emails from {folder}")
            return emails
            
        except Exception as e:
            print(f"❌ Failed to read emails: {e}")
            return []
    
    def _get_email_body(self, msg) -> str:
        """Extract body from email message."""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                elif content_type == "text/html" and not body:
                    # Fallback to HTML if no plain text
                    html_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    # Simple HTML stripping (you might want to use BeautifulSoup for better results)
                    import re
                    body = re.sub('<[^<]+?>', '', html_body)
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return body.strip()
    
    def mark_as_read(self, email_ids: List[str], folder: str = "INBOX") -> bool:
        """
        Mark emails as read.
        
        Args:
            email_ids: List of email IDs to mark as read
            folder: Email folder
            
        Returns:
            True if successful
        """
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.password)
            mail.select(folder)
            
            for email_id in email_ids:
                mail.store(email_id, '+FLAGS', '\\Seen')
            
            mail.close()
            mail.logout()
            
            print(f"✅ Marked {len(email_ids)} emails as read")
            return True
            
        except Exception as e:
            print(f"❌ Failed to mark emails as read: {e}")
            return False
    
    def delete_emails(self, email_ids: List[str], folder: str = "INBOX") -> bool:
        """
        Delete emails (move to trash).
        
        Args:
            email_ids: List of email IDs to delete
            folder: Email folder
            
        Returns:
            True if successful
        """
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.password)
            mail.select(folder)
            
            for email_id in email_ids:
                mail.store(email_id, '+FLAGS', '\\Deleted')
            
            mail.expunge()
            mail.close()
            mail.logout()
            
            print(f"✅ Deleted {len(email_ids)} emails")
            return True
            
        except Exception as e:
            print(f"❌ Failed to delete emails: {e}")
            return False
    
    def search_emails(self, 
                      keyword: str, 
                      folder: str = "INBOX",
                      in_subject: bool = True,
                      in_body: bool = True,
                      from_address: Optional[str] = None) -> List[Dict]:
        """
        Search for emails containing specific keywords.
        
        Args:
            keyword: Keyword to search for
            folder: Email folder to search in
            in_subject: Search in subject
            in_body: Search in body
            from_address: Filter by sender
            
        Returns:
            List of matching emails
        """
        criteria_parts = []
        
        if in_subject:
            criteria_parts.append(f'SUBJECT "{keyword}"')
        if in_body:
            criteria_parts.append(f'BODY "{keyword}"')
        if from_address:
            criteria_parts.append(f'FROM "{from_address}"')
        
        # IMAP OR syntax for multiple criteria
        if len(criteria_parts) > 1:
            criteria = f'OR {" ".join(criteria_parts)}'
        else:
            criteria = criteria_parts[0] if criteria_parts else 'ALL'
        
        return self.read_emails(folder=folder, search_criteria=criteria)