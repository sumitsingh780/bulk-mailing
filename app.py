from flask import Flask, request, jsonify, render_template
import yagmail
import pandas as pd
import os
import time
import threading

app = Flask(__name__)

# Make sure the 'uploads' folder exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html is in a 'templates' folder

def send_bulk_emails(sender_email, sender_password, file_path, email_subject, email_body):
    try:
        data = pd.read_excel(file_path)

        # Remove duplicate emails
        data = data.drop_duplicates(subset='Email')

        # Setup Yagmail client
        yag = yagmail.SMTP(user=sender_email, password=sender_password, host="smtp.gmail.com", port=465, smtp_ssl=True)

        sent_emails = set()

        for index, row in data.iterrows():
            recipient_email = row['Email']
            if pd.isna(recipient_email) or recipient_email.strip() == '':
                continue

            # Avoid sending to the same email twice
            if recipient_email in sent_emails:
                continue

            # Send the email
            yag.send(
                to=recipient_email,
                subject=email_subject,
                contents=email_body
            )

            sent_emails.add(recipient_email)
            print(f"Sent to: {recipient_email}")

            # Delay to avoid spam filters
            time.sleep(5)

        print("✅ All emails sent successfully!")

    except Exception as e:
        print("❌ Error during email sending:", e)

@app.route('/send-emails', methods=['POST'])
def send_emails():
    try:
        sender_email = request.form['senderEmail']
        sender_password = request.form['senderPassword']
        email_file = request.files['emailFile']
        email_subject = request.form['emailSubject']
        email_body = request.form['emailBody']

        # Save uploaded file
        file_path = os.path.join('uploads', email_file.filename)
        email_file.save(file_path)

        # Start email sending in background thread
        thread = threading.Thread(target=send_bulk_emails, args=(sender_email, sender_password, file_path, email_subject, email_body))
        thread.start()

        return jsonify({'message': '✅ Emails are being sent in the background!'}), 200

    except Exception as e:
        return jsonify({'message': f'❌ Failed to start email process: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
