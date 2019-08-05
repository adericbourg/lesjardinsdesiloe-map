#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from collections import namedtuple
from typing import Optional

import requests

Coordinates = namedtuple('Coordinates', ['lat', 'lon'])


def lookup(address_query: str) -> Optional[Coordinates]:
    result = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={address_query}")
    if result.status_code < 400:
        content = json.loads(result.content)
        content = sorted(content, key=lambda line: line["importance"], reverse=True)
        if len(content) > 0:
            address = content[0]
            if len(content) > 1:
                print(f"Found several places for address '{address_query}':")
                for o in content[1:]:
                    print(f"  {o}")
            return Coordinates(address["lat"], address["lon"])
        print(f"Address not found: '{address_query}' (got {len(content)} results): \n{content}")
    return None
