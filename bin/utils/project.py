import os
import json
import random
import numpy as np
from typing import List, Dict

class Project(object):
    '''Benchmark Project Object.

    Due to different implementation of the benchmarking framework, we need to specialize
    methods for different languages to process the data.
    '''

    def __init__(self, path: str, name : str):
        super(Project, self).__init__()
        self.path = path
        self.name = name
        self.table : Dict = {}
        self._data = None

    @staticmethod
    def random_color():
        '''random color in RGB format.
        '''
        return (random.random(), random.random(), random.random())

    def data_file(self):
        data_file_list = []
        # find any file end with data.json and put it into this list
        for (root, dirs, files) in os.walk(os.path.join(self.path, 'data')):
            for file in files:
                if file.endswith('data.json'):
                    data_file_list.append(os.path.join(root, file))
        return data_file_list

    def read_data(self):
        last = self.data_file()[-1]
        with open(last) as f:
            data = json.load(f)

        return data

    @property
    def data(self):
        if self._data is None:
            self._data = self.read_data()

        return self._data

    def get_label(self, data, label : str):
        raise NotImplementedError

    def get_min_time(self, entry):
        raise NotImplementedError

    def get_nqubits(self, entry):
        raise NotImplementedError

    def labels(self, data):
        raise NotImplementedError

    def update_table(self, labels : List[str]):
        for label in labels:
            label_data = self.get_label(self.data, label)
            if label_data:
                min_times = [self.get_min_time(each) for each in label_data]
                nqubits = [self.get_nqubits(each) for each in label_data]
                indices = sorted(range(len(nqubits)), key=lambda k : nqubits[k])
                min_times = [min_times[k] for k in indices]
                nqubits = [nqubits[k] for k in indices]
                self.table[label] = {"nqubits": nqubits, "times": min_times}


    def absolute(self, plots : List, colors = None):
        for each in plots:
            for label in each.labels:
                if label in self.table:
                    d = self.table[label]
                    if colors is None:
                        color = self.random_color()
                    else:
                        color = colors[label]

                    line = each.ax.semilogy(d["nqubits"], d["times"], '-o', markersize=4, color=color)
                    each.add_line(self, line)


    def relative(self, project, plots : List, colors = None):
        for each in plots:
            for label in each.labels:
                d = self.table[label]
                if colors is None:
                    color = self.random_color()
                else:
                    color = colors[label]


                line = each.ax.semilogy(d["nqubits"],
                    np.array(d['times'])/np.array(project.table[label]['times']), '-o', markersize=4, color=color)
                each.add_line(self, line)


class PythonProject(Project):

    def __init__(self, path : str, name : str = None):
        if name is None:
            name = os.path.basename(path)

        super(PythonProject, self).__init__(path, name)


    def labels(self, data = None):
        if data is None:
            data = self.read_data()
        return set([each['group'] for each in data['benchmarks']])

    def get_label(self, data, label : str):
        return [each for each in data['benchmarks'] if each['group'] == label]

    def get_min_time(self, entry):
        return entry['stats']['min'] * 1e9 # convert to ns

    def get_nqubits(self, entry):
        return entry['params']['nqubits']

class JuliaProject(Project):

    def __init__(self, path : str, name : str = None):
        if name is None:
            name = path.capitalize()
        super(JuliaProject, self).__init__(path, name)

    def get_label(self, data, label : str):
        return data[label]

    def get_min_time(self, entry):
        return entry['times']

    def get_nqubits(self, entry):
        return entry['nqubits']

    def update_table(self, labels):
        for l in labels:
            self.table[l] = self.data[l]



class Plot:

    def __init__(self, ax, title, labels = None, lines = None):
        self.ax = ax
        self.title = title

        if labels is None:
            self.labels = []
        else:
            self.labels = labels

        if lines is None:
            self._lines = {}
        else:
            self._lines = lines

    def add_line(self, project : Project, line):
        if project in self._lines:
            self._lines[project].append(line)
        else:
            self._lines[project] = [line]

    def getlines(self, project : Project = None):
        if project is None:
            lines = []
            for ls in self._lines.values():
                lines.append(ls)

            return lines

        else:
            return self._lines[project]

    @property
    def lines(self):
        return self.getlines()
