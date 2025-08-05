Project Title: Invoice & Quotation Generator

A full-stack web application built with Python and Flask that enables users to create professional invoices or quotations in pdf format, and email them directly to clients. 
Designed for a Private contractor in Civil Engineering, this app streamlines billing processes with a user-friendly interface and robust backend functionality.

Features
Dynamic PDF Generation: Creates customizable invoices/quotations using FPDF, including itemized lists, VAT calculations, and professional formatting.
Email Integration: Sends generated PDFs to clients via SMTP (Gmail) with secure credential handling using environment variables.
Interactive Frontend: Responsive HTML/CSS/JavaScript interface for adding, editing, and deleting items, with real-time summary updates.
RESTful API: Handles client-side requests securely with JSON payloads and CORS support.
Error Handling & Logging: Robust error management and debugging with Python’s logging module.

Tech Stack:
Backend: Python, Flask, FPDF, smtplib
Frontend: HTML, CSS, JavaScript
Deployment: Deployed on GitHub, Render and Pythonanywhere <  http://hillary.pythonanywhere.com/  >; configurable for local hosting
Other: Environment variable management, CORS, responsive design

How to Run:Clone the repository
Install dependencies: pip install -r requirements.txt
Set environment variable: export EMAIL_PASSWORD=<your-gmail-app-password>
Run the app: python app.py
Access at http://localhost:8080

Web Development:
Built a RESTful API with Flask, handling JSON data and HTTP requests.
Enabled cross-origin resource sharing (CORS) for secure client-server communication.
Developed a responsive frontend with HTML, CSS, and JavaScript.

Frontend Development:
Designed an intuitive UI with dynamic table updates and form handling.
Implemented client-side logic for item management (add/edit/delete) and real-time calculations.
Applied CSS for styling and responsive design.

Integration with External Services:
Configured SMTP for secure email delivery using Gmail’s API.
Managed sensitive data (e.g., email credentials) with environment variables.

Error Handling & Debugging:
Implemented comprehensive error handling for SMTP authentication and network issues.
Used Python’s logging module for debugging and monitoring.

Project Management & Deployment:
Structured a full-stack application with clear separation of concerns (frontend, backend, templates).
Deployed the project on GitHub with clear documentation.
Ensured portability with environment variable configuration.

Problem-Solving & Business Logic:Designed business logic for VAT calculations and dynamic PDF generation.
Created a user-friendly workflow for invoice/quotation creation and delivery.

