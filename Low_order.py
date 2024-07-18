import networkx as nx
import matplotlib.pyplot as plt

from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, LpStatus, lpSum, value


#H = nx.read_edgelist("graph_H.txt")
#G = nx.read_edgelist("graph_G.txt")

#GC = nx.complement(G)
#HC= nx.complement(H)

#G = nx.read_edgelist("graph_E.txt",create_using = nx.DiGraph())




import networkx as nx
import matplotlib.pyplot as plt

def Isomorphism (group_1, group_2):

    Gr= nx.read_edgelist(group_1, nodetype=int,
      data=(('label',int),), create_using=nx.DiGraph())
    Hr= nx.read_edgelist(group_2, nodetype=int,
    data=(('label',int),), create_using=nx.DiGraph())
     
    
     
    G={}
    for u in Gr.nodes():
        G[u]=nx.DiGraph()
        for v in Gr.nodes():
            G[u].add_node(v)
    for u in Gr.nodes():
        for v in Gr.nodes():
            for w in Gr.nodes():
                if (Gr[v][w]["label"]==u):
                    G[u].add_edge(v,w)
         
    #print("the graph")
    #print( G[2].edges())      
     
    H={}
    for a in Hr.nodes():
        H[a]=nx.DiGraph()
        for b in Hr.nodes():
            H[a].add_node(b)
    for a in Hr.nodes():
        for b in Hr.nodes():
            for c in Hr.nodes():
                if (Hr[b][c]["label"]==a):
                    H[a].add_edge(b,c)              
        
    
     
    ### Compute the order of each element
    #e_g=Gr.nodes(0)
    #print(e_g)
    flag=0
    for u in Gr.nodes():
        if flag==0 :
         for v in Gr.nodes():
             if v== u:
                 continue
             if (Gr[u][v]["label"]==v):
                 flag=1
                 e_g=u
                 break
    #print(e_g)  
     
    Gr_ord={}
    for u in Gr.nodes():
        Gr_ord[u]=5
        count=1
      
        v=u
        while (v != e_g) :
            for w in G[u].neighbors(v):
                v=w
                count=count+1
        Gr_ord[u]=count     
     
    #print("G orders is ")
    #print(Gr_ord)
    flag=0
    for a in Hr.nodes():
        if flag==0 :
          for b in Hr.nodes():
              if b== a:
                  continue
              if (Hr[a][b]["label"]==b):
                  flag=1
                  e_h=a
                  break
    #print(e_h)  
     
    Hr_ord={}
    for a in Hr.nodes():
        Hr_ord[a]=5
        count=1
      
        b=a
        while (b != e_h) :
            for c in H[a].neighbors(b):
                b=c
                count=count+1
        Hr_ord[a]=count     
     
     
    #print("H orders is ")
    #print(Hr_ord)
    #print(Hr_ord)  
        
    #list_1=Gr_ord.sort()
    #list_2=Hr_ord.sort()
    list_1=[]
    list_2=[]
     
    for u in Gr.nodes():
      list_1.append(Gr_ord[u])
    for a in Hr.nodes():
      list_2.append(Hr_ord[a])
    list_1.sort()
      
    list_2.sort()
    #print(list_1)
    #print(list_2)
    
    # if list_1 != list_2 :
    #    print("No group isomorphism")
    #    exit()  
     
    ## Here we create the single lists :
    ## we could figure out the list of strongly_connected components in G[u] and
    ## H[a]in   
    L = {}
    list_strong_G=[]
    list_strong_H=[]
    for u in Gr.nodes():
        L[u] = []
        for a in Hr.nodes():
          
            list_strong_G= [len(v) for v in sorted(nx.strongly_connected_components(G[u]),
                                                   key=len, reverse=True)]
            list_strong_H=[len(c) for c in sorted(nx.strongly_connected_components(H[a]),
                                                   key=len, reverse=True)]
          
            if (Gr_ord[u] == Hr_ord[a] and list_strong_G==list_strong_H):
             L[u].append(a)
    
    #print(":L:")
    #for i in L:
    #   print(f"{i}: {L[i]}")
    # ########################################################################################
    # #Helper Function
    # ########################################################################################
    def print_dict(dic):
       for i in dic:
            print(f"{i}: {dic[i]}")
      
    # ##########################################################################################
    # #Pre-Processing
    # ##########################################################################################
     
           
        
     
    # #Main Arc consistency
    # #########################################################################################
     
     
    D_G={}
    D_H={}
    n_g=len(Gr_ord)
    n_h=len(Hr_ord)
    #print("n_g is")
    #print(n_g)
    RG={}
    for u in Gr.nodes():
        for v in Gr.nodes():
            if( Gr[u][e_g]["label"]==v):
                RG[u]=v
                break
    #print(RG)      
     
    RH={}
    for a in Hr.nodes():
        for b in Hr.nodes():
            if( Hr[a][e_h]["label"]==b):
                RH[a]=b
                break
    for u in Gr.nodes():
        D_G[u]={}
        for v in Gr.nodes():
            D_G[u][v]={}
            for w in Gr.nodes():
                D_G[u][v][w]=n_g+1
     
    G_SP={}  # size of the shortest path
    #G_NS={}  # number of shortest path
    for u in Gr.nodes():
        G_SP[u]={}
    #   G_NS[u]={}
        for v in Gr.nodes():
          G_SP[u][v]=n_g+1
      #    G_NS[u][v]=0
     
    ### we compute shortest path for every pair of vertices in G[u] and DG[u][v][w]
    ## shows the length of the shortest path from v to w in G[u]...
    ## G[u][v][w]=t means that vu^t=w in the gruop. 
     
    for u in Gr.nodes():
      
        for x in Gr.nodes():
            for y in Gr.nodes():
              G_SP[x][y]=n_g+1
      
        for x in G[u].nodes():
            G_SP[x][x]=0
      
        for x in G[u].nodes():
            for y in G[u].neighbors(x):
                if (x != y):
                 G_SP[x][y]=1
      
        #max_dis=0;
        for z in G[u].nodes():
            for x in G[u].nodes():
              for y in G[u].nodes():
                if (z==x or z==y or x==y):
                    continue
                if (G_SP[x][z]+G_SP[z][y] < G_SP[x][y]) :
                    G_SP[x][y]=G_SP[x][z]+G_SP[z][y]
      
        for v in G[u].nodes():
            for w in G[u].nodes():
                D_G[u][v][w]=G_SP[v][w]
     
    #print("distances in D_G[0]")
    #print(D_G[2])
    ## end of computing G[v][w][u] ...          
       
    for a in Hr.nodes():
        D_H[a]={}
        for b in Hr.nodes():
            D_H[a][b]={}
            for c in Hr.nodes():
                D_H[a][b][c]=n_h+1
     
    H_SP={}  # size of the shortest path
    #G_NS={}  # number of shortest path
    for a in Hr.nodes():
        H_SP[a]={}
    #   G_NS[u]={}
        for b in Hr.nodes():
          H_SP[a][b]=n_h+1
      #    G_NS[u][v]=0
     
    ### we compute shortest path for every pair of vertices in H[u] and D_H[a][b][c]
    ## shows the length of the shortest path from b to c in H[a]...
    ## H[a][b][c]=t means that ba^t=c in the gruop H
           
    for a in Hr.nodes():
      
        for d in Hr.nodes():
            for c in Hr.nodes():
              H_SP[d][c]=n_h+1
      
        for d in H[a].nodes():
            H_SP[d][d]=0
      
        for b in H[a].nodes():
            for c in H[a].neighbors(b):
                H_SP[b][c]=1
      
        #max_dis=0;
        for d in H[a].nodes():
            for b in H[a].nodes():
              for c in H[a].nodes():
                if (d==b or d==c or b==c):
                    continue
                if (H_SP[b][d]+H_SP[d][c] < H_SP[b][c]) :
                    H_SP[b][c]=H_SP[b][d]+H_SP[d][c]
      
        for b in H[a].nodes():
            for c in H[a].nodes():
                D_H[a][b][c]=H_SP[b][c]
     
     
    update = 1
    while update:
        update = 0
        for u in Gr.nodes():
            for v in Gr.nodes():
                if (u ==v ):
                    continue
                for w in Gr.nodes():
                    if (w==u):
                        for a in L[u]:
                            flag=0
                            for b in L[v]:
                                if(D_H[a][a][b]==D_G[u][u][v]):
                                    flag=1
                                    break
                            if (flag == 0 ) :
                              L[u].remove(a)
                              update = 1  
                    if (w==v):
                         for a in L[u]:
                             flag=0
                             for b in L[v]:
                                 if(D_H[b][a][b]==D_G[v][u][v]):
                                     flag=1
                                     break
                             if (flag == 0 ) :
                               L[u].remove(a)
                               update = 1   
                               
                    if (w != u and w!=v):         
                     for a in L[u]:
                       flag=0                  
                       for b in L[v] :
                         for c in L[w] :
                           if (D_H[c][a][b] == D_G[w][u][v]):
                             flag = 1
                             break
                         if (flag==1):
                          break
                       if (flag == 0 ) :
                        L[u].remove(a)
                        update = 1
    #print(":L:")
    #for i in L:
    #  print(f"{i}: {L[i]}")
    
    
     
     
    ## Now creating the ll list based on D_G and D_H
    #G[u] :
       
    #     for every w, D_G[w] : distance from u to v in G[w]
    #    for every c distance from  a to b in  H[c]
     
     
    #Pair Consistency Setup
    # need L(x,y) all possible images for x and y
    uv_pairs = []
    for u in Gr.nodes():
        for v in Gr.nodes():
            if u != v:
                uv_pairs.append((u,v))
     
     
    ll = {}
     
     
    for p in uv_pairs:
        u = p[0]
        v = p[1]
        ll[p] = []
      
        for a in L[u] :
            for b in L[v]:
      
                ## compute the list of distances for u,v and distances for a,b
                flag=0
                list_dis_G=[]
                list_dis_H=[]
                for w in Gr.nodes():
                    list_dis_G.append(D_G[w][u][v])
                  
                for c in Hr.nodes():
                    list_dis_H.append(D_H[c][a][b])
              
                flag_m=1
                for w in Gr.nodes():
                    flag=0
                    for c in L[w]:
                        if (D_H[c][a][b] == D_G[w][u][v]):
                            flag=1
                            break
                    if flag==0 :
                        flag_m =0;
                        break
                  
                      
                        #list_dis_G.append(D_G[w][u][v])
              
                list_dis_G.sort()
                list_dis_H.sort()
                if (RG[u]!=v ):
                  if ( list_dis_G == list_dis_H and flag_m==1) :
                    ll[p].append((a,b))
                if (RG[u]==v):
                   if ( list_dis_G == list_dis_H and flag_m==1 and RH[a]==b) :
                     ll[p].append((a,b))
                  
     
               
     
     
    #ll = {}
    #print("Before")
    #print_dict(ll)
     
     
    ## Further updating the pair lists ll(u,v) :
    ## for a given integet t< n. A_1={ w | uw^t=v : D_G[w][u][v]=t }
    ## for t let A_2={ c | ac^t=b: D_H[c][a][b]=t}
    ## if |A_2| != |A_1| the (a,b) is not in ll(u,v)  check if c is in L(w)
     
     
   
    update = 1
    while update:
        update = 0
        for p in uv_pairs:
            u = p[0]
            v = p[1]
            for q in ll[p]:
                a = q[0]
                b = q[1]
                for w in Gr.nodes():
                    #if (a,b) in ll[p]:
                    if w != u and w!= v:
                        flag = 0
                        for r in ll[(u,w)] :
                            c=r[1]
                            if (a != r[0]):
                                continue
                            if (b,c) in ll[(v,w)]:
                                flag = 1
                                break  
                        if flag == 0:
                            if (a,b) in ll[(u,v)] :
                              ll[(u,v)].remove((a,b))
                              update = 1
                              #print("something removed")
     
    # print("After")
    # print_dict(ll)
     
    update = 1
    while update:
        update = 0
        for p in uv_pairs:
            u = p[0]
            v = p[1]
            for q in ll[p]:
                a = q[0]
                b = q[1]
                for w in Gr.nodes():
                    #if (a,b) in ll[p]:
                    if w != u and w!= v:
                        for x in Gr.nodes():
                            for y in Gr.nodes():
                                s1=D_G[x][u][w]
                                s2=D_G[y][v][w]      
                        
                        flag = 0
                       
                        if (x==v and u!=y) :
                            for r in ll[(u,w)] :
                                c=r[1]
                                if (a != r[0]):
                                    continue
                                if (b,c) in ll[(v,w)]:
                                    for j in L[y]:
                                        if (D_H[b][a][c] == s1 and D_H[j][b][c]==s2) :
                                          flag = 1
                                          break 
                            if flag == 0:
                                if (a,b) in ll[(u,v)] :
                                  ll[(u,v)].remove((a,b))
                                  update = 1         
                       
                        if (x!=v and u==y) :
                           for r in ll[(u,w)] :
                             c=r[1]
                             if (a != r[0]):
                                continue
                             if (b,c) in ll[(v,w)]:
                                for j in L[y]:
                                    if (D_H[j][a][c] == s1 and D_H[a][b][c]==s2) :
                                          flag = 1
                                          break  
                           if flag == 0:
                            if (a,b) in ll[(u,v)] :
                              ll[(u,v)].remove((a,b))
                              update = 1
                              #print("agian something removed")
                        
                        if (x!=v and u!=y):
                            for r in ll[(u,w)] :
                                c=r[1]
                                if (a != r[0]):
                                    continue
                                if (b,c) in ll[(v,w)]:
                                    for i in L[x] :
                                        for j in L[y]:
                                            if (D_H[i][a][c] == s1 and D_H[j][b][c]==s2) :
                                              flag = 1
                                              break  
                            if flag == 0:
                                if (a,b) in ll[(u,v)] :
                                  ll[(u,v)].remove((a,b))
                                  update = 1
                                  #print("agian something removed")
     
    #print("After")
    #print_dict(ll)
