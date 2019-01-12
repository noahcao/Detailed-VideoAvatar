# OpenDR: An Approximate Differentiable Renderer学习笔记

---

## 关键词 ##
### 1. Inverse graphics ###
*Inverse graphics* 是指**逆图像化**，与**图像化**是一个相反的过程。“图像化”是通过一些参数（几何信息、光照、材质，etc）来**渲染**（*render*）得到图像。“逆图像化”就是指从sensor data（图片、视频、体感数据，etc）中推测得到几何信息、光照信息等参数。   
这两个过程相结合，就可以从sensor data中提取信息，然后产生模型数据来仿真和拟合真实情景。

### 2. Renderer ###
Renderer是指**渲染器**，负责处理图像化的过程，即利用参数来生成图片/模型

### 3. Differentiable Renderer ###
OpenDR是一个开源框架，DR指**Differentiable Renderer（可微的渲染器）**，也就是说，它具有这样的功能：    
（1）能通过给定的参数来**渲染**图像   
（2）能自动对这些参数进行**求导**，从而进行**局部优化**   
OpenDR是基于OpenGL、OpenCV和Chumpy（提供auto differentiation）搭建的

----------


## 简介 ##
OpenDR的**前向渲染过程**可以简单理解成一个函数$f(\Theta)$，其中$\Theta$ 就是渲染用到的参数的集合。而最简单的**优化过程**也就是使rendered image intensities和observed image intensities之间的difference最小。这个difference可能是由各种复杂的函数定义的，但是核心思想都是要让合成的图像和实际的图像之间区别最小

----------


## 前向过程-渲染 ##
前面已经提到渲染函数$f(\Theta)$，这里将$\Theta$总的分解为三个参数：**V**（vertex locations），**C**（ camera parameters ）和 **A**（per-vertex brightness ）。即$\Theta = {V, C, A}$    

forward model主要进行以下几个近似：
### 1. Appearance（A）：

>  Per-pixel surface appearance is modeled as **product of mipmapped texture and per-vertex brightness**, such that brightness combines the effects of reflectance and lighting. 
每个像素的值都是纹理数据和每点的光照乘积，所以像素的亮度就反映了反射项和光照项的共同作用。

关键词：texture；per-vertex brightness；

### 2. Geometry （V）

>  We assume a 3D scene to be approximated by triangles, parameterized by vertices V , with the option of a background image (or depth image for the depth renderer) to be placed behind the geometry
3D信息是通过点组成的三角面片表示的，背景图像、深度图像可以作为几何信息的附加信息。

关键词：vertices；background image；depth image；

### 3. Camera (C) 

> We approximate continuous pixel intensities by their sampled central value.
使用连续像素的采样中心值来近似像素的强度。相机投影模型是来自OpenCV的 pinhole-plus-distortion camera projection model。

总的来说，openDR的渲染过程与其他的图像管线（graphics pipelines）大体是相同的。关键的区别在于，其他pipeline支持的是per-pixel的渲染函数，而openDR支持的是**per-vertex**的渲染函数

----------
## 对前向过程进行微分 ##
### Part0 ：中间变量U ###
为了描述在求偏导的过程，引入中间变量**U**，U表示**2D的投影点坐标**  
整个求偏导的过程遵循链式法则：   

![链式法则][1]

### Part1 ：Differentiating Appearance ###

> Pixels projected by geometry are colored by the product of texture T and appearance A; therefore ∂f ∂A can be quickly found by rendering the texture-mapped geometry with per-vertex colors set to 1.0, and weighting the contribution of surrounding vertices by rendered barycentric coordinates. 

由于几何投影的像素是通过texture T和appearance A乘积来进行着色的，所以通过将与纹理对应的点的颜色设为1.0，并通过对周围点的重心坐标进行加权，就可以得到$\delta f/\delta A$  
> Partials ∂A ∂V may be zero (if only ambient color is required), may be assigned to built-in spherical harmonics or point light sources, or may be deﬁned directly by the user.

$\delta A/\delta V$与设置的光照有关，如果只有环境光就是0  

### Part2 ：Differentiating Projection ###
由于image的值是通过2D投影来与3D坐标和相机参数产生联系的，换言之，f通过U与C和V产生联系，所以有：
$$ \frac{\delta f}{\delta V} = \frac{\delta f}{\delta U}\frac{\delta U}{\delta V},\frac{\delta f}{\delta C} = \frac{\delta f}{\delta U}\frac{\delta U}{\delta C}$$
其中$\delta U/\delta V$和$\delta U/\delta C$都是OpenCV直接提供的

### Part3 ：Differentiating Intensity with Respect to  2D Image Coordinates  ###
这里篇幅比较长，而且都是一些具体做法。大致是这样的过程：（1）将所有的像素点分区：遮挡边界像素点和内部像素点（2）在此基础上将每个像素划分为三类：interior, interior/boundary, 和 many-boundary 中的一类，使用不同的filter进行处理

----------
## 代码演示 ##
在论文的第5和第6部分讲解了两个demo的代码，推荐阅读，在这里就不分析了

----------
## 需要利用openDR做的工作 ##
1.区分出3D facial landmarks    
2.构造3D facial landmarks的project rays    
3.建立2D facial landmark和相关rays的static map    

[1]: http://m.qpic.cn/psb?/V13Ti98m05LW5b/PJ.th52wDmEWP7e3kKKxtdFE4inZgveuDT0UJjAn*Ek!/b/dL8AAAAAAAAA&bo=uQGZAQAAAAADFxI!&rf=viewer_4
