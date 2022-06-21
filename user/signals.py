from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format('password_reset: reset-password-request', reset_password_token.key)

    send_mail(
        "Password Reset for {title}".format(title="Some website title"),
        email_plaintext_message,
        "djangoblogkunal@gmail.com",
        [reset_password_token.user.email]
    )