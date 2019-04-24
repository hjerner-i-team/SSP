from visdom import Visdom
import numpy as np

'''
Plotting module. Create an instance of this as a global variable for easy plotting throughout the project pipeline. 
Requires a running visdom server. Start server using:
python3 -m visdom.server
'''
class VisdomLinePlotter:
    def __init__(self, env_name='main'):
        self.viz = Visdom()
        self.env = env_name
        self.plots = []
        
#Plots a line plot. Creates new plot if not existing, else redraws plot
    def plot(self, x, y, win, title):
        if win not in self.plots:
            self.plots.append(win)
            self.viz.line(X=x, Y=y, win=win, opts=dict(
                title=title,
                xlabel='t',
                ylabel='y'))

        else: 
            self.viz.line(X=x,Y=y, win=win, update='replace')
        
# heatmap
    def plot_map(self, x, win, title):
        if win not in self.plots:
            self.plots.append(win)
            viz.heatmap(
                X=x,
                win=win,
                opts=dict(colormap='Electric',)   
            )

        else:
            viz.heatmap(
                X=x,
                win=win,
                update='replace'
            )

global plotter
