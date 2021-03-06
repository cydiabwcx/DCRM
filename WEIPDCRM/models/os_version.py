# coding:utf-8

"""
DCRM - Darwin Cydia Repository Manager
Copyright (C) 2017  WU Zheng <i.82@me.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals

from django.db import models
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.core.validators import validate_slug


class OSVersion(models.Model):
    """
    For DCRM Compatibility Module
    This model manages all iOS Versions.
    """
    class Meta(object):
        verbose_name = _("iOS Version")
        verbose_name_plural = _("iOS Versions")

    # Base Property
    id = models.AutoField(primary_key=True, editable=False)
    enabled = models.BooleanField(verbose_name=_("Enabled"), default=True)
    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True,
    )
    descriptor = models.CharField(
        verbose_name=_("Version"),
        max_length=255,
        help_text=_("Example: 10.2")
    )
    build = models.CharField(
        verbose_name=_("Build"),
        max_length=255,
        help_text=_("Example: 14C92/11A466"),
    )

    # Warning: this field will store icon/file relative to MEDIA_URL,
    #          defined in settings.py.
    icon = models.FileField(
        verbose_name=_("Icon"),
        max_length=255,
        upload_to="os-icons",
        help_text=_("Choose an Icon (*.png) to upload"),
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.descriptor + " (" + self.build + ")"

    def get_admin_url(self):
        """
        :return: URL String
        :rtype: str
        """
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,)
        )
