import networkx as nx
import matplotlib.pyplot as plt

H = nx.read_edgelist("graph_H.txt")
G = nx.read_edgelist("graph_G.txt")


print(H)

nodes_H = list(H.nodes)
nodes_G = list(G.nodes)
n_g=len(nodes_G)
n_h=len(nodes_H)

edges_G =list(G.edges)
edges_H =list(H.edges)
print(edges_G)
print(edges_H)


L = {}
for n in G.nodes():
    L[n] = []
    for m in nodes_H:
        L[n].append(m)
print()
print("Before Pre-Processing")   
print(f"L:")
for i in L:
    print(f"{i}: {L[i]}")

########################################################################################
#Helper Function
########################################################################################
def print_dict(dic):
    for i in dic:
        print(f"{i}: {dic[i]}")
    
##########################################################################################
#Pre-Processing
##########################################################################################

#Node Check
if len(nodes_G) != len(nodes_H):
    print("Not the same number of nodes in the two graphs")

#Edge Check
if len(edges_G) != len(edges_H):
    print("Not the same number of edges in the two graphs")

#Degree Checking
for u in L:
    degree_u = len(list(G.neighbors(u)))
    for a in L[u][:]:
        degree_a = len(list(H.neighbors(a)))
        if degree_u != degree_a:
            L[u].remove(a)

sp_G= dict(nx.all_pairs_shortest_path(G))
sp_H = dict(nx.all_pairs_shortest_path(H))

#distance=nx.all_pairs_shortest_path(G)
### writing the all-pairs-shortest-path

G_SP={}  # size of the shortest path
G_NS={}  # number of shortest path 
for u in G.nodes():
    G_SP[u]={}
    G_NS[u]={}
    for v in G.nodes():
      G_SP[u][v]=n_g
      G_NS[u][v]=0

for u in G.nodes():
    G_SP[u][u]=0
    G_NS[u][u]=1
   
for u in G.nodes():
    for v in G.nodes():
      if( (u,v) in G.edges() ) :
           G_SP[u][v]=1
         #  G_SP[v][u]=1
           G_NS[u][v]=1
         #  G_NS[v][u]=1
           
           

max_dis=0;
for w in G.nodes():
    for u in G.nodes():
        for v in G.nodes():
            if (w==u or w==u or u==v):
                continue
            if (G_SP[u][w]+G_SP[w][v] < G_SP[u][v]) :
                G_SP[u][v]=G_SP[u][w]+G_SP[w][v]
       

max_dis_G=0;
for u in G.nodes():
    for v in G.nodes():
        if (G_SP[u][v] > max_dis_G):
            max_dis_G=G_SP[u][v]

for u in G.nodes():
    for d in range(1,max_dis_G+1):
        for v in G.nodes():
            if (G_SP[u][v]==d):
                for w in G.nodes():
                    if ((v,w) in G.edges()):
                        if (G_SP[u][w]==d+1):
                          G_NS[u][w]+=G_NS[u][v]



H_SP={}  # size of the shortest path
H_NS={}  # number of shortest path 
for a in H.nodes():
    H_SP[a]={}
    H_NS[a]={}
    for b in H.nodes():
      H_SP[a][b]=n_g
      H_NS[a][b]=0

for a in H.nodes():
    H_SP[a][a]=0
    H_NS[a][a]=1
   
for a in H.nodes():
    for b in H.nodes():
      if( (a,b) in H.edges() ) :
           H_SP[a][b]=1
         #  H_SP[v][u]=1
           H_NS[a][b]=1
         #  H_NS[v][u]=1

max_dis_H=0;
for a in H.nodes():
    for b in H.nodes():
        if (H_SP[a][b] > max_dis_H):
            max_dis_H=H_SP[a][b]


#print('max_dis ',max_dis)

#for u in G.nodes():

for c in H.nodes():
    for a in H.nodes():
        for b in H.nodes():
            if (c==a or c==b or a==b):
                continue
            if (H_SP[a][c]+H_SP[c][b] < H_SP[a][b]) :
                H_SP[a][b]=H_SP[a][c]+H_SP[c][b]

for a in H.nodes():
    for d in range(1,max_dis_H+1):
        for b in H.nodes():
            if (H_SP[a][b]==d):
                for c in H.nodes():
                    if ((b,c) in H.edges()):
                        if (H_SP[a][c]==d+1):
                          H_NS[a][c]+=H_NS[a][b]

#print(np.max(np.array(G_SP))) 


#print("Before Distance")
#print_dict(L)
#Distance
for u in sp_G:
    new_array = []
    for v in sp_G[u]:  
        lis = sp_G[u][v]
        new_array.append((len(lis)-1))
    new_array.sort()
    sp_G[u] = new_array

for a in sp_H:
    new_array = []
    for b in sp_H[a]:
        lis = sp_H[a][b]
        new_array.append((len(lis)-1))
    new_array.sort()
    sp_H[a] = new_array

#print("Distances")
#print_dict(sp_G)
#print_dict(sp_H)

for u in L:
    for a in L[u]:
        if sp_G[u] != sp_H[a]:
            L[u].remove(a)

print()
print("After Distance:")
print_dict(L)


print()
print("After Pre-Processing")   
print_dict(L)

L['11']= ['0']
#L['9']= ['4']
#L['10']=['1']
#L['12']=['13']


#Main
#########################################################################################
update = 1

while update:
    update = 0
    for u in L: 
        for v in list(G.neighbors(u)):
            for a in L[u]:
                flag = 0 
                for b in L[v]:
                    if (a,b) in H.edges():
                        flag = 1
                if flag == 0:
                    L[u].remove(a)
                    update = 1

print("After Arc Consitency")
print_dict(L)

#print_dict(G_NS)

#Pair Consistency Setup
# need L(x,y) all possible images for x and y
uv_pairs = []
for u in G:
    for v in G:
        if u != v:
            uv_pairs.append((u,v))

ab_pairs = []
for a in H:
    for b in H:
        if a != b:
            ab_pairs.append((a,b))

ll = {}

for p in uv_pairs:
    u = p[0]
    v = p[1]
    ll[p] = []
    for q in ab_pairs:
        a = q[0]
        b = q[1]
        if a in L[u] and b in L[v]:
            if (G_SP[u][v] != H_SP[a][b]):
              continue 
            if (G_NS[u][v] != H_NS[a][b]):
              continue
            if (u,v) in G.edges() and (a,b) in H.edges():
                ll[p].append(q)
            if (u,v) not in G.edges() and (a,b) not in H.edges():
                ll[p].append(q)

# check the distance for uv and ab. 
#Pair Consistency Alg
#print("Before")
#print_dict(ll)

update = 1
while update:
    update = 0
    for p in ll:
        u = p[0]
        v = p[1]
        for q in ll[p]:
            a = q[0]
            b = q[1]
            for w in nodes_G:
                if (a,b) in ll[p]:
                    if w != u and w!= v:
                        flag = 0
                        for c in L[w]:
                            if flag != 0:
                                break
                            if c != a and c!= b:
                                if (a,c) in ll[(str(u),str(w))] and (b,c) in ll[(str(v),str(w))]:
                                    flag = 1
                        if flag == 0:
                            ll[(str(u),str(v))].remove((str(a),str(b)))
                            update = 1
print("After")
print_dict(ll)
#shortest_path_G(0,G_SP)

plt.figure(1)
nx.draw(G,with_labels=True)
plt.figure(2)
nx.draw(H,with_labels=True)
plt.show()