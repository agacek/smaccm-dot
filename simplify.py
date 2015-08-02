#!/usr/bin/env python

import re
from collections import defaultdict

names = {}
arrows = defaultdict(lambda: 0)
curr = None

f = open("smaccmpilot.dot")
for line in f.readlines():
    m = re.search("(thread_\w+)", line)
    if m:
        names[m.group(1)] = m.group(1)
    
    m = re.search('subgraph *cluster_(\w+)', line)
    if m:
        curr = m.group(1)

    if curr:
        m = re.search('^ *(\w+);$', line)
        if m:
            names[m.group(1)] = curr

    if "}" in line:
        curr = None

    m = re.search('(\w+) -> (\w+)', line)
    if m:
        src = names[m.group(1)]
        dst = names[m.group(2)]
        arrows[(src, dst)] += 1

print '''
digraph main {
  node [shape=box];
  {
    { rank=min; GCS [style=filled]; uart; }
    { rank=max; Pixhawk [style=filled]; can_node; }
  }
  GCS -> uart -> GCS;
  Pixhawk -> can_node -> Pixhawk;
'''
for (src, dst) in arrows:
    print "  %s -> %s;" % (src, dst)
print "}"
