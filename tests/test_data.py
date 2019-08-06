#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import unittest

import yaml


class TestData(unittest.TestCase):
    """Check data consistency"""

    def test_all_people_should_have_an_address_or_an_event(self):
        with open(f"content/people.yml", "r") as f:
            all_people = yaml.load(f, Loader=yaml.SafeLoader)["people"]
        for people in all_people:
            name = people["name"]
            self.assertTrue(
                "address" in people or ("events" in people and len(people["events"]) > 0),
                f"Empty data for {name}")

    @staticmethod
    def _load_events():
        with open(f"content/reference.yml", "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)["events"]

    def test_events_should_have_a_code(self):
        events = self._load_events()
        for event in events:
            self.assertIn("code", event)

    def test_events_should_have_a_label(self):
        events = self._load_events()
        for event in events:
            self.assertIn("label", event)

    def test_all_events_should_have_a_distinct_code(self):
        events = self._load_events()
        event_codes = set()
        for event in events:
            code = event["code"]
            if code in event_codes:
                self.assertNotIn(event["code"], event_codes, f"Duplicate event code: '{code}'")
            event_codes.add(code)
