# -*- coding: utf-8 -*-

__all__ = ['servicemethod']


def servicemethod(fn):
    fn.service_method = True
    return fn
