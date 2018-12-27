# SMPL学习笔记

### smpl论文中相关的知识：

##### Blend Skinning：

骨架空间变形方法，也称为混合剥皮法。将网格的表面附加到底层骨骼结构上。受邻近关节点的影响，网格曲面中的每个顶点都使用加权变换。smpl的核心公式一组映射从R的（3N * 3K *theta *W）----->  R的（3N）空间中，我们，其中 rest pose：T（3N）； joint locations： J（3K）； a pose：θ； blend weights：W。为了精细化模型，我们加上了shape blend shape项和pose blend shape项，即将rest pose细分为三项，T-pose标准姿势下各个顶点的坐标， shape blend shape offset项，pose blend shape offset项。W是blend weight 为了方便计算我们假设每个vertices只和4个关节点旋转有关。

##### Shape blend shapes：

通过线性的方程Bs来表示不同人的body shape。是一个从shape到vertices 的映射，具体的那内容可以参照smpl论文中的（8）。Bs = β*s。β是个关于的形状的参数。s是经过训练出来的针对每一个shape的vertices的位移量，大小是（3N * |β|）

##### Pose blend shapes：

与Shape blend shape不同的是Bp不是一个线性的公式，而是一个跟cos和sin有关的公式，大致的操作是用当前的旋转矩阵和rest pose的旋转矩阵之差乘以个pose blend shapes矩阵P。旋转矩阵（9*23 = 207）；pose blend shape矩阵（3N * 9K）。P是通过训练得到的。

##### Rodrigues formula：

罗德里格旋转公式是将一个向量按照旋转轴旋转一定的角度之后得到的新的向量，可以通过矩阵表示。爱smpl的论文中，通过改变换可以得到joint的旋转方向

##### Training：

smpl对两类数据集进行了训练，使对这两个dataset的重建的误差降到最小，这两个数据集分别是muti-pose和muti-shape包含了男性和女性。muti-pose的数据集主要展现的是人的不同的动作姿势；muti-shape主要展现的是人不同的形状，比如人的高低胖瘦。

这里的优化方法也是优化不同的能量项

优化参数的规模：

pose blend shapes：P（9K*3N）

shape blend shapes：S（3N * 3K）

以上两项乘以相应的参数矩阵均可以得到规模是（3N）的vertices offset的矩阵

joint regressor ：J（3N * 3K）

这项乘上vertices矩阵可以得到每个joint的坐标。

skinning weights： W（4 * 3N）

每个顶点和4个joint相关

data term：是注册得到的顶点和我们模型得到的顶点之差。

left-right asymmetry：这个惩罚项可以保证joint和mesh是对称。（计算 J 和 T 和其镜像之间的差值）

be close to this initial prediction：我们对模型划分成了24个区域，我们将每个关键点初始化成为每个区域的中心，我们希望模型中的关节点和初始化中的关节点的位置相差尽可能小。

以上步骤我们可以通过shape和pose得到估计的mesh的空间位置，但是仅仅知道mesh不够的，我们还需要通过mesh回归得到joint的位置信息，这里我们采取Joint regressor的方法。即我们可以通过几个稀疏的mesh对joint进行线性的关联，起到给每个joint定位的作用。

### smpl数据结构及代码分析：

##### 参量的表示：

`v_personal`：和v_template相同规模，是每个顶点的offse

`v_template`：顶点模板。所有的优化都是在这个基础上进行的

 `J`：关节坐标

`weight`：混合权重（关节点-顶点）

`kintree_table`：关节树

`f`:face由三个顶点构成

`bs_type`：蒙皮方法LBS还是DQBS

`posedirs`：pose的字典对应论文中的pose blend shapes

`shapedir`: shape的字典对应论文中的shape blend shapes

`trans`：平移量

`pose`：定义了pose的参数，关节个数*3（转轴方向，旋转角度）

`beta`：定义shape的参数

`J_regressor`：joint的回归矩阵，用于给joint定位

##### 代码分析：

在给的代码中，model文件夹下有smpl.py模块

在SMPL主模块中，给了两个参数`terms = 'model'`表示我们要读取的smpl的路径

`dterms = 'trans', 'betas', 'pose', 'v_personal'`对应论文一种公式（3），tran：表示基本的模板，beta：表示shape，pose：即pose，v_personal：表示我们的优化项D

对`tran`、`beta`、`pose`进行初始化：

```python
if not hasattr(self, 'trans'):
    self.trans = ch.zeros(3)
#trans是三维坐标中的位移量
if not hasattr(self, 'betas'):
    self.betas = ch.zeros(10)
#beta是shape的参数，总共有十个数据
if not hasattr(self, 'pose'):
    self.pose = ch.zeros(72)
#pose姿势的参量跟关节点的个数有关
```

接下来的代码是将序列化的模型（保存在pkl中）还原成为smpl模型，具体每个参数的意思可以见之前的参数列表。

```python
def joints_coco(smpl):
    J = smpl.J_transformed
    nose = smpl[VERT_NOSE]
    ear_l = smpl[VERT_EAR_L]
    ear_r = smpl[VERT_EAR_R]
    eye_l = smpl[VERT_EYE_L]
    eye_r = smpl[VERT_EYE_R]

    shoulders_m = ch.sum(J[[14, 13]], axis=0) / 2.
    neck = J[12] - 0.55 * (J[12] - shoulders_m)

    return ch.vstack((
        nose,
        neck,
        2.1 * (J[14] - shoulders_m) + neck,
        J[[19, 21]],
        2.1 * (J[13] - shoulders_m) + neck,
        J[[18, 20]],
        J[2] + 0.38 * (J[2] - J[1]),
        J[[5, 8]],
        J[1] + 0.38 * (J[1] - J[2]),
        J[[4, 7]],
        eye_r,
        eye_l,
        ear_r,
        ear_l,
    ))
```

因为smpl的joint数量多于coco数据集中的，所以这里选取一部分的joint用于和coco数据集中的joint进行比较。

```python
self.v_shaped = self.shapedirs.dot(self.betas) + self.v_template
```

每个shape参数点乘训练好的shape blend shapes矩阵，再加上每个顶点的模板信息，得到每个vertices的空间坐标。

```python
self.v_shaped_personal = self.v_shaped + self.v_personal
```

加入自定义的offset

```python
self.J = ch.sum(self.J_regressor.T.reshape(-1, 1, 24) * self.v_shaped.reshape(-1, 3, 1), axis=0).T
```

通过joint的回归矩阵，得到每个joint的空间坐标

```python
self.v_posevariation = self.posedirs.dot(posemap(self.bs_type)(self.pose))
```

pose参量按照给定的蒙皮的方式点乘训练好的pose blend shapes矩阵，得到每个vertices的offset

```python
self.v_poseshaped = self.v_shaped_personal + self.v_posevariation
```

结合了shape from shapes 和pose from shapes之后的每个vertices的空间坐标

