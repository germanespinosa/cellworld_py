import sys
from cellworld_py import *


implementation_name = sys.argv[1]
size = float(sys.argv[2])
center_x = float(sys.argv[3])
center_y = float(sys.argv[4])

new_implementation = World_implementation.get_from_name("hexagonal", "canonical")

new_implementation.space.transformation.size *= size
new_implementation.space.center.x *= center_x
new_implementation.space.center.y *= center_y
new_implementation.cell_transformation.size *= size

for cell_location in new_implementation.cell_locations:
    cell_location.x = (cell_location.x-.5) * size + center_x
    cell_location.y = (cell_location.y-.5) * size + center_y

with open("hexagonal."+implementation_name,"w") as f:
    f.write(str(new_implementation))
