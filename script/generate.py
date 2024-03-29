#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import os

import jinja2
import macros

if "DEVSETTINGS" in os.environ:
    import devsettings as settings
else:
    import settings
import shutil
import sys
from typing import Dict, List
import yaml
import nominatim
from itertools import groupby


def _read_yaml(file: str) -> Dict:
    with open(f"content/{file}", "r") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def _load_content() -> Dict:
    # Raw and exhaustive: might be good to sanitize this some day
    content = {
        **_read_yaml("reference.yml"),
        **_read_yaml("people.yml"),
    }
    attendees = {}
    for people in content["people"]:
        if "events" in people:
            for event in people["events"]:
                code = event["code"]
                date = event["date"]
                if not code in attendees:
                    attendees[code] = {}
                if not date in attendees[code]:
                    attendees[code][date] = list()
                attendees[code][date].append(people)
    content["attendees"] = attendees
    return content


def _render_template(env: jinja2.Environment, template: str, output: str, data: Dict = {}):
    template = env.get_template(template)
    output_text = template.render({
        "site": {
            "title": settings.SITE_NAME,
            "root_url": settings.ROOT_URL
        },
        "page": data
    })

    with open(output, "w") as fh:
        fh.write(output_text)


def _generate_events(env: jinja2.Environment, output: str, data: Dict):
    events_path = os.path.join(output, "events")
    os.mkdir(events_path)

    _render_template(env, "events/index.template.html", os.path.join(events_path, "index.html"), data)
    for event in data["events"]:
        event_code = event["code"]
        if event_code in data["attendees"]:
            attendees = data["attendees"][event_code]
        else:
            attendees = {}
        _render_template(env, "events/detail.template.html", os.path.join(events_path, f"{event_code.lower()}.html"), {
            "event": event,
            "attendees": attendees
        })


def _group_people_by_geolocation(geocoded_people: List[Dict]) -> List[Dict]:
    sorted_input = sorted(geocoded_people, key=lambda p: p["coordinates"])
    groups = groupby(sorted_input, key=lambda p: p["coordinates"])
    grouped = [{'location': k, 'people': [x for x in v]} for k, v in groups]
    return grouped


def _geocode_people(people: List[Dict]) -> List[Dict]:
    geocoded_people = []
    for p in people:
        if "address" in p:
            address = p["address"]
            geo_result = nominatim.lookup(address)
            if geo_result:
                p["coordinates"] = geo_result
                geocoded_people.append(p)

    return _group_people_by_geolocation(geocoded_people)


def _render_map(env: jinja2.Environment, output_dir: str, content: Dict):
    geocoded_people = _geocode_people(content["people"])
    _render_template(env, "map.template.html", os.path.join(output_dir, "map.html"), {
        "people": geocoded_people,
        "events": content["events"]
    })


def _copy_static(output_dir: str):
    shutil.copytree("static", os.path.join(output_dir, "static"))


def generate(output_dir: str):
    print(f"""Generating site "{settings.SITE_NAME}" into "{os.path.abspath(output_dir)}" """)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    content = _load_content()

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_env.filters["anchor"] = macros.anchor
    template_env.filters["as_event"] = macros.as_event
    template_env.filters["render_people"] = macros.render_people

    _generate_events(template_env, output_dir, content)
    _render_map(template_env, output_dir, content)
    _render_template(template_env, "index.template.html", os.path.join(output_dir, "index.html"))
    _copy_static(output_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing output directory")
        sys.exit(1)
    generate(sys.argv[1])
