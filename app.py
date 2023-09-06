from flask import Flask, render_template, request, redirect, url_for, session
import datetime, random, string, sqlite3
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kajal03g@gmail.com'  # Replace with your Gmail email address
app.config['MAIL_PASSWORD'] = 'iewrwnyvngkbgwmg'  # Replace with your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'kajal03g@gmail.com'  # Replace with your Gmail address

mail = Mail(app)

# Database connection
conn = sqlite3.connect('interviews.db')
c = conn.cursor()

# Create a table for interviewer schedule
c.execute('''
    CREATE TABLE IF NOT EXISTS interviewer_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        interviewer_name TEXT NOT NULL,
        interviewer_email TEXT NOT NULL,
        datetime TEXT NOT NULL,  -- Store date and time as a single string
        confirmed INTEGER DEFAULT 0
    )
''')
conn.commit()

# Create a table for interviewee requests
c.execute('''
    CREATE TABLE IF NOT EXISTS interviewee_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        interviewee_name TEXT NOT NULL,
        interviewee_email TEXT NOT NULL,
        datetime TEXT NOT NULL,  -- Store date and time as a single string (YYYY-MM-DD HH:MM:SS)
        confirmed INTEGER DEFAULT 0,
        interviewer_email TEXT,
        google_meet_link TEXT
    )
''')

conn.commit()

# Close the connection after creating tables
conn.close()

# from google.oauth2.credentials import Credentials

# json_key_content = {
#     "type": "service_account",
#     "project_id": "schedulingproject-393817",
#     "private_key_id": "0f9452ece5d3ccd1543b6ef5590859ebab127cac",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDbCKszPp81wwnT\nhaKaj+Z9h5Nk4L7EQsbz111SSW53BCAMOyIQibPD6DzZNL5T139YFv75r6WLbavo\nbsYQei5tLNsvNYVHRFPVG9fLL9Y2L677JIFVwxhjJLKHstwgUvUct6qbXT7kLNhD\n4KGSTocECRWhLb9dYrRqeW0+U9FCP0i0qYFPgR+0dE0d4SOJQzjLQjlFLQ/nT1l7\n1+JDn7m97jfOkWDBnIVD9ixfW19YCne/OAZBDq6SddLxnxY892/MzrfcXws3wIKy\nu5+qx+YPvJr4Q2C64bf0basQW7nd9cIYwrjqzhGX7CVJrpDGCIwKTdUeVYiQmv6W\ndNSxL1WFAgMBAAECggEADY1EQRKV+YFnPryXxRYJLelw/6lTdEN+GWvQ8ic+m+4t\nPhnR2jxthb39NyJ8ciXfqFIdQCfox1nSQeUfVmP7h7ViRvykkeES325uaWZndl54\nkOupyuYcFf+ZF4Hup7CqSgwSagluEOJgwRZeuMrTWgxmglyZE0yTmruHkaHQTS0N\njkKEnJnFntRPGvrE/J0xOE6LMHur4wRcCMZNePPlkY8QFgB7hQDKL4crnsey7UlU\nShtepe2QsmEuGdUm3PYISrDEC1ijIv4bZSPamzMC0e510ocQOi34ToqN55AFlR8y\nycAizJQDg6tXY3abIkVde1wOQLmh9cvotP7cW/VKMQKBgQDuH5jFY173hi1aV8iD\nM06KdFVtV8msuHt2tWYueNGi9TJoWmlePnvYZg8VXnYfrThIlnjYchifWfFhAUjN\npGihtMYFHNYtONu6uCcbrlFE6frVom5ukIFqP/ZMBmBpwdh/CPknjn2SylYlQLZv\njXjjeYbOGgfM/CDeQDpAS88hDQKBgQDrejJsqPczdFRQ4O+viZlbXBs+KDJBhTOC\np6fC7aneli+nMNxvubAa4TSOnXA/Uin6f5wfiCG9nMMAibInK2pUMtdq3Mk5L3Bz\nzg34iilUnx2ICEyfVrc66UQcA6mQyufTAvnSDKk27GI3NLYYbpVVyuFAsYqf89xM\n363PMjo4WQKBgQDlBY6xifl0p6BHG9bGGTqY/3qKR7y4WlakvaMhXyKBUMLCivJ8\nqiwC3WX0b328yaUwa0ifJF16Jc96NPoIju/zVyJ9GFcF94Gd/C/g969CUKfngOol\nfOZ7gjkotZlVHhNTWxYHbYxo+iIQgkT01WRHpEJ7R53pETWrjKp53G/CoQKBgH1j\n2ooGB2x825Ed1kQxD1qY12Dn4qsFFQLT5/9isvv2GXX8DMXpqR8HIQd4SpdNV1Eu\ntqILyXvAiA43RIibE8m2MQOUggpTepwP81yPpaaL/Bu9359Re8yA/mW0hYy2n2+7\nu+/gEhNPGJWxGe40pIzEteHPKLQ4FO1Shqk4Y8wxAoGANAyLPHhM9SxJ891iPUhI\n180tcC5aWELmpvObJOoFRdkhJmtRmOd8RYFRDn9JL/dMdbCtpGk9cXRp5bB6r8u1\nA6jD25NEkeJADatqdK9O46mzVgHw6e2JqDPivlmMilqY+DQTDeVBXR3b3ByJTqGl\nUg2bqZD5UtWLztFhY6qoxOk=\n-----END PRIVATE KEY-----\n",
#     "client_email": "interviewscheduling@schedulingproject-393817.iam.gserviceaccount.com",
#     "client_id": "113561895603016446654",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/interviewscheduling%40schedulingproject-393817.iam.gserviceaccount.com",
#     "universe_domain": "googleapis.com"
# }
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# # Create credentials using the service account info
# credentials = service_account.Credentials.from_service_account_info(json_key_content)

