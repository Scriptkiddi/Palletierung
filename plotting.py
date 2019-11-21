import matplotlib.pyplot as plt
import numpy as np
import pyglet

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width // 2, y=window.height // 2,
                          anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
    label.draw()

# prepare some coordinates
def plot(width, depth, height, boxes):
    pyglet.app.run()
    #x, y, z = np.indices((width, depth, height))

    ## draw cuboids in the top left and bottom right corners, and a link between them
    #cubes = []
    #voxels = (x > width) & (y > depth) & (z > height)
    #for box in boxes:
    #    box_x, box_y, box_z = box.urc()
    #    cube = (box.x / 10 <= x) & (box.y / 10 <= y) & (box.z / 10 <= z) & (x <= box_x / 10) & (y <= box_y / 10) & (
    #            z <= box_z / 10)
    #    cubes.append(cube)
    #    voxels |= cube

    ## link = abs(x - y) + abs(y - z) + abs(z - x) <= 2

    ## combine the objects into a single boolean array
    #cube1 = (1 <= x) & (x < 3) & (y < 3) & (z < 3)
    #cube2 = (x >= 5) & (y >= 5) & (z >= 5)
    ##voxels = cube1 | cube2

    ## set the colors of each object
    #colors = np.empty(voxels.shape, dtype=object)
    ##colors[cube1] = 'blue'
    ##colors[cube2] = 'green'
    #avaliable_colors = ['red', 'green', 'blue', 'pink', 'yellow']
    #color_counter = 0
    #for cube in cubes:
    #    color_counter += 1
    #    colors[cube] = avaliable_colors[color_counter % len(avaliable_colors)]

    ## and plot everything
    #fig = plt.figure()
    #ax = fig.gca(projection='3d')
    #ax.voxels(voxels, facecolors=colors, edgecolor='k')

    #plt.show()
