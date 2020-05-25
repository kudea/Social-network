import matplotlib.pyplot as plt
import networkx as nx
import math
from matplotlib import artist
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
colormap = ['blue'] * 5
root = tk.Tk()
G=nx.complete_graph(5)
pos = nx.spring_layout(G)
def onclick(event):
    global colormap
    min_dist = 10000
    x = event.xdata
    y = event.ydata
    print("click on : ", x, y)
    for i in G.nodes:
        node = pos[i]
        dist = math.pow(x-node[0], 2) + math.pow(y-node[1], 2)
        if min_dist > dist:
            min_dist = dist
        if dist < 0.005:
            print(dist)
            colormap = ['blue'] * len(G.nodes)
            colormap[list(G.nodes()).index(i)] = 'yellow'
            tmp = i
    a.cla()
    nx.draw_networkx(G, pos=pos , ax=a, node_color = colormap)
    
    canvas.draw()

f = plt.figure(figsize=(5,4))
a = f.add_subplot(111)
nx.draw_networkx(G, pos=pos , ax=a, node_color = colormap)
xlim=a.get_xlim()
ylim=a.get_ylim()



# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


canvas.mpl_connect('button_press_event', onclick)
root.mainloop()