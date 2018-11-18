# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior <arthur@milchior.fr>
# Based on anki code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Source in https://github.com/Arthur-Milchior/anki-json-new-line
# Addon number ????????????
import json
import sys

from aqt.addons import AddonManager, ConfigEditor


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


def addonMeta(self, dir):
    path = self._addonMetaPath(dir)
    try:
        with open(path, encoding="utf8") as f:
            t = f.read()
            t = correctJson(t)
            j = json.loads(t)
            if not isinstance(j, dict):
                raise Exception(f"Invalid configuration {j} in {dir}.")
            return j
    except:
        return dict()


AddonManager.addonMeta = addonMeta


def writeAddonMeta(self, dir, meta):
    path = self._addonMetaPath(dir)
    meta = json.dumps(meta)
    meta = readableJson(meta)
    with open(path, "w", encoding="utf8") as f:
        f.write(meta)
# AddonManager.writeAddonMeta=writeAddonMeta


def updateText(self, conf):
    self.form.editor.setPlainText(
        readableJson(json.dumps(conf, sort_keys=True, indent=4, separators=(',', ': '))))


ConfigEditor.updateText = updateText


def accept(self):
    txt = self.form.editor.toPlainText()
    try:
        new_conf = json.loads(correctJson(txt))
        if not isinstance(new_conf, dict):
            showInfo(
                _("Invalid configuration: Configurations should be dictionnaries."))
            return
    except Exception as e:
        showInfo(_("Invalid configuration: ") + repr(e))
        return

    if new_conf != self.conf:
        self.mgr.writeConfig(self.addon, new_conf)
        # does the add-on define an action to be fired?
        act = self.mgr.configUpdatedAction(self.addon)
        if act:
            act(new_conf)

    super(ConfigEditor, self).accept()


ConfigEditor.accept = accept
