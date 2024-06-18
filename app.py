from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
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
app.config['MAIL_USERNAME'] = 'helpdeskform@townofparadise.com'  
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Read from environment variable
app.config['MAIL_DEFAULT_SENDER'] = 'helpdeskform@townofparadise.com'

mail = Mail(app)

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    image = FileField('Image')  # New field for image upload
    submit = SubmitField('Send')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():

        #create message object
        msg1 = Message(
            form.subject.data,
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=['helpdesk@townofparadise.com']  
        )
        msg1.body = f"From: {form.name.data} <{form.email.data}>\n\n{form.message.data}"
        if form.image.data:  # If an image file was uploaded
            image_file = request.files[form.image.name]
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join('uploads', filename))  # Save the file to a directory named 'uploads'
            with app.open_resource(os.path.join('uploads', filename)) as fp:
                msg1.attach(filename, 'image/*', fp.read())  # Attach the file to the email message
        
        # Create a second message object
        msg2 = Message(
            'Request Received',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[form.email.data]
        )
        msg2.body = 'Luis and Travis have received your request and will be in touch soon!'

        # Send the second email
        try:
            mail.send(msg2)
            flash('Luis and Travis have received your request and will be in touch soon!', 'success')
        except Exception as e:
            flash(f'Failed to send second email: {str(e)}', 'danger')
        
        
        try:
            mail.send(msg1)
            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send email: {str(e)}', 'danger')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)