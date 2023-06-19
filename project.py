# Harvard CS50 Python
########################################
# Final project
# Project name: Authentication App With Rate Limiter
# Creator: Paul Münzner
# python project.py

import re
import csv
import sys
import bcrypt
import validators
from datetime import datetime, timezone, timedelta

###################################################
###################################################
#####  AUTHENTICATION APP WITH RATE LIMITER  ######
###################################################


################ MAIN #############################
# main
def main():
    auth_type = auth_selection(input(lib["welcome"]))
    email = input_request(auth_type, "email")
    password = input_request(auth_type, "password")
    if auth_type == "register":
        print(process_registraion(password, email))
    else:
        print(process_login(password, email))

#####################################################
################ STEP 1 #############################
# Select option (register or login)
def auth_selection(auth_type):
    if auth_type.lower() == 'login' or auth_type.lower() == 'register':
        return auth_type
    else:
        raise ValueError(lib["option_error"])

#####################################################
################ STEP 2 #############################
# Requesting input for email address and password. For login and registration used
def input_request(auth_type, prop):
    def validate(request):
        return (
            validate_email_format(request)
            if prop == "email"
            else validate_password_format(request)
        )

    login_question = (
        lib["request_email"]["login"]
        if prop == "email"
        else lib["request_password"]["login"]
    )
    register_question = (
        lib["request_email"]["register"]
        if prop == "email"
        else lib["request_password"]["register"]
    )
    not_valid_response = (
        lib["request_email"]["repeat_invalid_format"]
        if prop == "email"
        else lib["request_password"]["repeat_invalid_format"]
    )
    question = login_question if auth_type == "login" else register_question
    request = input(question)
    valid = validate(request)
    while valid == False and auth_type == "register":
        request = input(not_valid_response)
        valid = validate(request)
    else:
        return request


# Email format validation
def validate_email_format(email):
    if validators.email(email):
        return True
    else:
        return False

# Password format validation
def validate_password_format(password):
    valid = re.search(r"^[A-Za-z0-9+=,\.@-_]{10,16}$", password)
    if valid:
        return True
    else:
        return False



################ REGISTRATION ###############################################
# save registration data email and password to csv file if not registered yet
################
def process_registraion(password, email):
    # Check registrations.csv if email address already registered
    list = read_csv("registrations")
    exist = False
    for entry in list:
        if entry["email"] == email:
            exist = True
    # Only add new registered user in registrations.csv if not registered so far
    if exist == False:
        with open("registrations.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["email", "password"])
            writer.writerow(
                {"email": email, "password": hash_password(password).decode("utf8")}
            )
    return lib["response_registration"]


################ LOGIN ####################################
# Manage login process
def process_login(password, email):
    registrations = read_csv("registrations")
    for entry in registrations:
        if entry["email"] == email:
            user_exist = True
            user_password = entry["password"]
            user_email = entry["email"]
            break
    else:
        user_exist = False
    # User is registered with provided email address?
    if user_exist == False:
        sys.exit(lib["login"]["wrong_credentials"])
    # Defend brute force attack
    # User did not exceed max. login failures within allowed time span?
    if rate_limit_check(user_email):
        sys.exit(lib["login"]["limit_reached"])
    # Password validation
    password_correct = password_match(password, user_password)
    if password_correct == False:
        with open("logger.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["email", "date"])
            writer.writerow({"email": email, "date": time_now_london()})
        sys.exit(lib["login"]["wrong_credentials"])
    # Check if provided email and password match. If yes, login successfull.
    else:
        return lib["login"]["success"]



##################### RATE LIMITER #############################
# check if max number of failed logins within certain time window reached
def rate_limit_check(email):
    logs = read_csv("logger")
    count = 0
    time_window_min = 10
    max_allowed_failed_logins = 3
    time_now = time_now_london()
    for log in logs:
        email = log['email']
        log_date = datetime.strptime(log['date'], '%Y-%m-%d %H:%M:%S.%f%z')
        difference_minutes = time_now.timestamp()/60 - log_date.timestamp()/60
        if log['email'] == email and difference_minutes < time_window_min:
            count += 1
    return count >= max_allowed_failed_logins



# Read csv file depending on requested document (logger.csv or registrations.csv)
def read_csv(type):
    if type != "registrations" and type != "logger":
        raise ValueError(lib["wrong_file_type_read"])
    file_name = "registrations.csv" if type == "registrations" else "logger.csv"
    try:
        filelist = []
        with open(file_name) as file:
            content = csv.DictReader(file)
            for row in content:
                filelist.append(row)
            return filelist
    # If file not existing (FileNotFoundError), it will be created automatically
    except FileNotFoundError:
        with open(file_name, "w") as file:
            newheader = (
                ["email", "password"] if type == "registrations" else ["email", "date"]
            )
            writer = csv.DictWriter(file, fieldnames=newheader)
            writer.writeheader()
            return []




# Store passwords as hashes only. Function to create hash during registration
def hash_password(password):
    bytes = password.encode('utf-8')
    return bcrypt.hashpw(bytes, bcrypt.gensalt())



# Compare hashed password in registrations.csv with provided password during login
def password_match(password, hash):
    hash_encoded = hash.encode("utf8")
    password_encoded = password.encode('utf-8')
    if bcrypt.checkpw(password_encoded, hash_encoded):
        return True
    else:
        return False




# Get London time to log failed logins in logger.csv
def time_now_london():
    time_zone_london = timezone(timedelta(hours=1))
    return datetime.now(time_zone_london)


# Library used as collection for responses
lib = {
    "welcome": "Welcome to authorization app. Choose and enter 'login' or 'register': ",
    "option_error": "Your chosen option is not available. Program stopped!",
    "request_password": {
        "login": "Enter your password: ",
        "register": "Choose your new password. Use min 10 and max 16 characters. Can only contain alphanumeric characters or any of the following: +=,.@-_: ",
        "repeat_invalid_format": "No valid format. Try again with min 10 and max 16 characters; only alphanumeric characters or any of the following: +=,.@-_: ",
    },
    "request_email": {
        "login": "Enter your registered email address: ",
        "register": "Choose your new email address: ",
        "repeat_invalid_format": "No valid email address format. Try again: ",
    },
    "response_registration": 'You are registered. Feel free to sign in.',
    "login": {
        "limit_reached": "Too many failed login attempts. Wait a while to try again.",
        "success": "Successfully signed in. Welcome to my app!",
        "wrong_credentials": "User does not exist or email and password combination not matching.",
    },
    "wrong_file_type_read": "Can only read files for registrations or logger.",
}


if __name__ == "__main__":
    main()


