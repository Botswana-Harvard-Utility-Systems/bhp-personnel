import random
import string

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_base.utils import get_utcnow
from edc_constants.constants import YES

from bhp_personnel.models import (Contract, ContractExtension,
                                  Contracting, Employee, Pi, Supervisor)
from .renewal_intent import RenewalIntent
from ..utils import send_employee_activation, send_manager_on_employee_activation
from ..utils import get_schedule_obj, schedule_email_notification, schedule_sms_notification
from ..utils import create_appraisal


@receiver(post_save, weak=False, sender=Employee,
          dispatch_uid='employee_on_post_save')
def employee_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:

            try:
                created_user = User.objects.get(email=instance.email)
            except User.DoesNotExist:
                pwd = ''.join(
                    random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                    for _ in range(8))
                created_user = User.objects.create_user(username=instance.email,
                                                        email=instance.email,
                                                        password=pwd,
                                                        first_name=instance.first_name,
                                                        last_name=instance.last_name,
                                                        is_staff=False, )

                employee_group = Group.objects.get(name='Employee')
                employee_group.user_set.add(created_user)

                send_employee_activation(created_user)
                send_manager_on_employee_activation(instance)

            try:
                Supervisor.objects.get(first_name=instance.first_name,
                                       last_name=instance.last_name)
            except Supervisor.DoesNotExist:
                pass
            else:
                supervisor_group = Group.objects.get(name='Supervisor')
                supervisor_group.user_set.add(created_user)


@receiver(post_save, weak=False, sender=Pi,
          dispatch_uid='pi_on_post_save')
def pi_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        User.objects.create_user(username=instance.
                                 first_name[0] + '' + instance.last_name,
                                 email=instance.email,
                                 password=instance.first_name + '@2020',
                                 first_name=instance.first_name,
                                 last_name=instance.last_name,
                                 is_staff=True, )


@receiver(post_save, weak=False, sender=Contract,
          dispatch_uid='contract_on_post_save')
def contract_on_post_save(sender, instance, raw, created, **kwargs):
    """
    Schedule email and sms reminder for 3 months before contract end
    date.
    """
    if not raw and created:
        schedule_email_notification(instance)


@receiver(post_save, weak=False, sender=Contracting,
          dispatch_uid='contracting_on_post_save')
def contracting_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        try:
            contract_obj = Contract.objects.filter(
                identifier=instance.identifier).latest(
                    'start_date')
        except Contract.DoesNotExist:
            raise ValidationError(f'Missing contract, create a new contract')
        else:
            instance.contract = contract_obj
            create_appraisal(contract_obj, appraisal_type='mid_year')


@receiver(post_save, weak=False, sender=ContractExtension,
          dispatch_uid='contractextension_on_post_save')
def contractextension_on_post_save(sender, instance, raw, created, **kwargs):
    """
    Reschedule an email and sms reminder for 3months before contract end
    date after extension.
    """
    if not raw and created:
        schedule_obj = get_schedule_obj(
            identifier=instance.contract.identifier)
        if schedule_obj:
            schedule_obj.delete()
        schedule_email_notification(instance, ext=True)
        schedule_sms_notification(instance, ext=True)


@receiver(post_save, weak=False, sender=RenewalIntent,
          dispatch_uid='renewal_intent_on_post_save')
def renewal_intent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    Reschedule an email and sms reminder for 3months before contract end
    date after extension.
    """
    if not raw and created:
        if instance.intent == YES:
            create_appraisal(instance.contract, appraisal_type='contract_end')
