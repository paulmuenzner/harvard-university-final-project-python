 # AUTHENTICATION APP WITH RATE LIMITER
 ### Video Demo:  https://youtu.be/gy8zwpGeDAU
 ### Description:
 This final project application written in Python reflects an authentication process in a simplified manner. It has been developed by Paul Münzner in the context of Harvard's course 'CS50’s Introduction to Programming with Python'. It offers the user to select two different options. One can either register with an email address and password or try to login by providing an email address and a password. The password for registration is validated with regex as it needs to meet a certain format. The email address is validated by using the pip installed validators library. The input for the login on the other hand is not validated to not provide any hints to malicious users. Once the registration is successful, the related data - email address and password in a hashed format - is saved to a CSV file as it is needed for following logins. The implementation of a database, for example MongoDB with PyMongo, was not possible. In the case the user decides to login, the procedure is different. First of all, the program checks if there were not more than 3 failed login attempts with this email address during the last 10 minutes. In principle this is a rate limiter preventing brute force attacks to a certain extent. If the rate limit threshold has been passed, the access is denied and the program stops; the login attempt failed. If the user did not reach the 3 failed login attempts within the last 10 minutes, the login process continues and checks if the password is correct. If the passwords doesn't match, this failed attempt is saved in a second CSV file to provide the these information for the rate limiter. If a registration with the provided email address exists in registrations.csv and the provided password matches with the registered password, the user successfully passed all requirements of the login procedure.

 ### App flowchart:

![My Image](cs50-flowchart-paul-muenzner.png)

 ### CS50 final project requirements:
 The CS50 Programming with Python final project is subject to the following repuirements: [Link](https://cs50.harvard.edu/python/2022/project/) <br>
 Harvard also requires, among other things, that the project is implemented in Python and all Python functions (min 4 incl. main) are in project.py placed in the root of the project.
 Any pip-installable libraries used must be listed, one per line, in a file called requirements.txt in the root of the project.

