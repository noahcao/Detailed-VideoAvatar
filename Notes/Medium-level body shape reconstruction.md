# 第一篇论文对应此部分内容  

1. segmentation  
通过一个CNN网络，将（K=120帧）关键帧的前景和背景分开

1. 2D landmarks -> 3D pose  
基于2D landmarks来恢复3D的pose。  
方法是使用SMPL的逆函数，将约束锥（轮廓图的光线）转换成SMPL的标准T-pose

# 第二篇论文  
为了得到更精细的面部细节，第一篇论文中计算能量的等式被修改为了等式（5） (加了面部能量项)  

等式（5）的 Esilh和Eregm在第一篇论文中已经讨论过，这里着重讲[Eface](#e-face)。

1. <span id="map">面部landmark和mesh点的映射</span>
```
landmark <---barycentric interpolation(重心插值)---> mesh->points
```
每个landmark *l* 通过与邻近顶点的[重心插值](#gravity)被映射到表面。  
在[优化Eface项](#e-face)的时候，landmark是一个点，所以猜测这里的重心插值就是根据很多个点，以及这些点的比重，来计算目标点（也就是landmark）的位置 

2. <span id="openpose">使用openpose得到的关键点：</span>  
```json
"people":[
    {
        "people":[x0,y0,score0,x1,y1,score1...],
        "face_keypoints":[x0,y0,score0,x1,y1,score1...],
        "hand_left_keypoints":[x0,y0,score0,x1,y1,score1...],
        "hand_right_keypoints":[x0,y0,score0,x1,y1,score1...],
    }
]
```
这里只讨论"face_keypoints"  
得到的数据中，共有70个面部关键点（每个关键点有三个值:(x, y, score)）  

这些关键点对应位置如下：
![facial-landmark](https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/doc/media/keypoints_face.png)  

3. <span id="e-face">Eface的计算</span>  
Eface是对**2D脸部关键点** 与 **3D脸部关键点的2D投影**之间的距离的惩罚。  
2D关键点来自于[openpose的关键点检测](#openpose)（即上面的2.）  
针对Eface的优化过程：  
    1. 测量模型上的landmark: $\vec{l}$，和对应的camera ray: $\vec{r}$之间的点线距离  
        点线距离： 
        ```latex
        $ \delta(\vec{l}, \vec{r}) = \vec{l} x \vec{r_n} - \vec{r_m}$
        ```
        这里的$\vec{r}$是在unpose空间中，用来描述2D landmark的ray，并且由[普朗克坐标(Pluker Coordinate)](#pluker)来描述：  
        ```
        $\vec{r} = (\vec{r_n}, \vec{r_m})$
        ```
        其中，$\vec{r_n}$是**r**的方向向量，$\vec{r_m}$是力矩，具体定义见[普朗克坐标](#pluker)  
    1. 计算Eface  
        ```
        $ E_face = \sum_{\vec{l}, \vec{r} \in L} \omega_l \rho ( \delta (\vec{l_l}, \vec{r_r}))
        ```
        其中，  
        $L$定义了landmark和mesh中点的[映射](#map)  
        $\omega$是CNN网络给出的landmark的可信度（这个RNN是在哪里定义的？）  
        $\rho$是[Geman-McClure robust cost function](#geman)  
        为了加快计算过程，3.2使用的是粗糙的SMPL模型（来自于第二篇论文中，等式(1)的定义）  

# 一些名词
1. <span id="gravity">重心插值</span>  
可以用类比cv课上颜色/灰度插值算法的内容来理解。  
举一个最简单的一维坐标例子，有两个点`p1(x1)`和`p2(x2)`，  
那么给定权重w，点P可以表示为：  
```
P(w) = w*x1 + (1-w)x2
```

2. <span id="pluker">普朗克坐标 Pluker Coordinates</span>  
普朗克坐标是用来表示线的一种方法,可以快速的判断两条3D空间内的线是否重合，快速计算他们之间的距离  
普朗克坐标定义方法：  
给定线 $l$上任意两点P0(x0, y0, z0)和P1(x1, y1, z1)，计算该线段的方向向量 $\vec{d}$ 和原点到这两个点的向量的叉乘结果 $\vec{m}$   
普朗克坐标：
$ \vec{l}=(\vec{d} ; \vec{m}) $
```
    $(\vec{d}, \vec{m}) $
= $(\vec{p0} - \vec{p1}, \vec{p0} x \vec{p1}) $
= $((x0-x1, y0-y1, z0-z1), (x0, y0, z0)x(x1, y1, z1))$
```
其中:  
​    x: 叉乘cross product  
​    第一个向量规定了线的方向向量，第二个向量又被称为“力矩”

3. <span id="geman">Geman-McClure函数</span>  
错误函数: $ \rho (x) = \frac{1}{2} \frac{x^2}{x^2 + \sigma^2 } $  
其中$\sigma$是一个协调参数
# 参考  
1. [改进的核回归图像恢复（包含Geman-McClure)](http://www.docin.com/p-1234969747.html)  
1. [维基百科Plücker coordinates](https://en.wikipedia.org/wiki/Pl%C3%BCcker_coordinates)  
1. [openpose官方文档](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md)

