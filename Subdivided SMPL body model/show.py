import cPickle as pkl
import scipy.sparse as sp
from scipy.optimize import minimize
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import numpy as np
import sys
row = []
col = []
data = []
node_num = 6890

#3D model
def init():
    glClearColor(1.0,1.0,1.0,1.0)
    gluOrtho2D(-5.0,5.0,-5.0,5.0)
#3D model
def plotfunc():
    global new_dd
    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(0.1, 0,5,0)
    glColor3f(1.0,0.2,0.6)
    glPointSize(3.0)

    glBegin(GL_POINTS)
    for x in new_dd:#from -5.0 to 5.0 plus 0.1 every time
        glVertex3f(2*x[0],2*x[1],2*x[2])

    glEnd()
    glFlush()
#3D model
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(0,0)
    glutInitWindowSize(1000,2000)
    glutCreateWindow("Function Plotter")
    glutDisplayFunc(plotfunc)
    glutIdleFunc(plotfunc)
    glutMainLoop()


def opt(node_position):
    global adj,kk,new_dd
    kk = kk+1
    node_position = np.reshape(node_position,(223,3))
    res = adj.dot(np.concatenate([v_template,node_position]))-np.concatenate([v_template,node_position])
    res = (res*res).sum(axis = 1)
    res = pow(res,0.5).sum()
    if kk %500 == 0:#itelate 500 and stop
        kk  = 1
        print res
        new_dd = node_position #only new node
        new_dd = np.concatenate([np.reshape(node_position,(223,3)),v_template]) #new node and fix node
        new_dd = v_template #fix node
        main() #show 3D model
        y=input("to stop the procedure") #stop
    return res
    
def add_new_node():
    ii = 0
    for x in f:
        ii= ii+1
        global node_num,row,col,data,new_node_position,v_template
        x0 = x[0]
        x1 = x[1]
        x2 = x[2]
        s01 = str(x0)+str(x1)
        s10 = str(x1)+str(x0)
        s02 = str(x0)+str(x2)
        s20 = str(x2)+str(x0)
        s12 = str(x1)+str(x2)
        s21 = str(x2)+str(x1)
        v0 = 0
        v2 = 0
        v1 = 0
        if dict.has_key(s01) == False:
            dict[s01] = node_num
            dict[s10] = node_num
            v0 = node_num
            new_node_position[node_num-6890][0] = (v_template[x0][0] +v_template[x1][0])/2
            new_node_position[node_num-6890][1] = (v_template[x0][1] +v_template[x1][1])/2
            new_node_position[node_num-6890][2] = (v_template[x0][2] +v_template[x1][2])/2
            node_num = node_num+1
            row = np.concatenate([row,[x0,v0,x1,v0]])
            col = np.concatenate([col,[v0,x0,v0,x1]])
            data = np.concatenate([data,[1,1,1,1]])
        else:
            v0 = dict[s01]
        if dict.has_key(s02) == False:
            dict[s02] = node_num
            dict[s20] = node_num
            v1 = node_num
            new_node_position[node_num-6890][0] = (v_template[x0][0] +v_template[x2][0])/2
            new_node_position[node_num-6890][1] = (v_template[x0][1] +v_template[x2][1])/2
            new_node_position[node_num-6890][2] = (v_template[x0][2] +v_template[x2][2])/2
            node_num = node_num+1
            row = np.concatenate([row,[x0,v1,x2,v1]])
            col = np.concatenate([col,[v1,x0,v1,x2]])
            data = np.concatenate([data,[1,1,1,1]])
        else:
            v1 = dict[s02]
        if dict.has_key(s12) == False:
            dict[s12] = node_num
            dict[s21] = node_num
            v2 = node_num
            new_node_position[node_num-6890][0] = (v_template[x1][0] +v_template[x2][0])/2
            new_node_position[node_num-6890][1] = (v_template[x1][1] +v_template[x2][1])/2
            new_node_position[node_num-6890][2] = (v_template[x1][2] +v_template[x2][2])/2
            node_num = node_num+1
            row = np.concatenate([row,[x1,v2,x2,v2]])
            col = np.concatenate([col,[v2,x1,v2,x2]])
            data = np.concatenate([data,[1,1,1,1]])
        else:
            v2 = dict[s12]
        row = np.concatenate([row,[v0,v1,v0,v2,v1,v2]])
        col = np.concatenate([col,[v1,v0,v2,v0,v2,v1]])
        data = np.concatenate([data,[1,1,1,1,1,1]])
        if ii == 100: #100 face 7113 node total
            break
#load from pkl
dd = pkl.load(open("basicModel_f_lbs_10_207_0_v1.0.0.pkl","rb"))
#init
f = dd['f']
betas = np.zeros(10)
v_template = dd['v_template']
v_personal = np.zeros_like(v_template)
shapedirs = dd['shapedirs']
J_regressor = dd['J_regressor']
J =J_regressor.dot(v_template)

kintree_table = dd['kintree_table']
bs_type = dd['bs_type']
weights = dd['weights']
posedirs = dd['posedirs']
vert_sym_idxs = dd['vert_sym_idxs']
v_shaped = shapedirs.dot(betas) + v_template
dict = {str(0):0}

new_node_position = np.zeros((7113-6890,3))
#create new node
add_new_node()

print node_num #7113 node
#adj is matrix for graph if adj[i][j] == 1 mean there is an edge between i and j
adj = sp.coo_matrix((data,(row,col)),shape=(7113,7113))
adj = adj.toarray()
#print adj
weight = adj.sum(axis = 1)
jj = 0
#¹éÒ»»¯
for x in adj:
    if weight[jj]>0:
        adj[jj] = x / weight[jj]
    jj= jj+1
    
kk = 0
#minimize 
result = minimize(opt, new_node_position, method='SLSQP')
print(result.fun)
print(result.success)
print(result.x)
new_dd = np.reshape(result.x,(223,3))
main()
