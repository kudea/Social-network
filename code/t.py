import matplotlib.pyplot as plt
import networkx as nx

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
''
f = []

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



G2 = G.copy()

for n in G.nodes:
    field = G.node[n]["field"].split(',')
    for i in field:
        i = i.strip()
        i = i.lstrip()
        idx = Field[i]
        f[idx].append(n)


for n in G2.nodes:
    N = G2.node[n]
    F = list(set(f[0]).difference(set(N)))

for NN in F:
    G2.remove_node(NN)
        
        


pos = nx.spring_layout(G2)
plt.axis('on')
nx.draw_networkx(G2, pos=pos, with_labels=False, node_size=40, edgecolors='black', edge_color='b')
plt.show()
