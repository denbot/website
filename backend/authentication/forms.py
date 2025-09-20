from django import forms
from phonenumber_field.formfields import PhoneNumberField


class PhoneNumberForm(forms.Form):
    phone_number = PhoneNumberField()

    def send_otp(self):
        print("HALP I DON'T KNOW HOW TO SEND AN OTP")


class OTPForm(forms.Form):
    otp_code = forms.CharField()

    def verify_otp(self):
        print("I sure as fuck don't know how to verify one")
