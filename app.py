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
                f" \n\nBest regards,\nThe Interview Scheduler"
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
