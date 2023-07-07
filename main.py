import csv
import random
import smtplib
import bcrypt

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


def check_email_exists(email):
    with open('user_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2] == email:
                return True
    return False


def login():
    email = input("Please enter your email: ")
    password = input("Please enter your password: ")

    with open('user_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2] == email:
                hashed_password = row[1].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    # Proceed with login
                    print("Login successful!")
                    return

    print("Email or password is incorrect. Please try again.")


def send_otp(email, otp):
    # Replace the placeholders with your SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'dipsubha.co@gmail.com'
    smtp_password = 'fjcnclsjrmxrfayj'

    sender_email = 'your_email@example.com'
    receiver_email = email

    message = f'Subject: OTP Verification\n\nYour OTP is: {otp}'

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message)
        print("OTP sent successfully!")
        server.quit()
    except smtplib.SMTPException as e:
        print("Error occurred while sending the email:", str(e))


def create_user_account():
    name = input("Please enter your name: ")
    email = input("Please enter your email: ")
    password = input("Please enter a password: ")
    renter_password = input("Please re-enter your password: ")

    while password != renter_password:
        print("Your re-entered password is incorrect.")
        renter_password = input("Please re-enter your password correctly: ")

    if check_email_exists(email):
        print("Email already in use. Please go to the login page.")
    else:
        # Create a new user object
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(name, email, hashed_password)

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Send OTP to user's email
        send_otp(email, otp)

        # Verify OTP
        user_otp = int(input("Please enter the OTP sent to your email: "))

        if user_otp == otp:
            # Append user data to the CSV file
            with open('user_data.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([name, hashed_password.decode('utf-8'), email])
            print("\nUser Account Created Successfully!")
            print("Name:", user.name)
            print("Email:", user.email)
        else:
            print("Incorrect OTP. User account creation failed.")


# Main program
choice = input("Press 1 to login, 2 to create a new account: ")

if choice == '1':
    login()
elif choice == '2':
    create_user_account()
else:
    print("Invalid choice.")