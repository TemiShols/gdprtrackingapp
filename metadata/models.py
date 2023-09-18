from django.db import models
from authentication.models import CustomUser


class Chrome(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    pc_username = models.CharField(max_length=120, blank=True, null=True)
    user = models.ForeignKey(CustomUser, related_name='chrome_user', on_delete=models.PROTECT, blank=True, null=True)
    cookies = models.ManyToManyField('Cookie')
    downloads = models.ManyToManyField('Download')
    history = models.ManyToManyField('History')
    logins = models.ManyToManyField('LoginItem')
    storages = models.ManyToManyField('LocalStorage')

    def __str__(self):
        return self.pc_username


class Download(models.Model):
    user = models.ForeignKey(CustomUser, related_name='download_user', on_delete=models.PROTECT)
    download_id = models.CharField(max_length=25, blank=True, null=True)
    download_url = models.CharField(max_length=25, blank=True, null=True)
    download_target_path = models.CharField(max_length=25, blank=True, null=True)
    download_danger_type = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.download_url


class Cookie(models.Model):
    #   creation_time = models.CharField(max_length=25, blank=True, null=True)  # timestamp_desc
    user = models.ForeignKey(CustomUser, related_name="cookie_owner", on_delete=models.PROTECT)
    name = models.CharField(max_length=25, blank=True, null=True)
    value = models.CharField(max_length=25, blank=True, null=True)
    path = models.CharField(max_length=25, blank=True, null=True)
    priority = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.name


class History(models.Model):
    user = models.ForeignKey(CustomUser, related_name='history_owner', on_delete=models.PROTECT)
    url = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=25, blank=True, null=True)
    visit_time = models.CharField(max_length=25, blank=True, null=True)
    visit_source = models.CharField(max_length=25, blank=True, null=True)
    visit_duration = models.CharField(max_length=25, blank=True, null=True)
    visit_count = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.title


class LoginItem(models.Model):
    creation_time = models.CharField(max_length=25, blank=True, null=True)
    name = models.CharField(max_length=25, blank=True, null=True)
    value = models.CharField(max_length=25, blank=True, null=True)
    count = models.CharField(max_length=25, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    interpretation = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.name


class LocalStorage(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    origin = models.CharField(max_length=25, blank=True, null=True)
    key = models.CharField(max_length=25, blank=True, null=True)
    value = models.CharField(max_length=25, blank=True, null=True)
    source_path = models.CharField(max_length=55, blank=True, null=True)

    def __str__(self):
        return self.origin
