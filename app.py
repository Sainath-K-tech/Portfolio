from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # <-- must match renamed HTML file

@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    email_user = os.environ.get('EMAIL_USER')
    email_pass = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = f"🔔 New Contact Request - {subject}"
    msg['From'] = email_user
    msg['Reply-To'] = email
    msg['To'] = email_user
    
    # Plain text version
    text_content = f"""
╔══════════════════════════════════════════════════════════╗
║           NEW CONTACT REQUEST FROM PORTFOLIO             ║
╚══════════════════════════════════════════════════════════╝

📋 CONTACT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Name:        {name}
📧 Email:       {email}
📝 Subject:     {subject}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 MESSAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ Received: {__import__('datetime').datetime.now().strftime('%B %d, %Y at %I:%M %p')}

"""
    
    # HTML version for better formatting
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="margin: 0; font-size: 28px;">🔔 New Contact Request</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">From Your Portfolio Website</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-left: 4px solid #667eea; border-right: 4px solid #667eea;">
                <h2 style="color: #667eea; margin-top: 0; border-bottom: 2px solid #667eea; padding-bottom: 10px;">📋 Contact Details</h2>
                
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr>
                        <td style="padding: 12px; background: white; border: 1px solid #dee2e6; font-weight: bold; width: 30%;">
                            👤 Name
                        </td>
                        <td style="padding: 12px; background: white; border: 1px solid #dee2e6;">
                            {name}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 12px; background: white; border: 1px solid #dee2e6; font-weight: bold;">
                            📧 Email
                        </td>
                        <td style="padding: 12px; background: white; border: 1px solid #dee2e6;">
                            <a href="mailto:{email}" style="color: #667eea; text-decoration: none;">{email}</a>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 12px; background: white; border: 1px solid #dee2e6; font-weight: bold;">
                            📝 Subject
                        </td>
                        <td style="padding: 12px; background: white; border: 1px solid #dee2e6;">
                            {subject}
                        </td>
                    </tr>
                </table>
                
                <h2 style="color: #667eea; margin-top: 30px; border-bottom: 2px solid #667eea; padding-bottom: 10px;">💬 Message</h2>
                <div style="background: white; padding: 20px; border-radius: 5px; border: 1px solid #dee2e6; margin: 20px 0;">
                    <p style="margin: 0; white-space: pre-wrap; word-wrap: break-word;">{message}</p>
                </div>
            </div>
            
            <div style="background: #343a40; color: white; padding: 20px; border-radius: 0 0 10px 10px; text-align: center;">
                <p style="margin: 0; font-size: 14px;">
                    ⏰ Received on {__import__('datetime').datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                </p>
                <p style="margin: 10px 0 0 0; font-size: 12px; opacity: 0.8;">
                    Click reply to respond directly to {name}
                </p>
            </div>
        </body>
    </html>
    """
    
    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
        return redirect('/')
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
