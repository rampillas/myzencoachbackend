# -*- coding: utf-8 -*-


class DescriptionPerViewMixin(object):
    views_descriptions = {}

    def get_view_description(self, html=False):

        suffix = getattr(self, 'suffix', None)
        if suffix:
            suffix = suffix.lower()

        DescriptionExtension = type('DescriptionExtension', (self.__class__,), {
            '__doc__': self.views_descriptions.get(suffix, '')
        })

        func = self.settings.VIEW_DESCRIPTION_FUNCTION
        return func(DescriptionExtension, html)
