#!/usr/bin/python
###
# Copyright 2013 Gary Wright
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# http://static.wrightsolutions.co.uk/guide/code/python/
# www.wrightsolutions.co.uk/contact
# V1.0 20130926GW Useful for Wheezy or Squeeze questions.
###

"""
Takes the [saved] output of dpkg --get-selections
and reports 'wheezy' or 'squeeze'
as best guess of the installed system.

Limitations: makes no distinction between 'install' and 'deinstall'
in the input file.
Might make a marginal difference to detection of 'wheezy'.
"""

#import apt
import sys, fileinput
import logging as l    # avoid reserved mathematical word 'log'

"""
# Log to stderr - leaving the output uncluttered and suitable for input to dpkg.
l.basicConfig(level=l.DEBUG)
debug = 3    # 2 rather than 1 gives you more chat. 3 for testing. 0 for silence.

all_packages = apt.Cache()
installed_packages = [i for i in all_packages if i.is_installed]
"""

install_list = []
for line in fileinput.input():
    line_split = line.strip().split('\t')     # last word on the line is the action
    pkgname = line_split[0]
    action = line_split[-1]
    if action == 'install':
        if ':' in pkgname:
            pkgname = pkgname.strip().split(':')[0]
        install_list.append(pkgname)
    #if debug > 3: l.debug(action)


""" score_new_old - positive leans towards 'wheezy'
negative leans towards a guess of 'squeeze'.
guesswork!!! will be output where score is close to zero
"""
score_new_old = 0

if 'libept1.4.12' in install_list:
	score_new_old += 1
elif 'libept1' in install_list:
	score_new_old -= 1
else:
	pass

if 'libdrizzle4' in install_list:
	score_new_old += 1
elif 'libdrizzle0' in install_list:
	score_new_old -= 1
else:
	pass

if 'libopus0' in install_list:
	score_new_old += 1
elif 'libcelt-0-0' in install_list:
	score_new_old -= 1
else:
	pass

if 'libgmp10' in install_list:
	score_new_old += 1
elif 'libgmp3' in install_list:
	score_new_old -= 1
else:
	pass

if 'libdb5.1' in install_list:
	score_new_old += 1
elif 'libdb4.6' in install_list:
	score_new_old -= 1
else:
	pass

if 'linux-image-3.2' in install_list:
	score_new_old += 1
elif 'linux-image-2.6' in install_list:
	score_new_old -= 1
else:
	pass

#print score_new_old

if score_new_old < 0:
	report_string = 'squeeze'
elif score_new_old > 0:
	report_string = 'wheezy'
else:
	report_string = 'difficult to say - sorry'

if abs(score_new_old) == 1:
	report_string += ' (guesswork!!!)'

print "### %s... based on score_new_old=%d" % (report_string,score_new_old)

