# 1. 使用说明

本文档为模型渲染工具的说明。该工具能够将模型和纹理渲染出来，并比较真实的展现出模型效果。

项目地址：[https://github.com/199ChenNuo/cv-visualization](https://github.com/199ChenNuo/cv-visualization)

## 1.1 使用
1. **[推荐] 运行 *.bat* 文件**  
    双击 *.bat* 后将文件夹拖到弹窗内即可即可。
1. 直接运行 *loader.exe* 可执行文件  
    双击即可，在弹窗内输入模型文件夹位置

    文件夹位置，即包含了模型和纹理的文件夹。  
（'/'和'\\'分隔符均支持）  
例如：  
- 文件夹： c:/models/femal-1-sport
- 模型路径：c:/models/femal-1-sport/consensus.obj
- 纹理路径：c:/models/femal-1-sport/tex-female-1-sport.jpg  
用户输入 `c:/models/female-1-sport`即可。(见下图)  

![user-input](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/tree/master/)

![dir](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/tree/master/)


1. 命令行运行  
    命令行指定文件夹位置：  
    ```shell
    $ loader.exe path-to-model
    ```
    或者命令行执行文件后，在弹窗内输入文件夹位置  
    ```shell
    $ loader.exe
    ```
    ```shell
    (cout) Model path:
    (cin)  path-to-model
    ```



注：文件命名规范应与论文给出的开源数据集相同，即纹理命名应为`tex-文件夹名.jpg`。模型名称应为`consensus.obj`


## 1.2 对渲染窗口的操作

| 按键 | 效果 |
| :-: | :-: |
| 回车 | 暂停/继续 旋转 |
| Esc | 退出 |
| A | 向左平移 |
| D | 向右平移 | 
| S | 后退 |
| W | 前进 |
| 方向键·左 | 模型向左旋转 |
|方向键·右|模型向右旋转| 
| 方向键·上| 视点上移 |
| 方向键·下|视点下移|

总结：AWSD是改变用户的视角，上下左右是改变模型的位置。


## 1.3 工具渲染效果  

模型在窗口中央，不停的绕模型的法线旋转，360°展示模型效果。  
按下回车键（约0.15s）会暂停旋转，再次按下（约0.15s）会继续旋转。  

旋转效果可以参照本repo中的demo问价夹下的 [*.gif*](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/tree/master/demo) 文件  

## 1.4 使用注意事项
使用平台为Win10。  
其他需要的库、文件一同打包在文件夹中，请不要删除。  

---

# 2. 程序说明

1. 语言框架说明  
使用C++编程，可视化采用 OpenGL 4.3。  

1. 展现内容
obj模型以及贴图  

1. 对obj模型的优化  
*并未修改obj文件，仅在导入模型时计算相关数据*   
- 法向量  
为了加入反射来展现出模型的真实感，需要计算模型表面mesh的法向量进而获得光照情况。  
论文代码生成的 *.obj* 文件中并没有加入法向量。  
为了得到法向量，曾经尝试通过Maya软件修改 *.obj* 文件（详见[3.1Maya手动添加](#"3-1")）来为模型定义表面反射模型（Phong模型光照）    

- uv映射&贴图  
代码生成的贴图和模型的uv映射的契合的，只要贴上贴图即可。由于代码 *.obj* 已经定义了uv映射，因此只要指定贴图文件即可。

- 细化mesh  
在导入模型时会将过大的mesh细化为小网格，并且所有mesh均用三角形表示。  

---

# 3. 其他渲染尝试

## <span id="3-1">3.1 Maya手动添加</span>
通过渲染编辑器中的HyperShader来为模型指定法向量，表面反射模型和表面纹理。    


## 3.2 改动文件
通过修改 *.obj* 文件，新增 *.mtl* 文件来实现渲染效果

## 3.3 最终方案
不改动论文代码生成的文件，导入模型时计算法向量，手动指定纹理图片。  

遇到的问题：

1. 纹理没有被渲染出来，只能看到黑色的轮廓  
    - 原因： 模型中没有指明纹理位置
    - 解决： 在渲染时指定
1. 模型没有法向量，渲染时没有反射光线，效果看起来很虚假。
    - 解决：
    1. 渲染过程中导入模型时，计算法向量。（这样不需要改动原有 *.obj* 文件）
1. 在没有安装VS的电脑上，启动程序会报错：[应用程序无法正常启动0xc000007b](https://blog.csdn.net/xiejiashu/article/details/61209920)     
    - 原因：在打包依赖库时，我放了64位的dll文件。但是由于OpenGL只有32位的库，所以在没有安装VS的电脑上程序无法启动。（VS中带有32位的库，64位系统不自带）。  
    - 解决：改用32位的dll之后，应用程序可以正常启动。