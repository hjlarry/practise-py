import smtplib
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os


main_msg = MIMEMultipart()
# Create the message
msg = MIMEText('内容中可以有中文,<b>哈哈</b>')
main_msg.attach(msg)

part = MIMEApplication(open('tags.csv','rb').read())
part.add_header('Content-Disposition', 'attachment', filename="tags.csv")
main_msg.attach(part)


main_msg['To'] = email.utils.formataddr(('Recipient',
                                    'recipient@example.com'))
main_msg['From'] = email.utils.formataddr(('Author',
                                      'author@example.com'))
main_msg['Subject'] = 'Simple test message'

# server = smtplib.SMTP('smtp.qq.com', 587)
# server.set_debuglevel(True)  # show communication with the server
# server.starttls()
# server.login('14653858@qq.com', 'prsiimeknnnrbija')
# try:
#     server.sendmail('14653858@qq.com',
#                     ['3015644@qq.com'],
#                     main_msg.as_string())
# finally:
#     server.quit()
print(os.environ.items())
import dbm.ndbm