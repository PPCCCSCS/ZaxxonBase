# ZaxxonBase
Blatantly Stolen from Wireframe Magazine then Altered
https://www.raspberrypi.org/blog/code-a-zaxxon-style-axonometric-level-wireframe-33/

... the Wireframe code saves levels as [[column],[column],...] in the json files, which makes extended levels infeasible.
I prefer [[row],[row],...] format, so I've changed the json file, and rotated the input with mapBlocks = list(map(list, zip(*mapData['blocks']))).

I'm keeping this around for the isometric blitting, until I write something better.

Collision detection is broken after the level input rotation, which is weird, but I'll track that down again some point. It's probably a mismatch between getShipXY() and bx,by in drawMap().

Bitmaps need to be in a subdirectory named 'images', without the quotes, obviously.

I'm looking into polygons in pygame zero before I get back to collision detection.
