# Subdivided SMPL body model And modelling with own video

### 细化模型

##### 概论:

原本的smpl的模型中，使用了6890个点，13776个面。对于一个3D的model来说，这样的点面数量略有稀疏，在模型展示的时候可以明显的分辨出表面的mesh快，所以作者在论文的第一部分中就将模型做了细化，细化后的模型将拥有110210 点，和220416个面。细化后的模型更加细致平滑，人体表面没有明显mesh。

##### 细化原理

在原始的smpl的模型中，有6890个顶点和13776个mesh，并且通过pkl保存下来了。v_template中记录的是所有顶点的三维的坐标，而f中记录的是组成每一个mesh的顶点的编号。作者通过拉普拉斯平滑优化在原有的顶点集中加入新的顶点。

![1](./src/1.png)

顶点Vi和Vj属于同一条边，新加入的顶点是Vi和Vj的中点并且可以沿着该点的法向量做微小的位移s。该点的法向量n是所在面的法向量之和。偏移量s由拉普拉斯优化得到（拉普拉斯优化请详见repo，大致的思想是空间中一个点的位置和其相邻的点位置相关，每一个相邻点会带来一个惩罚项，优化的目标是保证总的惩罚项最小）。经过拉普拉斯处理后的结果可以表示如下：

![1](./src/2.png)

简化后：

![1](./src/3.png)

##### 实现的困难

由于我们的电脑的内存的资源有限，而模型的大小和顶点的平方成正比。如果按照论文中的要求，顶点的数量增加了16倍，导致所需要的内存资源增加了256倍，会导致memory error所以我们做了一定的简化，最终生成的模型的顶点数量是之前的4倍，总共27554给顶点

##### 代码的实现

- 应用的库：

  ```python
  #读取模型pkl
  import cPickle as pkl
  import scipy.sparse as sp
  #非线性规划模块
  from scipy.optimize import minimize
  #可视化展示的模块
  from OpenGL.GL import *
  from OpenGL.GLU import *
  from OpenGL.GLUT import *
  #进行矩阵的运算
  from numpy import *
  import numpy as np
  import sys
  ```

  特别的，我们这里使用scipy模块中的optimize进行优化，使拉普拉斯惩罚项的值最小。

- 建立smpl模型图矩阵：

  由于我们知道了每个face是由哪些顶点组成的，即哪些顶点是相邻的，所以我们可以由此建立起该模型的图相邻矩阵。每一个新加的顶点的初始位置是每条边的中值。

  ```python
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
  ```

  由于考虑到了内存不够的问题，我们这里使用了稀疏矩阵。因为该矩阵中大多数位置都为0，每个点之和其周围的6个点相连。我们只要记录矩阵中有数据的row和col，即可还原出整个矩阵。

  生成稀疏矩阵：

  `adj = sp.coo_matrix((data,(row,col)),shape=(node_num,node_num))`

- 对图矩阵进行归一化

  ```python
  weight = adj.sum(axis = 1)
  jj = 0
  for x in adj:
      if weight[jj]>0:
          adj[jj] = x / weight[jj]
      jj= jj+1    
  kk = 0
  
  ```

- 进行拉普拉斯优化

  ```python
  def opt(node_position):
      global adj,kk,new_dd,node_num
      kk = kk+1
      node_position = np.reshape(node_position,(node_num-6890,3))
      res = adj.dot(np.concatenate([v_template,node_position]))-np.concatenate([v_template,node_position])
      res = (res*res).sum(axis = 1)
      res = pow(res,0.5).sum()
      if kk %500 == 0:#itelate 500 and stop
          kk  = 1
          print res
          new_dd = node_position #only new node
          new_dd = np.concatenate([np.reshape(node_position,(node_num-6890,3)),v_template]) #new node and fix node
          #new_dd = v_template #fix node
          main() #show 3D model
          y=input("to stop the procedure") #stop
      return res
  ```

  将所有的邻接点乘上对应的矩阵减去该点原有的位置，可以得到拉普拉斯坐标下各个点的位置，我们可以通过多轮优化得到其最小值。

  ```python
  result = minimize(opt, new_node_position, method='SLSQP')
  ```

  使用minimize自带的SLSQP进行非线性规划。


##### 优化比较：

+ 训练收敛：

  ![center](./src/4.jpg)

+ 原始模型和细化后模型对比：

  ![center](./src/4000-500.png)

  ![center](./src/4000-500-2.png)

  我们对原有的模型的一半进行细化训练，左右对比后效果明显。



