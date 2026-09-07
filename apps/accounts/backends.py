import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import IntegrityError

logger = logging.getLogger(__name__)

class PersistentAuthBackend(ModelBackend):
    """
    Robust authentication backend that handles email-based login (case-insensitive)
    and provides resilient session restoration on serverless instances.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        email = kwargs.get('email') or username
        if email is None:
            return None
        
        email = email.strip().lower()
        try:
            # Case-insensitive email or username lookup
            user = UserModel.objects.filter(email__iexact=email).first()
            if not user:
                user = UserModel.objects.filter(username__iexact=email).first()
            
            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception as e:
            logger.warning(f"Auth error during authenticate: {e}")
            return None
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(pk=user_id).first()
            if not user and isinstance(user_id, str) and '@' in user_id:
                user = UserModel.objects.filter(email__iexact=user_id).first()
            if user and self.user_can_authenticate(user):
                return user
            return user if user else None
        except Exception as e:
            logger.warning(f"Auth error in get_user: {e}")
            return None
