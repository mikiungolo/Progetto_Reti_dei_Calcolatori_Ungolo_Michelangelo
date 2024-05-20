from django.db import models

# Create your models here.
CHAR_FIELD_LENGHT = 20
CHAR_EXTENSION_LENGHT = 4


# User Model with main component to authenticate with 2FA
class User(models.Model):
    username = models.CharField(max_length = CHAR_FIELD_LENGHT)
    name = models.CharField(max_length = CHAR_FIELD_LENGHT)
    surname = models.CharField(max_length = CHAR_FIELD_LENGHT)
    password = models.CharField(max_length = CHAR_FIELD_LENGHT)
    email = models.EmailField()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


# File Model to track download
class File(models.Model):
    identifier = models.CharField(max_length = CHAR_FIELD_LENGHT)
    extension = models.CharField(max_length = CHAR_EXTENSION_LENGHT)
    users = models.ManyToManyField(User, related_name = "files")

    def __str__(self):
        return self.identifier.name + '.' + self.extension.name

    class Meta:
        verbose_name = "file"
        verbose_name_plural = "files"