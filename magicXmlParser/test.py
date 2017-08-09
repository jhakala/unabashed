from emap_parser import *

crate = "22"
slot = "11"
for line in search_emap([("crate", crate),("slot", slot)]):
  print line
