# -*- coding: utf-8 -*-
from rest_framework import permissions


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Permission to only allow owners of a resource to modify it
    Assumes the view will receive a 'username' kwarg
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.user and request.user.is_authenticated()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow owners of a resource to modify it
    Assumes the view will receive a 'username' kwarg
    """

    def has_permission(self, request, view):
        if view.kwargs.get('username', None) and request.method not in permissions.SAFE_METHODS:
            return request.user.username == view.kwargs['username']
        return True


class IsOwner(permissions.BasePermission):
    """
    Permission to only allow owners of a resource to access it
    Assumes the view will receive a 'username' kwarg
    """

    def has_permission(self, request, view):
        if view.kwargs.get('username', None):
            return request.user.username == view.kwargs['username']
        return True

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owned_by'):
            return obj.owned_by(request.user)
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        else:
            return False
