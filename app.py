from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv('creds.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to a strong, unique value
app.config['MAIL_SERVER'] = 'smtp.office365.com'  # Exchange Online SMTP server
app.config['MAIL_PORT'] = 587  # SMTP port for TLS
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USE_SSL'] = False  
app.config['MAIL_USERNAME'] = 'tthompson@townofparadise.com'  
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Read from environment variable
app.config['MAIL_DEFAULT_SENDER'] = 'tthompson@townofparadise.com'

mail = Mail(app)

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            form.subject.data,
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=['helpdesk@townofparadise.com']  # Replace with your email for testing
        )
        msg.body = f"From: {form.name.data} <{form.email.data}>\n\n{form.message.data}"
        try:
            mail.send(msg)
            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send email: {str(e)}', 'danger')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
