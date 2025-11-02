from smtplib import SMTPException

from Crypto import Random
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mass_mail

from .models import Notifications


def contract_end_email_notification(
        first_name=None, last_name=None, email=None, supervisor_email=None,
        end_date=None):
    """
    Send email notification to employee for contract expiration.
    """
    Random.atfork()

    users = User.objects.filter(groups__name='HR')
    hr_emails = list(map(lambda user: user.email, users))

    msg = (f'Contract expiration notification ({end_date})',
           f'Dear {first_name} {last_name}, \n \n Please be notified that your'
           f' contract is ending on the {end_date}. For renewal draft a letter'
           ' for your supervisor to indicate renewal intent or otherwise. \n '
           '\n Have a good day :).',
           'BHP HR <no-reply@bhp.org.bw>',
           [email])

    hr_msg = (f'Contract expiration notification for {first_name} {last_name}',
              f'Please be notified that {first_name} {last_name}\'s contract '
              f'is ending on the {end_date}.',
              'BHP CMS <no-reply@bhp.org.bw>',
              hr_emails)

    supervisor_msg = (
        f'Contract expiration notification for {first_name} {last_name}',
        f'Please be notified that {first_name} {last_name}\'s contract is '
        f'ending on the {end_date}.',
        'BHP HR <no-reply@bhp.org.bw>',
        [supervisor_email])

    try:
        send_mass_mail((msg, hr_msg, supervisor_msg), fail_silently=False)
    except SMTPException as e:
        raise ValidationError(f'There was an error sending an email: {e}')
    else:
        email_addrs = [email, supervisor_email, ]
        email_addrs.extend(hr_emails)
        for email_addr in email_addrs:
            Notifications.objects.create(
                email=email_addr,
                success_status=True)
