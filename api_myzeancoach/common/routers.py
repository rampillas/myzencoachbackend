# -*- coding: utf-8 -*-
from rest_framework_nested.routers import *


class CustomNestedSimpleRouter(NestedSimpleRouter):
    """
    Router to be nested inside other router.
    Allows having nested resources endpoints, such as:

    * v3/messages/<?uuid>/nodes/<?node_uuid>/

    """

    def __init__(self, parent_router, parent_prefix, *args, **kwargs):
        """ Create a CustomNestedSimpleRouter nested within `parent_router`
        Args:

        parent_router: Parent router. Mayb be a simple router or another nested
            router.

        parent_prefix: The url prefix within parent_router under which the
            routes from this router should be nested.

        lookup:
            The regex variable that matches an instance of the parent-resource
            will be called '<lookup>_<parent-viewset.lookup_field>' if <lookup> is different from the empty string,
            else it wil be called <parent-viewset.lookup_field>.
            In the example above, lookup=domain and the parent viewset looks up
            on 'pk' so the parent lookup regex will be 'domain_pk'.
            Default: 'nested_<n>' where <n> is 1+parent_router.nest_count

        """
        self.parent_router = parent_router
        self.parent_prefix = parent_prefix
        self.nest_count = getattr(parent_router, 'nest_count', 0) + 1
        self.nest_prefix = kwargs.pop('lookup', 'nested_%i' % self.nest_count)
        if self.nest_prefix:
           self.nest_prefix += '_'
        super(NestedSimpleRouter, self).__init__(*args, **kwargs)
        parent_registry = [registered for registered in self.parent_router.registry if registered[0] == self.parent_prefix]
        try:
            parent_registry = parent_registry[0]
            parent_prefix, parent_viewset, parent_basename = parent_registry
        except:
            raise RuntimeError('parent registered resource not found')

        nested_routes = []
        parent_lookup_regex = parent_router.get_lookup_regex(parent_viewset, self.nest_prefix)

        self.parent_regex = '{parent_prefix}/{parent_lookup_regex}/'.format(
            parent_prefix=parent_prefix,
            parent_lookup_regex=parent_lookup_regex
        )
        if hasattr(parent_router, 'parent_regex'):
            self.parent_regex = parent_router.parent_regex+self.parent_regex

        for route in self.routes:
            route_contents = route._asdict()

            # This will get passed through .format in a little bit, so we need
            # to escape it
            escaped_parent_regex = self.parent_regex.replace('{', '{{').replace('}', '}}')

            route_contents['url'] = route.url.replace('^', '^'+escaped_parent_regex)
            nested_routes.append(type(route)(**route_contents))

        self.routes = nested_routes

