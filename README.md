-*- coding: utf-8 -*-
Copyright: Arthur Milchior <arthur@milchior.fr>
Based on anki code by Damien Elmes <anki@ichi2.net>
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in https://github.com/Arthur-Milchior/anki-json-new-line
Addon number 112201952


Allow newline in strings in the json part of the configuration of add-ons.

In standard json, string should not contain newlines. They should
contain "\n" instead. Which clearly create a readability problem.

This add-on allow you to write new line in your string. The add-on
will replace them by "\n" before json load the configuration. This
works both for configuration in the file meta.json, and for the the
add-on manager's configuration editor.

Furthermore, the add-on manager's configuration editor will show new
line (instead of \n) in the strings. Which will keep the configuration
more readable.

Note that it will also put newlines in the configuration written
in meta.conf. Indeed, this would create at least two problems:
*we can't control the order in which add-ons are loaded. Thus all
add-ons loaded before this current add-on would fail when trying to
read their configuration.
*if you decide to uninstall this add-on, no configuration with new
lines could be read anymore. (In particular, this would happen if you
synchronize your configuration using another add-on).
