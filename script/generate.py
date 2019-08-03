#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import jinja2
import os
import settings
import shutil
import sys


def generate(output_dir: str):
    print(f"""Generating site "{settings.SITE_NAME}" into "{os.path.abspath(output_dir)}" """)
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template("index.template.html")
    output_text = template.render({
        "site": {
            "title": settings.SITE_NAME,
            "root_url": settings.ROOT_URL
        }
    })

    with open(f"{output_dir}/index.html", "w") as fh:
        fh.write(output_text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing output directory")
        sys.exit(1)
    generate(sys.argv[1])
