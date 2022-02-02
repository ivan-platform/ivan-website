from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, first_name=None, last_name=None, password=None, is_active=False, is_staff=False, is_admin=False):
        if not username:
            raise ValueError("Users must have an username")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            username = self.normalize_email(username),
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = True
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, first_name=None, last_name=None, password=None):
        user = self.create_user(
                username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_staff=True,
                is_admin=True,
                is_active=True,
        )
        return user


class User(AbstractBaseUser):
    username = models.EmailField(max_length=255, unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    alternate_mobile = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

#
# class DockerImage(models.Model):
#     user = models.ForeignKey(User, related_name="container_owner", on_delete=models.DO_NOTHING, null=True)
#     image_name = models.CharField(max_length=250, blank=True, null=True)
#     extra_command = models.CharField(max_length=250, blank=True, null=True)
#     description = models.CharField(max_length=250, blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=250, choices=(
#         ("Already Build", "Already Build"),("Ready To Build", "Ready To Build")
#     ), default="Available", blank=True, null=True)
#
#     active = models.BooleanField(default=True)
#
#     def str(self):
#         return self.image_name

class DockerContainers(models.Model):
    user = models.ForeignKey(User, related_name="container_owner", on_delete=models.DO_NOTHING, null=True)
    container_id = models.CharField(max_length=25, blank=True, null=True)
    image = models.CharField(max_length=250, blank=True, null=True)
    command = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250, choices=(("running", "running"),("stop", "stop")), default="Completed", blank=True, null=True)
    ports = models.CharField(max_length=250, blank=True, null=True)
    names = models.CharField(max_length=250, blank=True, null=True)

    active = models.BooleanField(default=True)

    def str(self):
        return self.container_id


class DockerUsage(models.Model):
    container = models.ForeignKey(DockerContainers, related_name="container_usage", on_delete=models.DO_NOTHING, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    uptime = models.BigIntegerField(null=True, blank=True)
    charge = models.BigIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.container_id