from __future__ import unicode_literals
from rest_framework.routers import DefaultRouter
from django.conf.urls import *
from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.urlpatterns import format_suffix_patterns

import logging
logger = logging.getLogger('tasks')

class CustomRouter(DefaultRouter):
    """
    The default router extends the SimpleRouter, but also adds in a default
    API root view, and adds format suffix patterns to the URLs.
    """
    include_root_view = True
    include_format_suffixes = True
    root_view_name = 'api-root'

    def get_api_root_view(self):
        """
        Return a view to use as the API root.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse(url_name, request=request, format=format)
                ret['toast-apps'] = reverse('toast-apps-api', request=request)
                ret['nearby-shops'] = reverse('nearby-shops-api', request=request)

                return Response(ret)

        return APIRoot.as_view()

    def get_urls(self):
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = []

        if self.include_root_view:
            root_url = url(r'^$', self.get_api_root_view(), name=self.root_view_name)
            urls.append(root_url)
        default_urls = super(DefaultRouter, self).get_urls()
        urls.extend(default_urls)
        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls)

        return urls
