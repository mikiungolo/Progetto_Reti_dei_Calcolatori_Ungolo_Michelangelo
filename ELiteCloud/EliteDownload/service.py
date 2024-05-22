import smtplib
from datetime import datetime, timedelta

import pyotp, configu


# service: generate otp code for authenticate 2FA login
def send_otp(request):
    # create code
    otp_obj = pyotp.TOTP(pyotp.random_base32(), interval = 60)
    # start validate
    otp = otp_obj.now()

    # save informations to session
    request.session["otp_code"] = otp_obj.secret
    valid_date = datetime.now() + timedelta(minutes = 1)
    request.session["otp_date"] = str(valid_date)

    send_email(otp, request.session["email"])

def send_email(otp, to_add):
    # port 587 is required for smtp
    server_smtp = smtplib.SMTP("smtp.gmail.com", 587)
    server_smtp.ehlo()
    # start TLS secure connection
    server_smtp.starttls()
    # login to gmail account
    server_smtp.login(configu.EMAIL_USER, configu.EMAIL_PASSWORD)

    server_smtp.sendmail(configu.EMAIL_USER, to_add,
                         "Subject: Codice OTP elite-cloud\n\n"
                         f"Il tuo codice otp e' {otp}\n"
                         "Se non hai richiesto il seguente codice OTP da elite-cloud ignora questa mail. ")


if __name__ == "__main__":
    print("Incorrect file runned")