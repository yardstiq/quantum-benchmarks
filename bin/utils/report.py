import os
import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from .project import Project, Plot

class BenchmarkReport:

    def __init__(self, projects, layout : dict, colors = None, titles = None):
        super().__init__()
        if isinstance(projects, str):
            self.projects = self.scan_projects(projects)
        elif isinstance(projects, list):
            self.projects = projects
        else:
            raise TypeError('invalid argument type for <projects>')

        self.layout = layout
        self.titles = list(layout)

        self.labels = []
        for ls in layout.values():
            for l in ls:
                self.labels.append(l)

        self.update_table(self.labels)
        self.colors = colors

    def scan_projects(self, path):
        projects = []
        for (root, dirs, files) in os.walk(path):
            if 'benchmarks.sh' in files:
                projects.append(Project(root))

        return projects

    def create_figure(self, axes):
        if isinstance(axes, np.ndarray):
            axes_list = []
            for rows in axes:
                if isinstance(rows, np.ndarray):
                    for ax in rows:
                        axes_list.append(ax)
                else:
                    axes_list.append(rows)
        else:
            axes_list = [axes]

        plots = []
        for (ax, title) in zip(axes_list, self.layout):
            ax.set_xlabel("nqubits", size=16)
            ax.set_ylabel("ns", size=16)
            plots.append(Plot(ax, title, self.layout[title]))

        return plots

    def update_table(self, labels : List[str]):
        for pj in self.projects:
            pj.update_table(labels)

    def plot_absolute(self, axes):
        plots = self.create_figure(axes)

        for each in plots:
            each.ax.set_title(each.title)

        for pj in self.projects:
            pj.absolute(plots, self.colors[pj])

        return plots

    def plot_relative(self, project : Project, axes):
        plots = self.create_figure(axes)
        project.update_table(self.labels)

        for each in plots:
            each.ax.set_title(each.title + '(relative to ' + project.name + ')')

        if project in self.projects:
            projects = self.projects
        else:
            projects = [project, *self.projects]

        for pj in projects:
            pj.relative(project, plots, self.colors[pj])

        return plots

    def project_names(self):
        return [pj.name for pj in self.projects]
