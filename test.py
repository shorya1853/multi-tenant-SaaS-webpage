import getpass, imaplib
import email
import imaplib
import email
from email.header import decode_header
import boto3
from botocore.exceptions import NoCredentialsError
from io import BytesIO


M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
# M.login(getpass.getuser(), getpass.getpass())
email_add = "t15008278@gmail.com"
# password = "rpgg xllc ogbr xyzn"
password = "tpqf umkx sqll thci"
M.login(email_add, password)
M.select()
typ, data = M.search(None, 'UNSEEN')
s3 = boto3.client('s3')
for num in data[0].split():
    _, data = M.fetch(num, '(RFC822)')
    
    message = email.message_from_bytes(data[0][1])

    for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is not None:
                    # Get attachment data
                    attachment_data = BytesIO(part.get_payload(decode=True))

                    # Extract filename from header
                    filename, encoding = decode_header(part.get_filename())[0]
                    if isinstance(filename, bytes):
                        filename = filename.decode(encoding or 'utf-8')

                    # Upload attachment to S3
                    try:
                        print('reached')
                        s3.upload_fileobj(attachment_data, 'csvconverted123', filename)
                        print(f'Attachment "{filename}" uploaded to S3 successfully.')
                    except NoCredentialsError:
                        print('Credentials not available.')

M.close()
M.logout()