# # Build the Google Calendar API service
# service = build('calendar', 'v3', credentials=credentials)

@app.route('/interviewer/schedule', methods=['GET','POST'])
def interviewer_schedule():
    name = None
    email = None
    scheduled_datetime = None
    if request.method == 'POST':
        # Get the form data
        name = request.form.get('interviewer_name')
        email = request.form.get('interviewer_email')
        date = request.form.get('date')
        time = request.form.get('time')

        # Combine date and time to create a datetime object
        scheduled_datetime = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Store the scheduled interview details in the database
        with sqlite3.connect('interviews.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO interviewer_schedule (interviewer_name, interviewer_email, datetime) VALUES (?, ?, ?)",
                      (name, email, scheduled_datetime))

        return redirect(url_for('interviewer_schedule'))

    # Fetch available slots for the interviewee request form
    with sqlite3.connect('interviews.db') as conn:
        c = conn.cursor()
        c.execute("SELECT datetime FROM interviewer_schedule WHERE confirmed = 0")
        available_slots = c.fetchall()

    return render_template('interviewer_schedule.html', name=name, email=email,
                           scheduled_datetime=scheduled_datetime, available_slots=available_slots)
        # Generate the Google Meet link
        # google_meet_link = generate_google_meet_link()

    #     

    # # Render a template to display the scheduled interview details to the interviewee
    # return render_template('interviewer_schedule.html', name=name, email=email, scheduled_datetime=scheduled_datetime)

# def generate_google_meet_link(date_time):
#     event = {
#         "summary": "Interview Meeting",
#         "start": {"dateTime": date_time},
#         "end": {"dateTime": date_time},
#         "conferenceData": {
#             "createRequest": {"conferenceSolutionKey": {"type": "hangoutsMeet"}}
#         },
#     }
    
#     event = service.events().insert(calendarId="primary", body=event).execute()
#     return event.get("conferenceData").get("entryPoints")[0].get("uri")

def send_approval_email(interviewee_name, interviewee_email, interview_datetime):
    # Email subject and body
    subject = 'Interview Request Approval'
    body = f"Dear Interviewer,\n\n{interviewee_name} has requested an interview on {interview_datetime}.\n\n" \
           f"Please review the request and confirm it by accessing the link below:\n\n" \
           f"{url_for('confirm_interview', interviewee_email=interviewee_email, datetime=interview_datetime, _external=True)}\n\n" \
           f"Best regards,\nThe Interview Scheduler"

    # Use the Flask-Mail extension to send the email
    msg = Message(subject=subject, recipients=['kajal03g@gmail.com'], body=body)
    mail.send(msg)

@app.route('/interviewee/request', methods=['GET', 'POST'])
def interviewee_request():
    if request.method == 'POST':
        interviewee_name = request.form['interviewee_name']
        interviewee_email = request.form['interviewee_email']
        selected_slot = request.form.get('selected_slot')

        # Fetch the interview datetime based on the selected slot
        if selected_slot:
            interview_datetime = selected_slot

            # Send email to the interviewer for approval
            send_approval_email(interviewee_name, interviewee_email, interview_datetime)

            # Save the interviewee request in the database
            conn = sqlite3.connect('interviews.db')
            c = conn.cursor()
            c.execute("INSERT INTO interviewee_requests (interviewee_name, interviewee_email, datetime) VALUES (?, ?, ?)",
                      (interviewee_name, interviewee_email, interview_datetime))
            conn.commit()
            conn.close()

            return redirect(url_for('interviewee_request'))

    # Fetch the interview details from the database
    conn = sqlite3.connect('interviews.db')
    c = conn.cursor()
    c.execute("SELECT datetime FROM interviewer_schedule WHERE confirmed = 0")
    available_slots = c.fetchall()
    conn.close()

    return render_template('interviewee_request.html', available_slots=available_slots)

