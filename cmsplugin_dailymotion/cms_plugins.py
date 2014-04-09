from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import DailymotionViewer


class DailymotionViewerPlugin(CMSPluginBase):
    model = DailymotionViewer
    name = _("Dailymotion viewer")
    render_template = "cmsplugin_dailymotion/dailymotion_viewer.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder
        })
        return context

plugin_pool.register_plugin(DailymotionViewerPlugin)