import os 

already_done={32,16,8,81,25,44,64}
for i in range (55,101):
   if (i in already_done):
       continue
   print(i)
   string_name='/Users/arafiey/Documents/low-order/order'+str(i)+'/'
   files=[os.listdir(string_name)]
   f=files[0]
   for file_1 in range(len(f)):
        for file_2 in range(len(f)):
            if file_1 >= file_2 :
                continue 
            f_1=string_name+str(f[file_1])
            f_2=string_name+str(f[file_2])
            Isomorphism(f_1, f_2)
           # print("file_1")
           # print(f_1)  
           # print("file_2")        
           # print(f_2)
   
    #print(files)
  
# files=[os.listdir('/Users/arafiey/Documents/low-order/order16/')]

# #print(files)

# #for i in range(len(files))
# # for f in files :
# f=files[0]
# #for i in range(len(f)):
# #print(f[i]) 
    
# for file_1 in range(len(f)):
#     for file_2 in range(len(f)):
#         if file_1 >= file_2 :
#             continue 
#         f_1='/Users/arafiey/Documents/low-order/order16/'+str(f[file_1])
#         f_2='/Users/arafiey/Documents/low-order/order16/'+str(f[file_2])
#         # group_1='Documents/low-order/order32/'+f_1
#         # group_2='Documents/low-order/order32/'+f_2
#        # print("file_1")
#        # print(f_1)  
#        # print("file_2")        
#        # print(f_2)
#      #   Isomorphism(f_1, f_2)
#         #print("enter a number")
#         #variable=input()
        
        
#         # Gr= nx.read_edgelist(f_1, nodetype=int,
#         #   data=(('label',int),), create_using=nx.DiGraph())
        
