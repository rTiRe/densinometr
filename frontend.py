import matplotlib.pyplot as plt
import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from backend import Densitometr

COLORS_PAINTS_NAMES = {'blue': 'blue', 'green': 'green', 'lightblue': 'lightblue', 'red': 'red', 'purple': 'purple', 'yellow': 'yellow', 'white': 'lightgray'}
ITERATIONS_STEP = 10


class Graph(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.densitometr = Densitometr('COM4')

        self.figure, self.ax = plt.subplots()
        self.lines = {color: self.ax.plot([], [], label=color, color=paint)[0] for color, paint in COLORS_PAINTS_NAMES.items()}

        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel('Iteration')
        self.ax.set_ylabel('Optical Density')
        self.ax.legend()
        plt.ion()

        self.iteration = 0
        self.box = self.ids.box
        self.box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def start_plot(self):
        for _ in range(ITERATIONS_STEP):
            iter_data = self.densitometr.get_statistic()
            colors_density = iter_data.current_colors_optical_density
            print(colors_density)
            self._update_graph(colors_density)
        self._adjust_plot()

    def clear_plot(self):
        self.iteration = 0
        for color, _ in self.lines.items():
            self.lines[color].set_xdata([])
            self.lines[color].set_ydata([])
        self._adjust_plot()

    def _adjust_plot(self):
        self.ax.set_xlim(0, max(30, self.iteration))
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def _update_graph(self, colors_density):
        for color, line in self.lines.items():
            x = line.get_xdata()
            self.lines[color].set_xdata(np.append(x, self.iteration))
            self.lines[color].set_ydata(np.append(line.get_ydata(), colors_density[color]))
        self.iteration += 1


class GraphApp(App):
    def build(self):
        Builder.load_file('graph.kv')
        return Graph()


if __name__ == '__main__':
    GraphApp().run()
