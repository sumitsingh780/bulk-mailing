from flask import Flask, request, jsonify, render_template
import yagmail
import pandas as pd
import os
import time  # Import time module for the delay

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html is in a 'templates' folder

@app.route('/send-emails', methods=['POST'])
def send_emails():
    sender_email = request.form['senderEmail']
    sender_password = request.form['senderPassword']
    email_file = request.files['emailFile']
    email_subject = request.form['emailSubject']
    email_body = request.form['emailBody']

    # Save the uploaded file
    file_path = os.path.join('uploads', email_file.filename)
    email_file.save(file_path)

    try:
        data = pd.read_excel(file_path)

        # Use App Password instead of the regular Gmail password
        yag = yagmail.SMTP(user=sender_email, password=sender_password, host="smtp.gmail.com", port=465, smtp_ssl=True)

        for index, row in data.iterrows():
            recipient_email = row['Email']
            if pd.isna(recipient_email) or recipient_email.strip() == '':
                continue

            # Send the email to the recipient
            yag.send(
                to=recipient_email,
                subject=email_subject,
                contents=email_body
            )

            # Add a 3-second delay between emails to prevent being flagged as spam
            time.sleep(5)

        return jsonify({'message': 'Emails sent successfully!'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