def send_confirmation_email(interviewer_email, interviewee_name, interviewee_email, date, time):
    subject = 'Interview Request Confirmation'
    body = f"Dear Interviewer,\n\n{interviewee_name} has requested an interview on {date} at {time}.\n\n" \
           f"Please confirm the interview by accessing the link below:\n\n" \
           f"{url_for('confirm_interview', interviewer_email=interviewer_email, interviewee_email=interviewee_email, date=date, time=time, _external=True)}\n\n" \
           f"Best regards,\nThe Interview Scheduler"

    msg = Message(subject=subject, recipients=[interviewer_email], body=body)
    mail.send(msg)

    return True
@app.route('/confirm', methods=['GET', 'POST'])
def confirm_interview():
    if request.method == 'POST':
        confirmation_status = request.form['confirmation_status']
        interviewer_email = request.form['interviewer_email']
        interviewee_name = request.form['interviewee_name']
        interviewee_email = request.form['interviewee_email']
        date = request.form['date']
        time = request.form['time']
            

        # Update the interview confirmation status in the database
        conn = sqlite3.connect('interviews.db')
        c = conn.cursor()
        c.execute("UPDATE interviewer_schedule SET confirmed = ? WHERE interviewer_email = ? AND datetime = ?",
                  (1 if confirmation_status == 'accept' else -1, interviewer_email, f"{date} {time}"))
        c.execute("UPDATE interviewee_requests SET confirmed = ? WHERE interviewee_email = ? AND datetime = ?",
                  (1 if confirmation_status == 'accept' else -1, interviewee_email, f"{date} {time}"))


        conn.commit()
        conn.close()

        if confirmation_status == 'accept':
            # try:
            #     # Generate Google Meet link using the provided date and time
            #     date_time = f"{date}T{time}:00"  # Format as ISO 8601
            #     google_meet_link = generate_google_meet_link(date_time)
        
                # Send an email to the interviewee with the confirmed details and Google Meet link
            subject = 'Interview Confirmation'
            body = f"Dear {interviewee_email},\n\nYour interview on {date} at {time} has been confirmed. " \
                f"The Google Meet link is: \n\nBest regards,\nThe Interview Scheduler"
            msg = Message(subject=subject, recipients=[interviewee_email], body=body)
            mail.send(msg)
            

        elif confirmation_status == 'reject':
            subject = 'Interview Confirmation'
            body = f"Dear {interviewee_email},\n\nYour interview on {date} at {time} has been Rejected by the interviewer. Please book another available slots." \
                #    f"The Google Meet link is: {google_meet_link}\n\nBest regards,\nThe Interview Scheduler"
            msg = Message(subject=subject, recipients=[interviewee_email], body=body)
            mail.send(msg)
        return redirect(url_for('confirm_interview'))

    # Fetch the interview details from the database
    conn = sqlite3.connect('interviews.db')
    c = conn.cursor()
    c.execute("SELECT interviewer_email, interviewee_email, interviewee_name, datetime FROM interviewee_requests WHERE confirmed = 0")
    interview_requests = c.fetchall()


    conn.close()

    return render_template('confirm_interview.html', interview_requests=interview_requests)

@app.route('/notify', methods=['POST'])
def notify_interview_status():
    if request.method == 'POST':
        interviewer_email = request.form['interviewer_email']
        interviewee_email = request.form['interviewee_email']
        date = request.form['date']
        time = request.form['time']
        confirmation_status = request.form['confirmation_status']

        if confirmation_status == 'accept':
            # Send an email to the interviewee with the confirmed details
            subject = 'Interview Confirmation'
            body = f"Dear {interviewee_email},\n\nYour interview on {date} at {time} has been confirmed. " 
                #    f"The Google Meet link is: {google_meet_link}\n\nBest regards,\nThe Interview Scheduler"

            msg = Message(subject=subject, recipients=[interviewee_email], body=body)
            mail.send(msg)

        # Send an email to the interviewer with the interview status
        subject = 'Interview Status Notification'
        status = 'confirmed' if confirmation_status == 'accept' else 'rejected'
        body = f"Dear {interviewer_email},\n\nThe interview on {date} at {time} with {interviewee_email} has been {status}.\n\n" \
               f"Best regards,\nThe Interview Scheduler"

        msg = Message(subject=subject, recipients=[interviewer_email], body=body)
        mail.send(msg)

    return redirect(url_for('confirm_interview'))

if __name__ == '__main__':
    app.run(debug=True)
