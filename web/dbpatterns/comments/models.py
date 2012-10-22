from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from gravatar.templatetags.gravatar import gravatar_for_email
from auth.models import AnonymousProfile

class Comment(dict):
    # dictionary-like object for mongodb documents.
    __getattr__ = dict.get

    @property
    def profile_url(self):
        return reverse("auth_profile", args=[self.user.username])

    @property
    def avatar_url(self):
        return gravatar_for_email(self.user.email, size=40)

    @property
    def user(self):
        if not self._cached_user:
            self._cached_user = self.get_user()

        return self._cached_user

    def get_user(self):
        try:
            User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return AnonymousProfile()