# 关于python SMPL数据的部分理解

文件：basicModel_f_lbs_10_207_0_v1.0.0.pkl

## 注意事项
1. 使用python2的cPickle库打开，python3不支持
1. 打开后是字典格式的数据

## 数据结构

字典项和对应的数据类型

未修改的SMPL模型，6890个点，13776个face

| 字典项 | 数据类型 | 备注 |
| - | - | - |
| J_regressor_prior | (24,6890) |
| f | (13776,3) | face，就是每个三角形，[i0,i1,i2]其中i是点的序号（0~6889）
| J_regressor | (24,6890) |
| kintree_table | (2,24) | kinematic tree
| J | (24,3)|
| weights_prior | (6890,24)|
| weights | (6890,24) |
| vert_sym_idxs | (6890) | 点的序号（0~6889）不是顺序的
| posedirs | (6890,3,207)
| pose_training_info | {一个字典}
| bs_style | string | "lbs"
| bs_type | string | "lrotmin"
| v_template | (6890,3) | 模型的局部空间坐标
| shapedirs | (6890,3,10) | 10shapes

## magic numbers

### 6890
SMPL模型中顶点的数量

### 13776
SMPL中face的数量，face就是mesh的一个面，论文中的应用都是三角形，所以字典中"f"项中每个元素都是三个顶点的下标，表示三角形的三个顶点

### 24
SMPL将模型分为了24个部分，可以保留实现

### 23
24个部分拼接需要23个拼合处，可以保留实现

### 10
10个shape，实现不需要修改

### 207
23*9 pose blend shape（参见SMPL论文），我们的实现应该不关心这个数字

### 110210
论文2中提出优化后的顶点数量。

原始SMPL模型中有6890个点和13776个面，每个面有三条边，每两个面共享一个边，因而SMPL中边（edge）的数量为
> num(e) =  13776*3/2 = 20664

细化后SMPL模型中多出的边数量为
> num(e_add) = 110210-6890 = 103320

均分到每个face上的点增量为
> num(e_add_per_face) = 103320/13776 = 7.5

这里7.5就是两次细化后（论文2 Figure3）中，中心的3个加上边上的9个（9/2=4.5）

优化目标是把顶点数量6890变成110210...涉及到几乎所有的数据

### 220416
每个face被分成16个部分
> 220416 = 13776 * 16









