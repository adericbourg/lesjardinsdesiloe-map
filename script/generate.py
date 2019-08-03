#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import jinja2
import os
import settings
import shutil
import sys
from typing import Dict


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


def generate(output_dir: str):
    print(f"""Generating site "{settings.SITE_NAME}" into "{os.path.abspath(output_dir)}" """)
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)

    _render_template(template_env, "index.template.html", os.path.join(output_dir, "index.html"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing output directory")
        sys.exit(1)
    generate(sys.argv[1])
