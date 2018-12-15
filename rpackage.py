from gurobipy import *
dist_mt= [[0,   66.1007,   71.9911,   80.1807,    4.0441,   49.0771,   62.6661,   85.6245],
   [66.1007,         0,   80.9452,   65.1823,   68.1356,   68.4973,  106.5340,  151.4895],
   [71.9911,   80.9452,         0,  134.0825,   75.9730,   22.9174,  134.6030,  122.7266],
   [80.1807,   65.1823,  134.0825,         0,   78.6798,  114.6029,   72.7916,  152.9751],
    [4.0441,   68.1356,   75.9730,   78.6798,         0,   53.0649,   58.6549,   84.1754],
   [49.0771,   68.4973,   22.9174,  114.6029,   53.0649,         0,  111.7085,  107.3859],
   [62.6661,  106.5340,  134.6030,   72.7916,   58.6549,  111.7085,         0,   91.9076],
   [85.6245,  151.4895,  122.7266,  152.9751,   84.1754,  107.3859,   91.9076,         0]]


m=Model("Vehiclerouting")
x=m.addVars(8,8,vtype=GRB.BINARY)
ind=[]
for i in range(4):
    for j in range(8):
        if(i!=j):
            ind.append((i,j))
con1=quicksum(x[i] for i in ind)
m.addConstr(con1,GRB.EQUAL,1)      #constraint--1

ind=[]
for i in range(5,8):
    for j in range(8):
        if(i!=j):
            ind.append((i,j))
con2=quicksum(x[i] for i in ind)
m.addConstr(con2,GRB.LESS_EQUAL,1)      #constraint--2

ind1=[]
ind2=[]
for i in range(8):
    for j in range(8):
        if(i!=j):
            ind1.append((i,j))
            ind2.append((j,i))
con3=quicksum(x[i] for i in ind1)-quicksum(x[i] for i in ind2)
m.addConstr(con3,GRB.EQUAL,0)                       #constraint----3

ind=[i for i in range(8) if(i!=4)]
con4=quicksum(x[4,j] for j in ind)
m.addConstr(con4,GRB.LESS_EQUAL,4)              #constraint-----4

con5=quicksum(x[j,4] for j in ind)
m.addConstr(con5,GRB.LESS_EQUAL,4)              #constraint-------5

t=m.addVars(8,vtype=GRB.CONTINUOUS)

for i in range(8):
    for j in range(4):                                                  #constraint--------6a
        if(i!=j):
            exp=t[i]+(((dist_mt[i][j]*60)/40)-15)*x[i,j]-((11*60)*(1-x[i,j]))
            m.addConstr(exp,GRB.LESS_EQUAL,t[j])

for i in range(8):
    for j in range(5,8):                                                  #constraint--------6b
        if(i!=j):
            exp=t[i]+(((dist_mt[i][j]*60)/40)-15)*x[i,j]-((11*60)*(1-x[i,j]))
            m.addConstr(exp,GRB.LESS_EQUAL,t[j])

m.addConstr(t[4],GRB.GREATER_EQUAL,0)           #contraint-----------7
m.addConstr(t[4],GRB.LESS_EQUAL,11*60)

                                                                                    #constraint 8
for j in range(4):
    exp=(11*60)-15*(dist_mt[j][4]/40)
    m.addConstr(exp,GRB.GREATER_EQUAL,t[j])
for j in range(4,8):
    exp=(11*60)-30*(dist_mt[j][4]/40)
    m.addConstr(exp,GRB.GREATER_EQUAL,t[j])

for j in range(8):
    m.addConstr(t[j],GRB.GREATER_EQUAL,dist_mt[4][j])
y=m.addVars(8,vtype=GRB.CONTINUOUS)

for i in range(8):
    for j in range(5,8):                                                    #contraint--------9
        if(i!=j):
            exp=y[i]-(0.2*dist_mt[i][j]*x[i,j])+60*(1-x[i,j])
            m.addConstr(exp,GRB.GREATER_EQUAL,y[j])

for j in range(4,8):
    m.addConstr(y[j],GRB.EQUAL,60)                          #contraint----------10

minexp=quicksum(dist_mt[i][j]*x[i,j] for i in range(8) for j in range(8))

m.setObjective(minexp,GRB.MINIMIZE)


m.optimize()
m.write('mymodel.lp')
print(m.getAttr("X", m.getVars()))
