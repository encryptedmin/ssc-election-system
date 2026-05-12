from django.contrib.auth.decorators import user_passes_test


def super_admin_required(view_func):

    decorated_view = user_passes_test(
        lambda user: (
            user.is_authenticated and
            user.role == 'SUPER_ADMIN'
        )
    )(view_func)

    return decorated_view


def admin_required(view_func):

    decorated_view = user_passes_test(
        lambda user: (
            user.is_authenticated and
            user.role in [
                'SUPER_ADMIN',
                'ADMIN',
            ] and user.is_approved
        )
    )(view_func)

    return decorated_view