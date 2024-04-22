import networkx as nx
import matplotlib.pyplot as plt

H = nx.read_edgelist("graph_F.txt",create_using = nx.DiGraph())
G = nx.read_edgelist("graph_E.txt",create_using = nx.DiGraph())


print(H)

nodes_H = list(H.nodes)
nodes_G = list(G.nodes)


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



print("Before Distance")
print_dict(L)


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

# print("Distances")
# print_dict(sp_G)
# print_dict(sp_H)

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

L['4']= ['d']


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
            if (u,v) in G.edges() and (a,b) in H.edges():
                ll[p].append(q)
            if (u,v) not in G.edges() and (a,b) not in H.edges():
                ll[p].append(q)

#Pair Consistency Alg
print("Before")
print_dict(ll)

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


plt.figure(1)
nx.draw(G,with_labels=True)
plt.figure(2)
nx.draw(H,with_labels=True)
plt.show()