import numpy
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import matplotlib.colors
from .world import *
from .experiment import *

class Display:
    def __init__(self, world, fig_size=(12, 10), padding=.1, show_axes=False, cell_color="white", occlusion_color="black", background_color="white", habitat_color="white", cell_edge_color="black", habitat_edge_color="black"):
        if not isinstance(world, World):
            raise "incorrect type for world"
        self.world = world
        self.fig = plt.figure(figsize=fig_size)
        self.ax = self.fig.add_subplot(111)
        self.ax.axes.xaxis.set_visible(show_axes)
        self.ax.axes.yaxis.set_visible(show_axes)

        xcenter = world.implementation.space.center.x
        ycenter = world.implementation.space.center.y

        hsize = world.implementation.space.transformation.size / 2
        pad = hsize * padding

        xmin = xcenter - hsize - pad
        xmax = xcenter + hsize + pad

        ymin = ycenter - hsize - pad
        ymax = ycenter + hsize + pad

        self.ax.set_xlim(xmin=xmin, xmax=xmax)
        self.ax.set_ylim(ymin=ymin, ymax=ymax)
        self.ax.set_facecolor(background_color)
        ssides = world.implementation.space.shape.sides
        srotation = math.radians(0-world.implementation.space.transformation.rotation)

        csides = world.configuration.cell_shape.sides
        crotation = math.radians(0 - world.implementation.cell_transformation.rotation - srotation)


        csize = world.implementation.cell_transformation.size / 2
        ssize = hsize

        for cell in self.world.cells:
            color = occlusion_color if cell.occluded else cell_color
            self.ax.add_patch(RegularPolygon((cell.location.x, cell.location.y), csides, csize, facecolor=color, edgecolor=cell_edge_color, orientation=crotation, zorder=-2, linewidth=1))
        self.ax.add_patch(RegularPolygon((xcenter, ycenter), ssides, ssize, facecolor=habitat_color, edgecolor=habitat_edge_color, orientation=srotation, zorder=-3))
        plt.tight_layout()

    def add_trajectories(self, trajectories, colors={}):
        check_type(trajectories, Trajectories, "wrong type for trajectories")
        agents = trajectories.get_agent_names()
        for index, agent in enumerate(agents):
            locations = trajectories.get_agent_trajectory(agent).get("location")
            x = locations.get("x")
            y = locations.get("y")
            color = list(matplotlib.colors.cnames.keys())[index]
            if agent in colors:
                color = colors[agent]
            for i in range(len(x)-1):
                lcolor = None
                if type(color) is numpy.ndarray:
                    lcolor = color[i]
                else:
                    lcolor = color
                self.ax.plot([x[i], x[i+1]], [y[i], y[i+1]], color=lcolor, alpha=.5, linewidth=3)

    def circle(self, location, radius, color):
        circle_patch = plt.Circle((location.x, location.y), radius, color=color)
        self.ax.add_patch(circle_patch)

    def arrow(self, beginning, theta, dist, color, head_width=.02):
        check_type(beginning, Location, "incorrect type for beginning")
        ending = beginning.copy().move(theta=theta, dist=dist)
        length = ending - beginning
        self.ax.arrow(beginning.x, beginning.y, length.x, length.y, color=color, head_width=head_width, length_includes_head=True)