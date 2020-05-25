#Field=['Computer Science', 'Genetics and Molecular Biology', 'Veterinary', 'Decision Sciences', 'Physics and Astronomy', 'Biochemistry', 'Economics', 'Arts and Humanities', 
#'Immunology and Microbiology', 'Environmental Science', 'Energy', 'Social Sciences', 'Dentistry', 'Agricultural and Biological Sciences', 'Business', 'Chemistry', 
#'0', 'Chemical Engineering', 'Mathematics', 'Neuroscience', 'Health Professions', 'Medicine', 'Nursing', 'Multidisciplinary', 
#'Materials Science', 'Management and Accounting', 'Pharmacology', 'Econometrics and Finance', 'Psychology', 'Engineering', 'Earth and Planetary Sciences', 'Toxicology and Pharmaceutics']
#df = pd.DataFrame(index=list(range(1,10000)),columns=Field)

import matplotlib.pyplot as plt
import networkx as nx
import math

# all author in ncu
ncu_author = open('idnamefieldcite.txt', 'r', encoding='utf-8')
# all author for each paper
author = open('author.txt', 'r', encoding='utf-8')

a = ncu_author.readlines()
b = author.readlines()
ncu_author.close()
author.close()

author_id = []
author_name = []
author_field = []
author_cite_sum = []
author_paper_sum = []
t = []


for i in range(len(a)):
    a[i] = a[i].strip()
    tmp = a[i].split('\t')
    '''
    每次撈新資料需注意是否每row皆為5個columns
    '''
    author_id.append(tmp[0])
    author_name.append(tmp[1])
    author_field.append(tmp[2])
    author_cite_sum.append(int(tmp[3]))
    author_paper_sum.append(int(tmp[4]))
    t = t+ author_field[i].split(',')  
    T = set(t)  
    number = len(T)
    
    
for i in range(len(b)):
    b[i] = b[i].strip()

mat = []
# declare a adjacent matric
for i in range(len(author_id)):
    mat.append(len(author_id)*[0])


for i in range(len(b)):
    tmp = b[i].split('; ')
    tmp = list(set(tmp).intersection(set(author_id)))
    for j in range(len(tmp)-1):
        for k in range(j+1, len(tmp)):
            x = author_id.index(tmp[j])
            y = author_id.index(tmp[k])
            if x > y:
                t = y
                y = x
                x = t
            mat[x][y] += 1
# f = open("adj.txt", 'w')
# for i in range(len(a)):
#     for j in range(len(a)):
#         f.write(str(mat[i][j]) + ' ')
#     f.write('\n')
# f.close()
f = []
#Field
Field= {"Computer Science":0,"Genetics and Molecular Biology":1,"Veterinary":2,"Decision Sciences":3,
        "Physics and Astronomy":4,"Biochemistry":5,"Economics":6,"Arts and Humanities":7,
        "Immunology and Microbiology":8,"Environmental Science":9,"Energy":10,"Social Sciences":11,
        "Dentistry":12,"Agricultural and Biological Sciences":13,"Business":14,"Chemistry":15,
        "0":16,"Chemical Engineering":17,"Mathematics":18,"Neuroscience":19,"Health Professions":20,
        "Medicine":21,"Nursing":22,"Multidisciplinary":23,"Materials Science":24,
        "Management and Accounting":25,"Pharmacology":26,"Econometrics and Finance":27,"Psychology":28,
        "Engineering":29,"Earth and Planetary Sciences":30,"Toxicology and Pharmaceutics":31}
for i in range(number):
    f.append([])
    
    
G = nx.Graph()
for i in range(len(author_id)):
    for j in range(len(author_id)):
        if mat[i][j] > 5:
            G.add_edge(author_id[i], author_id[j], weight=mat[i][j])
            G.node[author_id[i]]["a_name"] = author_name[i]
            G.node[author_id[i]]["field"] = author_field[i]
            G.node[author_id[i]]["cite_sum"] = author_cite_sum[i]
            G.node[author_id[i]]["paper_sum"] = author_paper_sum[i]
            try:
                G.node[author_id[i]]["avg_cite"] = author_cite_sum[i] / author_paper_sum[i]
            except Exception:
                G.node[author_id[i]]["avg_cite"] = 0

            G.node[author_id[j]]["a_name"] = author_name[j]
            G.node[author_id[j]]["field"] = author_field[j]
            G.node[author_id[j]]["cite_sum"] = author_cite_sum[j]
            G.node[author_id[j]]["paper_sum"] = author_paper_sum[j]
            try:
                G.node[author_id[j]]["avg_cite"] = author_cite_sum[j] / author_paper_sum[j]
            except Exception:
                G.node[author_id[i]]["avg_cite"] = 0





for n in G.nodes:
    field = G.node[n]["field"].split(',')
    for i in field:
        idx = Field[i]
        f[idx].append(G.node[n]["a_name"])


m = []
# declare a adjacent matric
for i in range(len(author_id)):
    m.append(len(author_id)*[0])

which = input('要第幾個領域: ')
w = int(which)

tm = f[w]

for j in range(len(tm)-1):
    for k in range(j+1, len(tm)):
        x = author_name.index(tm[j])
        y = author_name.index(tm[k])
        if x > y:
            t = y
            y = x
            x = t
        m[x][y] += 1
            
g = nx.Graph()
for i in range(len(author_id)):
    for j in range(len(author_id)):
        if m[i][j] > 5:
            g.add_edge(author_id[i], author_id[j], weight=m[i][j])
            g.node[author_id[i]]["a_name"] = author_name[i]
            g.node[author_id[i]]["field"] = author_field[i]
            g.node[author_id[i]]["cite_sum"] = author_cite_sum[i]
            g.node[author_id[i]]["paper_sum"] = author_paper_sum[i]
            try:
                g.node[author_id[i]]["avg_cite"] = author_cite_sum[i] / author_paper_sum[i]
            except Exception:
                g.node[author_id[i]]["avg_cite"] = 0

            g.node[author_id[j]]["a_name"] = author_name[j]
            g.node[author_id[j]]["field"] = author_field[j]
            g.node[author_id[j]]["cite_sum"] = author_cite_sum[j]
            g.node[author_id[j]]["paper_sum"] = author_paper_sum[j]
            try:
                g.node[author_id[j]]["avg_cite"] = author_cite_sum[j] / author_paper_sum[j]
            except Exception:
                g.node[author_id[i]]["avg_cite"] = 0
                
pos = nx.spring_layout(g)
plt.axis('on')
nx.draw_networkx(g, pos=pos, with_labels=False, node_size=40, edgecolors='black', edge_color='b')
plt.show()
'''
cc = []
ccs = nx.connected_component_subgraphs(g)
for i in ccs:
    cc.append(i)
cc_len = nx.number_connected_components(g)
largest_cc = max(nx.connected_component_subgraphs(g), key = len)




def onclick(event):
    min_dist = 10000
    x = event.xdata
    y = event.ydata
    for i in tmp_G.nodes:
        node = pos[i]
        dist = math.pow(x-node[0], 2) + math.pow(y-node[1], 2)
        if min_dist > dist:
            min_dist = dist
        if dist < 80:
            print(tmp_G.node[i]["a_name"] + " " + tmp_G.node[i]["field"] + " " + str(tmp_G.node[i]["avg_cite"]))

pos = nx.spring_layout(tmp_G)

fig, ax = plt.subplots(figsize=(6,6))
fig.canvas.mpl_connect('button_press_event', onclick)

plt.axis('on')
nx.draw_networkx(tmp_G, pos=pos, with_labels=False, node_size=40, edgecolors='black', edge_color='b')
plt.show()
'''