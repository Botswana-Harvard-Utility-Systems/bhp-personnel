import logging
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_q.models import Schedule
from django_q.tasks import schedule

from edc_base.utils import get_utcnow
from edc_sms.classes import MessageSchedule

from .models import (Appraisal, Consultant, Contracting, Employee,
                     PerformanceAssessment, PerformanceReview, Supervisor)


logger = logging.getLogger(__name__)


def get_domain(request):
    try:
        domain = get_current_site(request).domain
    except Exception:
        domain = getattr(settings, 'DEFAULT_DOMAIN', 'example.com')
    return domain


def send_email(context, html_template, text_template):
    text_body = render_to_string(text_template, context)
    html_body = render_to_string(html_template, context)
    subject = context.get('subject')
    user = context.get('user')

    if not user and not user.email:
        logger.warning(
            'Activation email not sent: user missing or has no email.')
        return False

    to_email = [user.email]
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

    try:
        msg = EmailMultiAlternatives(subject, text_body, from_email, to_email)
        msg.attach_alternative(html_body, 'text/html')
        msg.send()
        logger.info(f'Activation email sent to {user.email}')
        return True
    except Exception as e:
        logger.exception(f'Failed sending activation email to {user.email}', e)
        return False


def send_employee_activation(user, request=None):
    """
        Takes each user one by one and sending an email to each
    """
    protocol = 'https'
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = get_domain(request)
    reset_path = reverse(
        'password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
    reset_url = f'{protocol}://{domain}{reset_path}'
    site_url = f'{protocol}://{domain}'

    subject = 'Time Sheet Activation Link'
    context = {
        'user': user,
        'subject': subject,
        'site_url': site_url,
        'reset_url': reset_url}

    text_body = 'emails/activation.txt'
    html_body = 'emails/activation.html'

    send_email(context, html_template=html_body, text_template=text_body)


def send_manager_on_employee_activation(user, request=None):
    mask = Employee.objects.get(id=user.id).supervisor_id
    supervisor = Supervisor.objects.get(id=str(mask))
    supervisor_firstname = Supervisor.objects.get(id=str(mask)).first_name
    supervisor_lastname = Supervisor.objects.get(id=str(mask)).last_name

    subject = 'New Employee Contracting'
    domain = get_domain(request)
    site_url = f'https://{domain}'

    context = {
        'user': supervisor,
        'supervisor_firstname': supervisor_firstname,
        'supervisor_lastname': supervisor_lastname,
        'subject': subject,
        'site_url': site_url}

    text_body = 'emails/activated.txt'
    html_body = 'emails/activated.html'

    send_email(context, html_template=html_body, text_template=text_body)


def update_contracting(instance=None):
    """
    Updating contracting details on post contract update
    """
    contracting = None

    if instance:
        try:
            contracting = Contracting.objects.get(
                identifier=instance.identifier,
                contract_id__isnull=True)
        except Contracting.DoesNotExist:
            raise ValidationError(f'Contracting for this contract does not exist '
                                  'please contact the Administrator.')
        else:
            contracting.contract = instance
            contracting.save()


def create_performance_review(
        contracting=None, contract=None, appraisal_instance=None):
    """
    Create Key Performance review for each KPA on the job description.
    @param contracting: Contracting instance
    @param contract: Contract instance
    @param appraisal_instance: appraisal instance
    """
    PerformanceAssessment.objects.create(contract=contract,
                                         emp_identifier=contract.identifier,
                                         review='mid_year')
    PerformanceAssessment.objects.create(contract=contract,
                                         emp_identifier=contract.identifier,
                                         review='contract_end')
    job_description = getattr(contracting, 'job_description', None)
    if job_description:
        for job_description_set in job_description.jobdescriptionkpa_set.all():
            PerformanceReview.objects.update_or_create(
                appraisal=appraisal_instance,
                kpa_title=job_description_set.key_performance_area,
                kpa_description=job_description_set.kpa_tasks
            )


def create_appraisal(instance=None, appraisal_type=''):
    """
    Creates appraisal on post save of a contract
    @param instance: Contract instance
    @param appraisal_type: type of appraisal
    """
    appraisal_instance, _ = Appraisal.objects.get_or_create(
        contract=instance,
        emp_identifier=instance.identifier,
        assessment_type=appraisal_type,
    )
    if appraisal_type == 'contract_end' and instance.contracting:
        create_performance_review(contracting=instance.contracting,
                                  contract=instance,
                                  appraisal_instance=appraisal_instance)


def schedule_email_notification(instance=None, ext=False):
    """
    Schedule email notification for contract expiration
    @param contract: instance of the contract
    """
    if instance:
        identifier = instance.contract.identifier if ext else instance.identifier
        end_date = (instance.end_date).strftime('%Y/%m/%d')
        user = get_user(identifier=identifier)
        schedule(
            'bhp_personnel.tasks.contract_end_email_notification',
            user.first_name,
            user.last_name,
            user.email,
            user.supervisor.email,
            end_date,
            name=f'{user.identifier}{get_utcnow()}',
            schedule_type='O',
            next_run=reminder_datetime(instance=instance, ext=ext))


def schedule_sms_notification(instance=None, ext=False):
    """
    Schedule sms notification for contract expiration
    @param contract: instance of the contract
    """
    user = None
    if instance:
        identifier = instance.contract.identifier if ext else instance.identifier
        user = get_user(identifier=identifier)

    msg = (f'Dear+{user.first_name},+Please+be+aware+that+your+contract+'
           f'is+ending+on+the+{instance.end_date}.+Please+notify+your+'
           'supervisor+of+your+renewal+intent+within+the+month.+Have+a+good+'
           'day+:).')

    MessageSchedule().schedule_message(
        message_data=msg,
        recipient_number=user.cell,
        sms_type='reminder',
        schedule_datetime=reminder_datetime(instance=instance, ext=ext))


def reminder_datetime(instance=None, ext=False):
    """
    Returns datetime when the reminder should be scheduled.
    """
    if instance:
        start_date = instance.start_date
        end_date = instance.end_date
        contract_duration = (end_date - start_date).days

        reminder_date = None
        if 0 < contract_duration <= 180:  # 6 Months
            reminder_date = instance.end_date - relativedelta(months=1)
        elif 180 < contract_duration <= 365:  # 1 Year
            reminder_date = instance.end_date - relativedelta(months=2)
        elif contract_duration > 365:  # 2 Years
            reminder_date = instance.end_date - relativedelta(months=3)

        tz = pytz.timezone('Africa/Windhoek')
        return tz.localize(
            datetime.combine(
                reminder_date, datetime.strptime('10:00', '%H:%M').time()))


def get_user(identifier=None):
    """
    Contract owner object getter
    @param identifier: unique identifier for the owner
    """
    try:
        return Employee.objects.get(identifier=identifier)
    except Employee.DoesNotExist:
        try:
            return Pi.objects.get(identifier=identifier)
        except Pi.DoesNotExist:
            try:
                return Consultant.objects.get(identifier=identifier)
            except Consultant.DoesNotExist:
                raise ValidationError(
                    f'Contract owner for identifier {identifier} does not exist.')


def get_schedule_obj(identifier=None):
    try:
        schedule_obj = Schedule.objects.get(name=f'{identifier}{get_utcnow()}')
    except Schedule.DoesNotExist:
        return None
    else:
        return schedule_obj
