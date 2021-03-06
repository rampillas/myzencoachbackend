# -*- coding: utf-8 -*-
from rest_framework import permissions


class IsAuthenticatedOrCreateOrRecoverOnly(permissions.BasePermission):
    """
    Permission to only allow owners of a resource to modify it
    Assumes the view will receive a 'username' kwarg
    """

    def has_permission(self, request, view):
        if view.action in {'create', 'set_password'} or request.method == 'OPTIONS':
            return True
        return request.user and request.user.is_authenticated()


class IsOwnerOrReadOrRecoverOnly(permissions.BasePermission):
    """
    Permission to only allow owners of a resource to modify it
    Assumes the view will receive a 'username' kwarg
    """

    def has_permission(self, request, view):
        if (view.kwargs.get('username', None)):
            return request.user.username == view.kwargs['username']
        return True

    def has_permission(self, request, view):
        if (
                view.kwargs.get('username', None) and (
                    (view.action not in ['set_password'] and
                            request.method not in permissions.SAFE_METHODS)
                )
        ):
            return request.user.username == view.kwargs['username']
        return True