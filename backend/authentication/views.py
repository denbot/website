from django.urls.base import reverse_lazy
from django.views.generic.edit import FormView

from authentication.forms import PhoneNumberForm, OTPForm


class LoginFormView(FormView):
    template_name = 'authentication/login.html'
    form_class = PhoneNumberForm
    success_url = reverse_lazy('login_otp')

    def form_valid(self, form):
        form.send_otp()
        # TODO Send back form with OTP field
        return super().form_valid(form)


class LoginOtpFormView(FormView):
    template_name = 'authentication/login_otp.html'
    form_class = OTPForm
    success_url = '/NOT_BLEGH'

    def form_valid(self, form):
        form.verify_otp()  # We should probably do something about this
        return super().form_valid(form)
