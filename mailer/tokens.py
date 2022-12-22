from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import safestring
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            safestring.SafeText(user.pk) + safestring.SafeText(timestamp) +
            safestring.SafeText(user.is_active)
        )
account_activation_token = TokenGenerator()