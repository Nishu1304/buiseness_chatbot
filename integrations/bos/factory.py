from django.conf import settings
from .auth import BOSAuth
from .client import BOSClient

_auth = BOSAuth()
_client = None


def get_bos_client():
    global _client
    if _client is None:
        _client = BOSClient(
            base_url=settings.BOS_BASE_URL,
            auth=_auth,
        )
    return _client