#!/usr/bin/env python

import re

print "digraph camkes {"

f = open("sys_impl_assembly.camkes")
for line in f.readlines():
    m = re.search('\(from (\w+).* to (\w+)', line)
    if m:
        src = m.group(1)
        dst = m.group(2)
        print " ", src, "->", dst, ";"

print "}"
