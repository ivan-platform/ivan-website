from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, username, password, email=None, first_name=None, last_name=None,
                    is_organization_admin=False, is_active=False,
                    is_staff=False, is_admin=False):
        if not username:
            raise ValueError("Users must have an username")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            username = username,
            password = password,
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.organization_admin = is_organization_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_organization_admin(self, username, password, email=None):
        user = self.create_user( username=username,
                                 password=password,
                                 email=email,
                                 is_organization_admin=True
        )
        return user

    def create_superuser(self, username, password, email=None, first_name=None, last_name=None):
        user = self.create_user(
                username,
                password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_admin=True,
                is_active=True,
        )
        return user


# class Organization(models.Model):
#     # user = models.ForeignKey(User, related_name="org_user", on_delete=models.DO_NOTHING, null=True)
#     organization_name = models.CharField(max_length=250,  null=True, blank=True)
#     organization_address = models.CharField(max_length=250,  null=True, blank=True)
#
#     # designation = models.DateTimeField(auto_now_add=True)
#     # department = models.DateTimeField(auto_now_add=False, null=True, blank=True)
#     active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def str(self):
#         return '{}'.format(self.organization_name)

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class User(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=255, unique=False, blank=True)
    mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    organization_admin = models.BooleanField(default=False, blank=True)
    is_staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #organization = models.ForeignKey(Organization, related_name="org_user", on_delete=models.SET_NULL, null=True, blank=True)
    organization_name = models.CharField(max_length=250, null=True, blank=True)
    organization_address = models.CharField(max_length=250, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_organization_admin(self):
        return self.organization_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

#
# class DockerImage(models.Model):
#     user = models.ForeignKey(User, related_name="container_owner", on_delete=models.DO_NOTHING, null=True)
#     base_image_name = models.CharField(max_length=250, blank=True, null=True)
#     new_image_name = models.CharField(max_length=250, blank=True, null=True)
#     extra_command = models.CharField(max_length=250, blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=250, choices=(
#         ("Already Build", "Already Build"),("Ready To Build", "Ready To Build")
#     ), default="Available", blank=True, null=True)
#
#     active = models.BooleanField(default=True)
#
#     def str(self):
#         return self.new_image_name
#
#
# class DockerContainers(models.Model):
#     user = models.ForeignKey(User, related_name="container_owner", on_delete=models.DO_NOTHING, null=True)
#     container_id = models.CharField(max_length=25, blank=True, null=True)
#     image = models.CharField(max_length=250, blank=True, null=True)
#     command = models.CharField(max_length=250, blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=250, choices=(("running", "running"),("stop", "stop")), default="Completed", blank=True, null=True)
#     ports = models.CharField(max_length=250, blank=True, null=True)
#     names = models.CharField(max_length=250, blank=True, null=True)
#
#     active = models.BooleanField(default=True)
#
#     def str(self):
#         return str(self.id)
#
#
# class DockerUsage(models.Model):
#     container = models.ForeignKey(DockerContainers, related_name="container_usage", on_delete=models.DO_NOTHING, null=True)
#     start_time = models.DateTimeField(auto_now_add=True)
#     stop_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
#     uptime = models.BigIntegerField(null=True, blank=True)
#     charge = models.BigIntegerField(null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def str(self):
#         return self.container

class App(models.Model):
    user = models.ForeignKey(User, related_name="app_owner", on_delete=models.DO_NOTHING, null=True)
    app_name = models.CharField(max_length=100, blank=True, null=True)
    app_description = models.CharField(max_length=100, blank=True, null=True)
    git_repo_url = models.CharField(max_length=250, blank=True, null=True)
    uses_database = models.BooleanField(default=False)
    # image_type = models.CharField(max_length=100, default="pre build",
    #                               choices=(("pre build", "pre build"),("user build", "user build")))
    # upload_shiny_docker_file = models.FileField(upload_to='docker/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.app_name)


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
        return str(self.id)


class DockerUsage(models.Model):
    container = models.ForeignKey(DockerContainers, related_name="container_usage", on_delete=models.DO_NOTHING, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    uptime = models.BigIntegerField(null=True, blank=True)
    charge = models.BigIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.container


