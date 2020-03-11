# ZaxxonBase
# Blatantly Stolen from Wireframe Magazine then Altered
# https://www.raspberrypi.org/blog/code-a-zaxxon-style-axonometric-level-wireframe-33/

# ... the Wireframe code saves levels as [[column],[column],...] in the json files, which makes extended levels infeasible.
# I prefer [[row],[row],...] format, so I've changed the json file, and rotated the input with mapBlocks = list(map(list, zip(*mapData['blocks']))).

# I'm keeping this around for the isometric blitting, until I write something better.
