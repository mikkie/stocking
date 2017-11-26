# -*-coding=utf-8-*-
__author__ = 'aqua'


def inner(**kw):
    print(kw['kw']['code'])

def wrappr(name,**kw):
    print(name)
    inner(kw=kw)

wrappr('li',code = '123')    