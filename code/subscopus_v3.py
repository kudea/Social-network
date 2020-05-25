import matplotlib.pyplot as plt
import networkx as nx
import math
from matplotlib import artist
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
Adj = []
Author_id = []
Author_name = []
Author_field = []
Author_cite_sum = []
Author_paper_sum = []
field = []
colormap = []
pos = {}
onclick_node = ''
Field= {"Computer Science":0,"Genetics and Molecular Biology":1,"Veterinary":2,"Decision Sciences":3,
        "Physics and Astronomy":4,"Biochemistry":5,"Economics":6,"Arts and Humanities":7,
        "Immunology and Microbiology":8,"Environmental Science":9,"Energy":10,"Social Sciences":11,
        "Dentistry":12,"Agricultural and Biological Sciences":13,"Business":14,"Chemistry":15,
        "0":16,"Chemical Engineering":17,"Mathematics":18,"Neuroscience":19,"Health Professions":20,
        "Medicine":21,"Nursing":22,"Multidisciplinary":23,"Materials Science":24,
        "Management and Accounting":25,"Pharmacology":26,"Econometrics and Finance":27,"Psychology":28,
        "Engineering":29,"Earth and Planetary Sciences":30,"Toxicology and Pharmaceutics":31}
for i in range(len(Field)):
    field.append([])
G = nx.Graph()
g = nx.Graph()

def setAdj():
    global Adj, Author_id, Author_name, Author_field, Author_cite_sum, Author_paper_sum
    # all author in ncu
    ncu_author = open('idnamefieldcite.txt', 'r', encoding='utf-8')
    # all author for each paper
    author = open('author.txt', 'r', encoding='utf-8')

    a = ncu_author.readlines()
    b = author.readlines()
    ncu_author.close()
    author.close()

    for i in range(len(a)):
        a[i] = a[i].strip()
        tmp = a[i].split('\t')
        '''
        每次撈新資料需注意是否每row皆為5個columns : author_id, author_name, field, cite_sum, paper_sum
        '''
        Author_id.append(tmp[0])
        Author_name.append(tmp[1])
        Author_field.append(tmp[2])
        Author_cite_sum.append(int(tmp[3]))
        Author_paper_sum.append(int(tmp[4]))

    for i in range(len(b)):
        b[i] = b[i].strip()

    
    # declare a adjacent matric
    for i in range(len(Author_id)):
        Adj.append(len(Author_id)*[0])
    for i in range(len(b)):
        tmp = b[i].split('; ')
        tmp = list(set(tmp).intersection(set(Author_id)))
        for j in range(len(tmp)-1):
            for k in range(j+1, len(tmp)):
                x = Author_id.index(tmp[j])
                y = Author_id.index(tmp[k])
                if x > y:
                    t = y
                    y = x
                    x = t
                Adj[x][y] += 1


def setG():
    for i in range(len(Author_id)):
        for j in range(len(Author_id)):
            if Adj[i][j] > 5:
                G.add_edge(Author_id[i], Author_id[j], weight=Adj[i][j])
                G.node[Author_id[i]]["a_name"] = Author_name[i]
                G.node[Author_id[i]]["field"] = Author_field[i]
                G.node[Author_id[i]]["cite_sum"] = Author_cite_sum[i]
                G.node[Author_id[i]]["paper_sum"] = Author_paper_sum[i]
                try:
                    G.node[Author_id[i]]["avg_cite"] = Author_cite_sum[i] / Author_paper_sum[i]
                except Exception:
                    G.node[Author_id[i]]["avg_cite"] = 0

                G.node[Author_id[j]]["a_name"] = Author_name[j]
                G.node[Author_id[j]]["field"] = Author_field[j]
                G.node[Author_id[j]]["cite_sum"] = Author_cite_sum[j]
                G.node[Author_id[j]]["paper_sum"] = Author_paper_sum[j]
                try:
                    G.node[Author_id[j]]["avg_cite"] = Author_cite_sum[j] / Author_paper_sum[j]
                except Exception:
                    G.node[Author_id[i]]["avg_cite"] = 0

def getGraph(idx):
    node_list = []
    node_list = field[idx]
    return G.subgraph(node_list)


def classification():
    global field
    for n in G.nodes:
        fieldList = G.node[n]["field"].split(',')
        for i in fieldList:
            i = i.strip()
            i = i.lstrip()
            idx = Field[i]
            field[idx].append(n)
def init():
    setAdj()
    setG()
    classification()

# connected component
def getCC(G, n):
    cc = []
    ccs = nx.connected_component_subgraphs(G)
    for i in ccs:
        cc.append(i)
    return cc[n]
def getLargestCC(G):
    cc_len = nx.number_connected_components(G)
    largestCC = max(nx.connected_component_subgraphs(G), key = len)
    return largestCC

def plotGraph():
    global pos, g, colormap
    
    start_time = time.time()
    num = Field[field_menu.get()]
    g = nx.Graph()
    g = getGraph(num)
    end_time = time.time()
    print("--- %2f seconds ---" % (end_time - start_time))

    # tmp_G = getCC(G, 3)

    colormap = ['red'] * len(g.nodes)
    pos = nx.nx_pydot.graphviz_layout(g)
    sub.cla()
    nx.draw_networkx(g, pos=pos, with_labels=False, node_size=40, edgecolors='black', edge_color='b', node_color=colormap)
    canvas.draw()
    
    canvas.mpl_connect('button_press_event', onclick)

