# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# Based on anki code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Source in https://github.com/Arthur-Milchior/anki-json-new-line
import json
import sys

from aqt.addons import AddonManager, ConfigEditor

# Addon number 112201952


oldLoads = json.loads


def newLoads(t, *args, **kwargs):
    t = correctJson(t)
    return oldLoads(t, *args, **kwargs)


json.loads = newLoads


def correctJson(text):
    l = []
    numberOfSlashOdd = False
    numberOfQuoteOdd = False
    for char in text:
        if char == "\n" and numberOfQuoteOdd:
            l.append("\\n")
        else:
            l.append(char)
            if char == "\n":
                char = "newline"

        if char == "\"":
            if not numberOfSlashOdd:
                numberOfQuoteOdd = not numberOfQuoteOdd

        if char == "\\":
            numberOfSlashOdd = not numberOfSlashOdd
        else:
            numberOfSlashOdd = False
    return "".join(l)


def readableJson(text):
    l = []
    numberOfSlashOdd = False
    numberOfQuoteOdd = False
    for char in text:
        if char == "n" and numberOfQuoteOdd and numberOfSlashOdd:
            l[-1] = "\n"
        else:
            l.append(char)
            if char == "\n":
                char = "newline"

        if char == "\"":
            if not numberOfSlashOdd:
                numberOfQuoteOdd = not numberOfQuoteOdd

        if char == "\\":
            numberOfSlashOdd = not numberOfSlashOdd
        else:
            numberOfSlashOdd = False
    return "".join(l)


def updateText(self, conf):
    self.form.editor.setPlainText(
        readableJson(json.dumps(conf, sort_keys=True, indent=4, separators=(',', ': '))))


ConfigEditor.updateText = updateText
