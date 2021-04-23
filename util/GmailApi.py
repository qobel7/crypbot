import smtplib
import time
import imaplib
import email
import traceback

# If modifying these scopes, delete the file token.json.


class GmailApi:
    ORG_EMAIL = "@gmail.com"
    FROM_EMAIL = "your_email"
    FROM_PWD = "your-password"
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993



    def __init__(self, mailAddress, mailPassword):
        self.FROM_EMAIL = mailAddress + self.ORG_EMAIL
        self.FROM_PWD = mailPassword
    def test(self):
        print(self.FROM_PWD)
    def read_email_from_gmail(self):
        try:
            mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
            mail.login(self.FROM_EMAIL,self.FROM_PWD)
            mail.select('inbox')

            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()
            latest_email_id = int(id_list[-1])
            data = mail.fetch(str(latest_email_id), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    Message_ID = msg['Message-ID']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    # for i in msg:
                    #     print('msg : ' + i + '\n')
                    #print('data:',msg)
            mail.store(str(latest_email_id),  "+FLAGS", "\\Deleted")
            mail.expunge()
            # close the mailbox
            mail.close()
            # logout from the account
            mail.logout()
            return msg
        except Exception as e:
            #traceback.print_exc()
            print("Mail bulunamadı,Alarm Yok")
    


