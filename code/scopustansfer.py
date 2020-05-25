import matplotlib.pyplot as plt
import networkx as nx
# all author in ncu
ncu_author = open('ncu_author.txt', 'r')
# all author for each paper
author = open('author.txt', 'r')
name = open('idname.txt', 'r',encoding = 'utf-16')
field = open('idfield.txt', 'r',encoding = 'utf8')


a = ncu_author.readlines()
b = author.readlines()
c = name.readlines()
d = field.readlines()

ncu_author.close()
author.close()
name.close()
field.close()

for i in range(len(a)):
    a[i] = a[i].strip()
for i in range(len(b)):
    b[i] = b[i].strip()
for i in range(len(c)):
    c[i] = c[i].strip()
for i in range(len(d)):
    d[i] = d[i].strip()

mat = []
# declare a adjacent matric
for i in range(len(a)):
    mat.append(len(a)*[0])


for i in range(len(b)):
    tmp = b[i].split('; ')
    tmp = list(set(tmp).intersection(set(a)))
    for j in range(len(tmp)-1):
        for k in range(j+1, len(tmp)):
            x = a.index(tmp[j])
            y = a.index(tmp[k])
            if x > y:
                t = y
                y = x
                x = t
            mat[x][y] += 1
			
		
G = nx.Graph()
for i in range(len(a)):
    for j in range(len(a)):
        if mat[i][j] > 5:
            G.add_edge(a[i], a[j], weight=mat[i][j])

for i in G.nodes.keys():
    for j in c[i]:
        print(c[i])
        if i == j:
            idx = c[i].index(j)
            G.nodes[i]["name"] = a[i][idx]
			
nx.write_gexf(G,"/Users/samue/OneDrive/桌面/journal/test.gexf")
'''
pos = nx.spring_layout(G,weight='weight')


plt.figure(figsize=(25, 25))
plt.axis('off')
nx.draw_networkx(G, pos=pos, with_labels=False, node_size=30, edgecolors='black', edge_color='b')
plt.savefig('C:/Users/samue/OneDrive/桌面/journal/test.png')

plt.show()
'''