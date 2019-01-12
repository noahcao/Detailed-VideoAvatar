# Detailed Human Avatars from Monocular Video学习笔记



---

## I、 Four Inportant New Aspects ##
1. Facial landmarks     
将2D人脸识别信息植入到3D模型的构建中

2. shape-from-shading     
通过阴影来复原一些褶皱等细节信息

3. texture stitching
- multi-labeling assignment
- texture update energy function

4. semantic texture stitching

## II、 Three Construction Steps ##
### 0. Subdivided SMPL body model ###
（1）目标：将原始的SMPL模型的每条边进行两次细分，得到具有110210个vertice和220416个face的更detail的模型（对比原始的N=6890，F=13776）      
     
（2）新增顶点的计算公式：     
> $$v_{N+e} = 0.5(v_i + v_j) + s_en_e$$

    v_i,v_j:组成一条边的两个顶点
    n_e:v_i和v_j的平均法矢量
    s_e: n_e方向上的位移

在对原始模型进行细分之后，得到了精模Mf(β,θ,D,s) ，其中s是细分过程中所有新顶点的位移矢量的集合。通过优化s使如下公式所示的误差值最小，从而得到细化的光滑模型：
>  $$arg\min_s( LM_f = \sum_{j}w_{ij}(v_i - v_j) )$$

    v_j:与v_i相邻的顶点
    w_ij:余切权重
    L： Laplace matrix 

（3）疑问： 

 - 法矢量怎么计算？
 - 顶点及其相邻的点在SMPL中是怎么表示的？
 - 最后的优化公式中的w是怎么得到的？
 - 最后的优化公式中L是怎么被使用的？


----------


### 1. Medium-level body shape reconstruction  ###
(1) 时机：unpose完成之后    

(2) 需要数据：关键帧的face landmark  

(3) 使用模型：粗粒度的SMPL model（没有细分过的）    

(4) 优化公式：    

> $$arg\min_{\beta,D} ( E_{silh}+E_{face}+E_{regm})$$

其中,$E_{silh}$来自paper1（公式4）, $E_{regm}$就是step2中的几个正则项:

> $$ E_{regm} = w_{lp}E_{lp} +w_{lp}E_{lp} +w_{var}E_{var} +w_{sym}E_{sym} $$

$E_{face}$可以类比paper1中的$E_{data}$,$E_{data}$惩罚的是顶点和剪影对应的ray之间的距离，类似的，$E_{face}$惩罚的是识别出的face landmark（来自file）和模型上的对应投影之间的距离。 
> $$E_{face} = \sum_{l,r} w_lρ(δ(l,r))$$
l : landmark  
r : ray

注意到file中的face landmark格式为（x,y,score),这里的score就是$w_l$, ray是3D模型中对应的点的投影光线，他们之间的距离计算应该可以调用现有的函数
 
（5）疑问：

 - 待优化的参数D指的是什么？
 - 3D模型中的landmark投影光线应该怎么得到？

 


----------


### 2. Modeling ﬁne-level surface details  ###
（1）总体过程：
1. 从K = 60个关键帧中使用shape-from_shading提取细节
2. 递增的将一个个detail merge到一起


----------


### 3. Texture generation ###


