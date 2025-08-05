from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os
import datetime
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    logging.debug("Received POST request to /generate-pdf")
    data = request.get_json()
    logging.debug(f"Request data: {data}")
    title = data['title']
    email = data['email']
    items = data['items']
    
    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Chipfuwa Civil and Construction", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, txt=title, ln=True, align="C")
    pdf.ln(10)

    # Details
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Issuer: Max", ln=True)
    pdf.cell(0, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S SAST')}", ln=True)
    pdf.cell(0, 10, txt=f"Bill To: {email}", ln=True)
    pdf.ln(10)

    # Table Header
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Description", 1, 0, "C", 1)
    pdf.cell(45, 10, "Price", 1, 0, "C", 1)
    pdf.cell(45, 10, "Quantity", 1, 1, "C", 1)

    # Table Content
    pdf.set_font("Arial", "", 12)
    pdf.set_fill_color(255, 255, 255)
    total = 0
    for item in items:
        price = float(item['price'])
        qty = 1  # Default quantity
        line_total = price * qty
        total += line_total 
        pdf.cell(100, 10, item['description'], 1, 0, "L", 1)
        pdf.cell(45, 10, f"R{price:.2f}", 1, 0, "C", 1)  # Changed $ to R
        pdf.cell(45, 10, str(qty), 1, 1, "C", 1)

    # VAT and Total
    vat = total * 0.15
    final_total = total + vat
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(145, 10, "Subtotal", 1, 0, "R", 1)
    pdf.cell(45, 10, f"R{total:.2f}", 1, 1, "C", 1)  # Changed $ to R
    pdf.cell(145, 10, "VAT (15%)", 1, 0, "R", 1)
    pdf.cell(45, 10, f"R{vat:.2f}", 1, 1, "C", 1)  # Changed $ to R
    pdf.cell(145, 10, "Total", 1, 0, "R", 1)
    pdf.cell(45, 10, f"R{final_total:.2f}", 1, 1, "C", 1)  # Changed $ to R

    # Save PDF
    pdf_file = f"{title.lower().replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(pdf_file)
    logging.debug(f"PDF saved as {pdf_file}")

    # Send Email with error handling
    sender_email = "USER_EMAIL_ADDRESS"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = f"{title} from COMPANY NAME"
    msg.attach(MIMEText(f"Attached is your {title} from Chipfuwa Civil and Construction.\n\nRegards, Maxwell", 'plain'))  # Added Regards, Maxwell
    with open(pdf_file, 'rb') as f:
        part = MIMEApplication(f.read(), Name=pdf_file)
        part['Content-Disposition'] = f'attachment; filename="{pdf_file}"'
        msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, "PASSWORD")  # Replace with Special 2FA from gmail
            logging.debug(f"Sending email to {email}")
            server.send_message(msg)
            logging.debug(f"Email sent to {email}")
    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication failed. Check your email or App Password.")
        os.remove(pdf_file)
        return jsonify({"message": "Authentication failed. Check your email or App Password."}), 401
    except Exception as e:
        logging.error(f"SMTP Error: {str(e)}")
        os.remove(pdf_file)
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

    os.remove(pdf_file)
    return jsonify({"message": "PDF sent successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
