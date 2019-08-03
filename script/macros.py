#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from jinja2 import evalcontextfilter, Markup


@evalcontextfilter
def render_people(_, people):
    if "name" in people:
        name = people["name"]
    else:
        "Personne non-identifiée"
    result = f"{ name }"
    return Markup(result)
