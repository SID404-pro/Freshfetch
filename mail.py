import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Helper function to send email after registration
def send_registration_email(user_name, user_email, user_password):
    sender_email = "freshfetch@gmail.com"  # Replace with your Gmail email address
    sender_password = "SIDDHANt12*"  # Replace with your Gmail app-specific password

    receiver_email = user_email
    subject = "Registration Successful"
    
    # Personalized body content
    body = f"""
    Hello {user_name},

    Thank you for registering with us!

    Your registration was successful. Here are your account details:
    
    Email: {user_email}
    Password: {user_password}  # Note: Sending passwords in emails is not secure. Consider another method in production!

    We appreciate your registration, and we look forward to having you as a part of our platform.

    Best regards,
    Farmer Vendor Transport Management System
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Login with your Gmail credentials
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)  # Send email
        server.quit()  # Logout from the SMTP server
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
