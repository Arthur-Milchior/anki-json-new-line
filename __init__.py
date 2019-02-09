# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# Based on anki code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Source in https://github.com/Arthur-Milchior/anki-json-new-line
import json
import re

oldLoads = json.loads


def newLoads(t, *args, **kwargs):
    t_ = correctJson(t)
    res = oldLoads(t_, *args, **kwargs)
    return res


json.loads = newLoads


def correctJson(text):
    """Text, with new lines replaced by \n when inside quotes"""
    def correctQuotedString(match):
        string = match[0]
        return string.replace("\n", "\\n")
    res = re.sub(r'"(?:(?<=[^\\])(?:\\\\)*\\"|[^"])*"',
                 correctQuotedString, text, re.M)
    return res


def readableJson(text):
    """Text, where \n are replaced with new line. Unless it's preceded by a odd number of \."""
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
