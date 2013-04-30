#!/usr/bin/env python

# This file fixes the bug in line 273 of funcparserlibs parser.py
# Run as admin!

import os
import shutil
import funcparserlib


OLD_STMT = 'return (res, e.state)'
NEW_STMT = 'return res, State(s.pos, e.state.max)'

funcparserlib_dir = os.path.dirname(funcparserlib.__file__)
parser_file = os.path.join(funcparserlib_dir, 'parser.py')
new_parser_file = os.path.join(funcparserlib_dir, 'parser_new.py')
backup_file = os.path.join(funcparserlib_dir, 'parser_backup.py')

print 'Found original at:\n\t%s' % parser_file

if not os.path.exists(backup_file):
    print 'Making backup at:\n\t%s' % backup_file
    shutil.copy(parser_file, backup_file)

if os.path.exists(backup_file):
    print 'Found backup at:\n\t%s' % backup_file

with file(parser_file, 'r') as fobj:
    old = fobj.read()

if 'return (res, e.state)' in old:
    print "Bug found."
else:
    print "Could not find the bug."

with file(new_parser_file, 'w') as fobj:
    fobj.write(old.replace(OLD_STMT, NEW_STMT))

os.remove(parser_file)
shutil.move(new_parser_file, parser_file)

with file(parser_file, 'r') as fobj:
    new = fobj.read()

if NEW_STMT in new and not OLD_STMT in new and os.path.exists(parser_file):
    print "SUCCESS."
else:
    print "ERROR"
