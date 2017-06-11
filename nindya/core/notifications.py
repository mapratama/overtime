import django_rq
from django.conf import settings

from gcm import GCM
from gcm.gcm import GCMInvalidRegistrationException, GCMNotRegisteredException


def send_notification(user, data, async=True):
    gcm = GCM(settings.GOOGLE_API_KEY)

    if not user.push_notification_key:
        return

    kwargs = {
        "data": data,
        "registration_ids": [user.push_notification_key],
    }

    try:
        if async:
            django_rq.enqueue(gcm.json_request, **kwargs)
        else:
            gcm.json_request(**kwargs)
    except (GCMInvalidRegistrationException, GCMNotRegisteredException):
        return


def send_coordinator_notification():
    from nindya.apps.users.models import User
    users = User.objects.filter(is_active=True, type=User.TYPE.coordinator)
    for user in users:
        notification_data = {
            'title': 'Pengajuan Lembur Baru',
            'body': 'Terdapat pengajuan lembur baru, silahkan reload data lembur di dalam aplikasi',
            'action': 'sync_overtime',
        }
        send_notification(user, notification_data)


def send_manager_notification():
    from nindya.apps.users.models import User
    users = User.objects.filter(is_active=True, type=User.TYPE.manager)
    for user in users:
        notification_data = {
            'title': 'Pengajuan Lembur Baru',
            'body': 'Terdapat pengajuan lembur baru yang telah disetujui koordinator,'
                    'silahkan reload data lembur di dalam aplikasi',
            'action': 'sync_overtime',
        }
        send_notification(user, notification_data)


def send_accepted_coordinator_notification(overtime):
    notification_data = {
        'title': 'Koordinator Menyetujui Pengajuan',
        'body': 'Pengajuan lembur anda telah disetujui koordinator'
                ' dan pengajuan telah diteruskan kepada manager',
        'action': 'sync_overtime_details',
        'extra_data': overtime.id
    }
    send_notification(overtime.user, notification_data)


def send_accepted_manager_notification(overtime):
    notification_data = {
        'title': 'Manager Menyetujui Pengajuan',
        'body': 'Pengajuan lembur anda telah disetujui manager'
                ' , silahkan melaksanakan lembur sesuai penjelasan dan catatan atasan',
        'action': 'sync_overtime_details',
        'extra_data': overtime.id
    }
    send_notification(overtime.user, notification_data)


def send_activated_user_notification(user):
    notification_data = {
        'title': 'Akun Anda Telah Diaktifasi',
        'body': 'Admin telah mengaktifasi akun anda, silahkan login aplikasi '
                'dengan menggunakan email dan password yang telah anda daftarkan.',
        'action': 'activated_user'
    }
    send_notification(user, notification_data)