#         # Hr= nx.read_edgelist(f_2, nodetype=int,
#         #  data=(('label',int),), create_using=nx.DiGraph())
        
       
    


# #LP programming starts here : 

# model = LpProblem(name="Isomorphism", sense=LpMaximize)    
# X={}
# for u in G.nodes():
#     X[u]={a: LpVariable(name=f"X{u,a}", lowBound=0, upBound=1,cat='Continues') for a in H.nodes() }
    
# for u in G.nodes():
#     for a in H.nodes():
#         if (a not in L[u]):
#             model+=(X[u][a]<=0)

# for u in G.nodes():
#     expression=sum(X[u][a] for a in L[u])
#     model+=(expression==1)

# for u in G.nodes():
#     for v in G.nodes():
#         if (u==v):
#             continue 
#         for a in L[u]:
#             for b in L[v]:
#                 if ( (str(a),str(b)) not in ll[str(u),str(v)]):
#                     model+=(X[u][a]+X[v][b] <=1)
                 
# model+=1

# status = model.solve()

# print(f"status: {model.status}, {LpStatus[model.status]}")
# print(f"objective: {model.objective.value()}")

# for var in model.variables():
#     print(f"{var.name}: {var.value()}")




# plt.figure(1)
# nx.draw(G,with_labels=True)
# plt.figure(2)
# nx.draw(H,with_labels=True)
# plt.show()