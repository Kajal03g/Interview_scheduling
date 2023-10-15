# Interview_scheduling

## Problem Statement

Navrojan the job portal of our organization, Stuvalley, needs a system to streamline the process of scheduling and managing interviews between interviewers and interviewees. The current manual process is time-consuming and error-prone.

## Solution

Developed an Interview Scheduling Application using Flask, which allows interviewers to schedule interview slots and interviewees to request interview slots. The application handles confirmation and rejection of interview requests and sends notification emails to both interviewers and interviewees.

## Tech Stack Used

- Flask: A Python web framework for building the application.
- SQLite: A lightweight and embedded database for storing interview schedule and request data.
- Flask-Mail: An extension for sending emails.
- HTML/CSS: Front-end for the user interface.

## Organization

- **Organization:** Stuvalley
- **Mentors:** Mr. Ayushman Pranav, Dr.Pankaj Mishra

## Observation

The application has greatly improved the efficiency of our interview scheduling process. It provides a user-friendly interface for both interviewers and interviewees, reducing manual errors and ensuring smooth communication.

## Screenshots
- Interviewers can access the schedule form by visiting the **/interviewer/schedule** route in a web browser. Interviewers can enter their name, email, date, and time for the interview slot they want to schedule.
  ![Interviewee Request and 2 more pages - Personal - Microsoft​ Edge 18-09-2023 00_53_52](https://github.com/Kajal03g/Interview_scheduling/assets/120003423/0c6b08b7-fcd7-48eb-929c-77bc40cebfab)

- The available slots are displayed on the page, allowing interviewers to see the slots they and others have scheduled. Interviewees can access the request form by visiting the **/interviewee/request** route in a web browser. Interviewees can enter their name, email, and select an available interview slot from the displayed options.

![Interviewee Request and 2 more pages - Personal - Microsoft​ Edge 18-09-2023 00_53_52](https://github.com/Kajal03g/Interview_scheduling/assets/120003423/3d306861-0ce3-49a8-a671-4d12db579352)


- Upon submission, the code sends an approval email to the interviewer responsible for the selected slot. The email includes details of the interviewee's request and a link for the interviewer to confirm the request.

![Editing Interview_scheduling_README md at main · Kajal03g_Interview_scheduling - Google Chrome 06-09-2023 14_24_21 (2)](https://github.com/Kajal03g/Interview_scheduling/assets/120003423/9b9b1e30-24c5-450b-aa38-5bca4969d30f)

- Interviewers can access the confirmation page by visiting the **/confirm** route in a web browser. Interviewers see a list of pending interviewee requests, including the interviewee's name, email, requested date, and time. Interviewers can choose to confirm or reject interviewee requests. This action updates the **confirmed** column in the database.

![Interviewer Schedule Input and 2 more pages - Personal - Microsoft​ Edge 18-09-2023 00_52_37](https://github.com/Kajal03g/Interview_scheduling/assets/120003423/dccd331e-d030-4069-a01a-6191ffd29dd2)

- If an interviewee's request is confirmed, the code sends a confirmation email to the interviewee with details of the confirmed interview.
If a request is rejected, the code sends a rejection email to the interviewee, prompting them to book another available slot.

![Interview Confirmation - kaja bt21cs22@opju ac in - OP Jindal University Mail - Google Chrome 06-09-2023 14_26_04 (3)](https://github.com/Kajal03g/Interview_scheduling/assets/120003423/f0f1c804-58d0-4821-b0e4-b0ecbdf25166)



## Repository Link

https://github.com/Kajal03g/Interview_scheduling