def onclick(event):
    global colormap, pos, g, onclick_node
    min_dist = 10000
    x = event.xdata
    y = event.ydata
    for i in g.nodes:
        node = pos[i]
        print(node)
        dist = math.pow(x-node[0], 2) + math.pow(y-node[1], 2)
        if min_dist > dist:
            min_dist = dist
        if dist < 80:
            # print(dist)
            print(g.node[i]["a_name"] + " " + g.node[i]["field"] + " " + str(g.node[i]["avg_cite"]))
            colormap = ['red'] * len(g.nodes)
            colormap[list(g.nodes()).index(i)] = 'yellow'
            author_info = tk.Label(root, text = "Name : " + g.node[i]["a_name"] + '\n' 
            + "Field : " + g.node[i]["field"] + '\n'
            + "Average_Cite : " + str(g.node[i]["avg_cite"])
            )
            onclick_node = i
            # author_info.place(x = 400, y = 120)
    sub.cla()
    nx.draw_networkx(g, pos=pos, with_labels=False, node_size=40, edgecolors='black', edge_color='b', node_color=colormap)
    canvas.draw()
    
    
    
def drawFields():
    # do something : 
    global onclick_node
    tmp_num = 0
    tmp = G.node[onclick_node]["field"]
    tmp = tmp.split(',')
    for i in tmp:
        i = i.lstrip()
        i = i.strip()
        num = Field[i]
        g = nx.Graph()
        g = getGraph(num)
        #用 i 去 dict找index
        #利用index找出g (call getGraph)
        for ii in g.nodes:
            colormap = ['red'] * len(g.nodes)
            colormap[list(g.nodes()).index(ii)] = 'yellow'

        plt.figure(figsize=(6,6), num=tmp_num)
        tmp_num += 1
        # plt.legend(loc='upper right', shadow=True)
        plt.grid(True)
        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos=pos, with_labels=False, node_size=40, edgecolors='black', edge_color='b', node_color=colormap)
        plt.draw()
        
def getDegCen():
    global g
    d = nx.degree_centrality(g)
    val = list(d.values())
    f2 = plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(g, pos=pos, cmap = plt.get_cmap('YlGn'), node_size=40, edgecolors='black', edge_color='b', node_color=val, vmin=0, vmax=1)
    nx.draw_networkx_edges(g, pos=pos)
    f2.show()

def getEgnCen():
    global g
    d = nx.eigenvector_centrality(g)
    val = list(d.values())
    f2 = plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(g, pos=pos, cmap = plt.get_cmap('YlGn'), node_size=40, edgecolors='black', edge_color='b', node_color=val, vmin=0, vmax=1)
    nx.draw_networkx_edges(g, pos=pos)
    f2.show()

def getCloseCen():
    global g
    d = nx.closeness_centrality(g)
    val = list(d.values())
    f2 = plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(g, pos=pos, cmap = plt.get_cmap('YlGn'), node_size=40, edgecolors='black', edge_color='b', node_color=val, vmin=0, vmax=1)
    nx.draw_networkx_edges(g, pos=pos)
    f2.show()

def getBtwnCen():
    global g
    d = nx.betweenness_centrality(g)
    val = list(d.values())
    f2 = plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(g, pos=pos, cmap = plt.get_cmap('YlGn'), node_size=40, edgecolors='black', edge_color='b', node_color=val, vmin=0, vmax=1)
    nx.draw_networkx_edges(g, pos=pos)
    f2.show()
    
root = tk.Tk()
root.geometry("800x600")
# root.aspect(1,1,1,1)    # fixed aspect ratio
f = plt.figure(figsize=(6,6))
sub = f.add_subplot(111)
canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().place(x = -50, y = 40)
init()
field_menu = ttk.Combobox(root, width=25, values = list(Field.keys()), state='readonly', justify='left')
field_menu.place(x = 80, y = 5)
run = tk.Button(root, text='run', width=5, height=3, command=plotGraph)
run.place(x = 350, y = 5)
show = tk.Button(root, text='show', width=5, height=3, command=drawFields)
show.place(x = 420, y = 5)
degree = tk.Button(root, text='degree', width=5, height=3, command=getDegCen)
degree.place(x = 490, y = 5)
eigen = tk.Button(root, text='Eigen', width=5, height=3, command=getEgnCen)
eigen.place(x = 560, y = 5)
between = tk.Button(root, text='between', width=5, height=3, command=getBtwnCen)
between.place(x = 630, y = 5)
close = tk.Button(root, text='close', width=5, height=3, command=getCloseCen)
close.place(x = 690, y = 5)
tk.mainloop()

'''
pos = nx.nx_pydot.graphviz_layout(G)
fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', onclick)
plt.figure(figsize=(8, 8), dpi=100)
plt.axis('off')
nx.draw_networkx(G, pos=pos, with_labels=False, node_size=25, edgecolors='black', edge_color='b')
plt.show()
'''

''' 
future work : 
1. rescale the graph 
2. change edge color to let it can represent weight (weather radar graph)
3. pick the highest weight hop to do analysis
4. connected component
'''

