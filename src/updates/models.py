from django.core.serializers import serialize
import json
from django.conf import settings
from django.db import models


def upload_update_image(instance, filename):
    return "updates/{user}/{filename}".format(user=instance.user, filename=filename)

# Create your models here.


class UpdateQuerySet(models.QuerySet):
    def serialize(self):
        # return serialize("json", self, fields=("user", "content", "image"))
        return json.dumps(list(self.values("user", "content", "image", "id")))


class UpdateManager(models.Manager):
    def get_queryset(self):
        return UpdateQuerySet(self.model, using=self._db)


class Update(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True,
                              upload_to=upload_update_image)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UpdateManager()

    def __str__(self):
        return self.content or ""

    def serialize(self):
        try:
            image = self.image.url
        except ValueError:
            image = ""
        data = {
            "id": self.id,
            "user": self.user.id,
            "content": self.content,
            "image": image
        }
        # return serialize("json", [data], fields=("user", "content", "image"))
        return json.dumps(data)
