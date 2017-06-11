import calendar


def serialize_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'mobile_number': user.mobile_number,
        'no_file': user.no_file,
        'type': user.type,
        'position': user.position or None,
        'department': user.department or None,
    }


def serialize_overtime(overtime):
    return {
        'id': overtime.id,
        'user': serialize_user(overtime.user),
        'start': calendar.timegm(overtime.start.utctimetuple()),
        'end': calendar.timegm(overtime.end.utctimetuple()),
        'created': calendar.timegm(overtime.created.utctimetuple()),
        'description': overtime.description or None,
        'notes_coordinator': overtime.notes_coordinator or None,
        'notes_manager': overtime.notes_manager or None,
        'status': overtime.status,
    }
