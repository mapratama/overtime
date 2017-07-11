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


def send_new_overtime_notification(user, created_by):
    notification_data = {
        'title': 'Penunjukan Lembur oleh %s' % created_by,
        'body': 'Terdapat penunjukan lembur baru dari % s, '
                'silahkan reload data lembur di dalam aplikasi' % created_by,
        'action': 'sync_overtime',
    }
    send_notification(user, notification_data)


def send_coordinator_notification(user):
    from overtime.apps.users.models import User
    users = User.objects.filter(is_active=True, type=User.TYPE.coordinator,
                                department=user.department)
    for user in users:
        notification_data = {
            'title': 'Pengajuan Lembur Baru',
            'body': 'Terdapat pengajuan lembur baru, silahkan reload data lembur di dalam aplikasi',
            'action': 'sync_overtime',
        }
        send_notification(user, notification_data)


def send_manager_notification(user):
    from overtime.apps.users.models import User
    users = User.objects.filter(is_active=True, type=User.TYPE.manager,
                                department=user.department)
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


def send_canceled_notification(overtime, canceled_by_manager=True):
    if canceled_by_manager:
        position = 'Manager'
    else:
        position = 'Koordinator'

    notification_data = {
        'title': 'Pengajuan Anda Ditolak',
        'body': ('Pengajuan anda ditolak oleh %s, silahkan lihat data '
                 'pengajuan untuk melihat detail penolakan' % position),
        'action': 'sync_overtime_details',
        'extra_data': overtime.id
    }
    send_notification(overtime.user, notification_data)


def send_need_approval_notification():
    from overtime.apps.users.models import User
    users = User.objects.filter(is_superuser=True)
    for user in users:
        notification_data = {
            'title': 'Terdapat User Baru',
            'body': 'Terdapat user baru yang telah melakukan registrasi. '
                    'Silahkan cek data untuk aktifasi user tersebut di dalam web',
            'action': 'sync_overtime',
        }
        send_notification(user, notification_data)


def send_new_forgets_notification():
    from overtime.apps.users.models import User
    users = User.objects.filter(is_superuser=True)
    for user in users:
        notification_data = {
            'title': 'Permintaan Ubah Password',
            'body': 'Terdapat permintaan perubahan password. '
                    'Silahkan cek data permintaan tersebut di dalam web',
            'action': 'sync_overtime',
        }
        send_notification(user, notification_data)
