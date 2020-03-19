# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# Based on anki code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Source in https://github.com/Arthur-Milchior/anki-json-new-line
# Addon number 11201952
import json
import re
import sys

from aqt.addons import AddonManager, ConfigEditor
from aqt import gui_hooks

not_special = '[^\\\\"]'
escaped_quote = '\\"'
escape_character = '\\\\'
inside_char = f'(?:{not_special}|{escape_character}|{escaped_quote}|\n)'
inside_string = f'(?:{inside_char}*)'
string = f'"{inside_string}"'

def correctJson(text):
    """Text, with new lines replaced by \n when inside quotes"""
    if not isinstance(text, str):
        return text

    def correctQuotedString(match):
        string = match[0]
        ret = string.replace("\n", "\\n")
        return ret
    res = re.sub(string,
                 correctQuotedString, text, re.M)
    return res
gui_hooks.addon_config_editor_will_save_json.append(correctJson)

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
gui_hooks.addon_config_editor_will_display_json.append(readableJson)
