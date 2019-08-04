#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from jinja2 import environmentfilter, Environment, Markup


@environmentfilter
def render_people(environment: Environment, people):
    template = environment.get_template("widgets/people-card.template.html")
    output_text = template.render({"people": people})
    return Markup(output_text)
