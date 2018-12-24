# Detailed Human Avatars from Monocular Vid

### step1 细化SMPL模型

我们的方法是基于SMPL进行人体建模。然而，原始的SMPL模型过于粗糙，无法对服装皱纹和精细面部特征等细节进行建模。所以我们需要完善SMPL模型

M(β, θ, D) = W(T(β, θ, D), J(β), θ,W) (1)T(β, θ, D) = T + Bs(β) + Bp(θ) + D (2)

这里的改善模型和第一篇论文中的相仿，都是通过增加一项offset项对每一个点进行微调

我们可以通过过M的逆函数将一个建立好的模型unpose成一个标准的T-pose函数

在第二篇论文中，我们为了细分每一条边，加入了一类新的顶点：

vN+e = 0.5(vi + vj ) + sene, (i, j) ∈ Ee  (3)

### step2:. Medium-level body shape reconstruction

首先联系第一篇论文，通过预处理好的关键帧的数据，我们可以通过2D画面预估出3D的姿势，然后再unpose成为标准地T-pose，之后基于阴影，对称性等损失量，对模型的shape进行优化，但是该过程对人脸的细节处理不够精准。所以作者提出了一个新的形体估计的公式：

arg min （Esilh + Eface + Eregm ）(5)
β,D
这里和第一篇论文中有点类似，将面部的三维模型的二维投影和在关键帧中的二维信息进行匹配，损失量为顶点到ray之间的距离。

### step3:Modeling fine-level surface details

通过剪影我们可以获得中的粒度的细节，但是无法获得更加精细的表面特征，所以这里作者采用了 shape-from-shading.

+ **shape-from-shading**

  对于每一针我们通过CNN分解方法，将图像分解成为反射比和留下的阴影。函数HC计算模型中顶点C留下的阴影。我们需要将模拟得到的阴影和观察得到的阴影相差最小。

  arg min |Hc(ni) − Is(Pvi)| , (8)

  p是投影矩阵用于计算观察得到的阴影，Hc能够计算模型中顶点留下的阴影。

  之后加入了两个惩罚下，一个是拉普拉斯光滑项，另一个是顶点到阴影距离的梯度项

+ **Surface reconstruction**

  这里我们还是使用step1，step2中的方法，对面部先进行unpose，然后在我们优化面部曲面使其更加自然，加入轮廓项，face项，shape-from-shading项，regf项{match：相邻关键帧差异的惩罚项（ warp-field），lap:光滑项，struc：通过改变边的长度保持mesh}等等。最后我们要做到使等式（11）尽可能的小。

### step4:Texture generation

+ **Partial texture generation:** 

  这一步其实就非常简单，就是将我们可见的颜色映射到相应的纹理中去。

+ **The semantic prior**

  我们将输入帧的每一个像素贴上语义的标签（这里总共给出了10个语义标签）然后我们将每一帧的语义信息融合到全局的语义map中使代价最小，具体可见等式16,17。公式16输入的label和该frame中实际的label一样则返回给定值，其余情况则返回0；公式17，为了实现代价最小，这里模拟了图上色的问题，每一个标签分配一种颜色？

+ **Texture merging**

  通过纹理k中t的颜色值之间的Mahalanobis距离表示这两个纹理之间的结构差异。我们保证了相邻纹理分配给相似的颜色，所以最后我们只要保证不同区域颜色的梯度值最小，即分配最为合理。

