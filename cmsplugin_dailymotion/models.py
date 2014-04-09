import os
import re
import urllib

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin


class DailymotionViewer(CMSPlugin):
    """
    Plugin for embedding a Dailymotion video.
    """
    video_src = models.URLField(_('video address'))
    width = models.CharField(_('width'), max_length=6, default='100%', validators=[RegexValidator(r'\d+(px|\%)')], help_text=_('Width in pixels or percent'))
    allow_fullscreen = models.BooleanField(_('allow fullscreen'), default=True)
    start_at = models.PositiveIntegerField(_('start at'), blank=True, null=True, help_text=_('Start delay in seconds'))
    auto_start = models.BooleanField(_('auto start'), blank=True, default=False)

    @property
    def src(self):
        kwargs = dict()
        if self.start_at:
            kwargs['start'] = self.start_at
        if self.auto_start:
            kwargs['autoPlay'] = 1
        base_url = self.get_base_url()
        return '{0}{1}'.format(base_url, '?{0}'.format(urllib.urlencode(kwargs)) if kwargs else '')

    def get_base_url(self):
        short = re.findall(r'://dai\.ly/([a-zA-Z0-9]+)', self.video_src)
        if short:
            return 'http://www.dailymotion.com/embed/video/{0}'.format(short[0])
        classic = re.findall(r'dailymotion.com/video/([a-zA-Z0-9]+)?', self.video_src)
        if classic:
            return 'http://www.dailymotion.com/embed/video/{0}'.format(classic[0])
        return self.video_src

    def __unicode__(self):
        return self.video_src
