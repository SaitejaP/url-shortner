import uuid

from django.conf import settings
from django.db import models


class URLMapper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    long_url = models.URLField(max_length=500, db_index=True, unique=True)
    short_url = models.URLField(db_index=True, unique=True)

    def serializer(self):
        return {
            "created_on": self.created_on,
            "updated_on": self.updated_on,
            "long_url": self.long_url,
            "short_url": '%s/%s/' % (settings.DOMAIN_URL, self.short_url)
        }


class URLDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url_mapping = models.ForeignKey(URLMapper, models.SET_NULL, null=True)
    visited_on = models.DateTimeField(auto_now=True)
