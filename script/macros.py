#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from jinja2 import environmentfilter, Environment, Markup


@environmentfilter
def render_people(environment: Environment, people):
    template = environment.get_template("widgets/people-card.template.html")
    output_text = template.render({"people": people})
    return Markup(output_text)


@environmentfilter
def anchor(_, text):
    # TODO Sanitize when needed
    return text


@environmentfilter
def as_event(_, code, events):
    for event in events:
        if event["code"] == code:
            return event["label"]
    return code
