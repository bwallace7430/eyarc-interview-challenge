from rest_framework.authentication import BaseAuthentication


class _DevUser:
    """Minimal user-like object that satisfies IsAuthenticated."""

    is_authenticated = True
    is_active = True
    pk = 0


_dev_user = _DevUser()


class DevStudentAuthentication(BaseAuthentication):
    """Always authenticates as the dev student — no credentials required."""

    def authenticate(self, request):
        return (_dev_user, None)
