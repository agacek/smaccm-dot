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

back = ["send_transdata",
        "frame_datalink_encode",
        "commsecEncodeState",
        "controllableVehicleProducerInput",
        "fragment_reassembly",
        "controllableVehicleProducerOutput"]

print '''
digraph main {
  newrank=true;
  node [shape=box];
  { rank=source; GCS [style=filled]; }
  { rank=sink; Pixhawk [style=filled]; }
  subgraph {
    subgraph cluster_init {
      color = blue;
      label = "Init";
      style = rounded;
      thread_init;
      commsecEncodeStaticKey;
      commsecDecodeStaticKey;
    }
    subgraph cluster_gcs_in {
      color = blue;
      label = "GCS in";
      style = rounded;
      thread_period_5ms;
      frame_datalink_decode;
      frameBuffer;
      commsecDecodeState;
      controllableVehicleConsumerOutput;
      commsecDecodeStaticKey;
    }
    subgraph cluster_pixhawk_out {
      color = blue;
      label = "Pixhawk out";
      style = rounded;
      controllableVehicleConsumerInput;
      fragment_drop;
      fragment_0x200;
    }
    subgraph cluster_pixhawk_in {
      color = blue;
      label = "Pixhawk in";
      style = rounded;
      fragment_reassembly;
      controllableVehicleProducerOutput;
    }  
    subgraph cluster_gcs_out {
      color = blue;
      label = "GCS out";
      style = rounded;
      controllableVehicleProducerInput;
      commsecEncodeState;
      frame_datalink_encode;
      send_transdata;
      commsecEncodeStaticKey;
    }  
    subgraph cluster_camera {
      color = blue;
      label = "Camera";
      style = rounded;
      periodic_camera_injector;
      camera_vm;
      thread_period_1000ms;
    }
  }
  { rank=same; send_transdata; frame_datalink_decode; }
  { rank=same; fragment_0x200; fragment_reassembly; }
  { rank=same; controllableVehicleProducerOutput; controllableVehicleConsumerInput; }
  { rank=same; thread_period_1000ms; commsecDecodeState; commsecEncodeState; }
  GCS -> uart;
  GCS -> uart [dir=back];
  can_node -> Pixhawk;
  can_node -> Pixhawk [dir=back];
  uart -> frameBuffer [style=invis];
'''
for (src, dst) in arrows:
    if src in back:
        print "  %s -> %s [dir=back];" % (dst, src)
    else:
        print "  %s -> %s;" % (src, dst)
print "}"
