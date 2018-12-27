# SMPL：Skinned Multi-Person Linear Model

### 概括：

 SMPL模型是一种参数化人体模型，是马普所提出的一种人体建模方法，该方法可以进行任意的人体建模和动画驱动。这种方法与传统的LBS的最大的不同在于其提出的人体姿态影像体表形貌的方法，这种方法可以模拟人的肌肉在肢体运动过程中的凸起和凹陷。因此可以避免人体在运动过程中的表面失真，可以精准的刻画人的肌肉拉伸以及收缩运动的形貌

### 原理：

SMPL是使用`pose`和`shape`参数驱动的线性的人体模型，模型的主要参数有：`rest pose template`,`blend weights`,`pose-dependent blend shapes`,`identity-dependent blend shapes`,和一个从vertices到joint的`regressor`，这些参数都是是从训练数据中学习得来的。

SMPL的核心是shape形状参数![\beta](https://math.jianshu.com/math?formula=%5Cbeta)，和pose动作参数![\theta](https://math.jianshu.com/math?formula=%5Ctheta)到vertices和joint之间的映射的关系，即我们输入给定的shape和pose，通过模型可以得到相应的vertices和joint，通过vertices和joint我们就可以得到大致人体3D模型

SMPL的目标是创造一个可以表示不同形状的身体的，可以随着动作自然的变形的，并且软组织在运动过程中还能发生形变的 人体模型。SMPL其一采用了Blendshape方式，可以自然的从pose A 转换到pose B。比如我们现在有一个大笑的表情，和一个不笑的表情，我们可以通过blendshape方式将不笑逐渐过渡到大笑中。这样可以减少很多不必要的骨骼点；其二采用了骨骼蒙皮的技术，将顶点与关节关联起来，每个关节控制控制若干个不同的顶点，达到角色运动的效果。

### 模型参数：

模型的输入参数pose 形状参数![\beta](https://math.jianshu.com/math?formula=%5Cbeta)和shape动作参数![\theta](https://math.jianshu.com/math?formula=%5Ctheta)，模型输出是每个点vertices的坐标量。在该模型中，vertices = 6890 joint=23，论文中给定了72个pose和10个shape。

vertices：顶点，可以当成小三角形（四边形）组成，顶点越多模型就越精细。

joint参数都由一个三元组作为参数去控制，即![\vec{\omega}_k\in \mathbb{R}^3](https://math.jianshu.com/math?formula=%5Cvec%7B%5Comega%7D_k%5Cin%20%5Cmathbb%7BR%7D%5E3)，在SMPL中总共设置了23处关节。

pose参数是使用axis-angle（轴角的意思是，我们可以会用一个旋转轴方向的单位矢量和一个转过的角度的标量来表示一个旋转量）来定义的，每一个joint有三个维度，所以需要3个pose进行控制。（SMPL中有23处关节加上原点总共24处，所以pose参量个数为24*3=72）

shape参量为人体高矮胖瘦、头身比等比例的10个参数。

模型中还包括了一下几项（只要是为了处理如何将shape 和pose映射到相应的点和关节上）

**SMPL模型公式**：具体见论文处

**N**：表示vertices数量6890 **K**：表示关节的数量23

![\bar{\textbf{T}} \in \mathbb{R}^{3N}](https://math.jianshu.com/math?formula=%5Cbar%7B%5Ctextbf%7BT%7D%7D%20%5Cin%20%5Cmathbb%7BR%7D%5E%7B3N%7D) ,平均的模板形状 (mean template shape) 这个时候的pose是zero pose,(![\vec{\theta^*}](https://math.jianshu.com/math?formula=%5Cvec%7B%5Ctheta%5E*%7D))

![\mathcal{W}\in \mathbb{R}^{N\times K}](https://math.jianshu.com/math?formula=%5Cmathcal%7BW%7D%5Cin%20%5Cmathbb%7BR%7D%5E%7BN%5Ctimes%20K%7D) ,各个关节的混合权重。（骨骼蒙皮）

![B_S(\vec{\beta}):\mathbb{R}^{|\vec{\beta}|} \mapsto \mathbb{R}^{3N}](https://math.jianshu.com/math?formula=B_S(%5Cvec%7B%5Cbeta%7D)%3A%5Cmathbb%7BR%7D%5E%7B%7C%5Cvec%7B%5Cbeta%7D%7C%7D%20%5Cmapsto%20%5Cmathbb%7BR%7D%5E%7B3N%7D) ,blend shape函数，将shape参数映射到每一个点上（pose A与pose B 的自然过渡）

![B_P(\vec{\theta}):\mathbb{R}^{|\vec{\theta}|} \mapsto \mathbb{R}^{3N}](https://math.jianshu.com/math?formula=B_P(%5Cvec%7B%5Ctheta%7D)%3A%5Cmathbb%7BR%7D%5E%7B%7C%5Cvec%7B%5Ctheta%7D%7C%7D%20%5Cmapsto%20%5Cmathbb%7BR%7D%5E%7B3N%7D) ,将pose参数映射到每个点上

 ![J(\vec{\beta}):\mathbb{R}^{|\vec{\beta}|} \mapsto \mathbb{R}^{3K}](https://math.jianshu.com/math?formula=J(%5Cvec%7B%5Cbeta%7D)%3A%5Cmathbb%7BR%7D%5E%7B%7C%5Cvec%7B%5Cbeta%7D%7C%7D%20%5Cmapsto%20%5Cmathbb%7BR%7D%5E%7B3K%7D)，将shape参数映射到每个joint的位置上

模型输出：

最终得到的结果就是![M(\vec{\beta},\vec{\theta};\Phi):\mathbb{R}^{|\vec{\theta}|\times |\vec{\beta}|} \mapsto \mathbb{R}^{3N}](https://math.jianshu.com/math?formula=M(%5Cvec%7B%5Cbeta%7D%2C%5Cvec%7B%5Ctheta%7D%3B%5CPhi)%3A%5Cmathbb%7BR%7D%5E%7B%7C%5Cvec%7B%5Ctheta%7D%7C%5Ctimes%20%7C%5Cvec%7B%5Cbeta%7D%7C%7D%20%5Cmapsto%20%5Cmathbb%7BR%7D%5E%7B3N%7D) ,将shape和pose参数映射到每个点上，每个节点在空间上有三个维度。

### 应用扩展：

有别于其他的人体模型，SMPL可以进行人体骨骼蒙皮（Rig）和人体贴图。

+ 骨骼蒙皮（Rig）：建立骨骼点和顶点的关联关系。每个骨骼点会关联许多顶点，并且每一个顶点权重不一样。通过这种关联关系，就可以通过控制骨骼点的旋转向量来控制整个人运动

- 纹理贴图：动画人体模型的表面纹理，即衣服裤子这些。（这部分感觉是论文中主要讨论,因为SMPL是生成裸体的人物模型，如何将还原人体表面的细节纹理是进一步的要求）









