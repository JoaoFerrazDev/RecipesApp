# observers/email_observer.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailObserver:
    def __init__(self, email_address, smtp_server, smtp_port, smtp_username, smtp_password):
        self.email_address = email_address
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def update(self, recipe):
        self.send_email(recipe)

    def send_email(self, recipe):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = self.email_address
        msg['Subject'] = 'New Recipe Added'

        body = f"Title: {recipe.title}\nIngredients: {recipe.ingredients}\nInstructions: {recipe.instructions}"
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.smtp_username, self.email_address, text)
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
