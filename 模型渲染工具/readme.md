# 1. 使用说明

本文档为模型渲染工具的说明。该工具能够将模型和纹理渲染出来，并比较真实的展现出模型效果。

项目地址（源代码）：[https://github.com/199ChenNuo/cv-visualization](https://github.com/199ChenNuo/cv-visualization)   
可执行文件： [https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/tree/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/%E5%B7%A5%E5%85%B7/loader](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/tree/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/%E5%B7%A5%E5%85%B7/loader)

## 1.1 使用  
批处理文件 *run.bat* 可执行文件 *loader.exe*
1. **[推荐] 运行 *run.bat* 文件**  
    将含有模型和贴图的文件夹拖到 *run.bat* 上运行即可  
    ![run-bat](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/run-bat.png)   

<center>图1. 使用`run.bat`运行可视化工具</center>  

2. 直接运行 *loader.exe* 可执行文件  
    双击即可，在弹窗内输入模型文件夹位置

    文件夹位置，即包含了模型和纹理的文件夹。  
（'/'和'\\'分隔符均支持）  
例如：  
- 文件夹： c:/models/femal-1-sport
- 模型路径：c:/models/femal-1-sport/consensus.obj
- 纹理路径：c:/models/femal-1-sport/tex-female-1-sport.jpg  
用户输入 `c:/models/female-1-sport`即可。(见下图)  

<span id="pic-1"></span>
![user-input](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/%E7%94%A8%E6%88%B7%E8%BE%93%E5%85%A5.png)  
<center>图2. 用户输入</center>  

![dir](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/%E6%96%87%E4%BB%B6%E5%A4%B9%E7%BB%93%E6%9E%84.png)  
<center>图3. 文件路径</center>  

3. 命令行运行  
    命令行指定文件夹位置：  
    ```shell
    > loader.exe c:/models/femal-1-sport
    ```
    或者命令行执行文件后，在弹窗内输入文件夹位置  
    ```shell
    > loader.exe
    ```
    同[图1](#pic-1)
    ```shell
    (cout) Model path:
    (cin)  c:/models/femal-1-sport
    ```
注：文件命名规范应与论文给出的开源数据集相同，即纹理命名应为`tex-文件夹名.jpg`。模型名称应为`consensus.obj`

## 1.2 对渲染窗口的操作

| 按键 | 效果 |
| :-: | :-: |
| 回车 | 暂停（继续）旋转 |
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

通过 'AWSD' + '上下左右' 8个键可以对模型位置做更精准的调整，便于观察。

![result](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C.png)
<center>图4. 渲染效果</center>  

旋转效果可以参照本repo中的demo文件夹下的 [*.gif*](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/tree/master/demo) 文件  

## 1.4 使用注意事项
使用平台为Win10。  
其他需要的库、资源文件一同打包在文件夹中，请不要删除。  

---

# 2. 程序说明

## 2.1 语言框架说明  
使用C++编程，可视化采用 OpenGL 4.3。  

## 2.2 展现内容
obj模型以及贴图  

## 2.3 对obj模型的优化      
1. 法向量  
为了加入反射来展现出模型的真实感，需要计算模型表面mesh的法向量进而获得光照情况。  
论文代码生成的 *.obj* 文件中并没有加入法向量。  
为了得到法向量，曾经尝试通过Maya软件修改 *.obj* 文件（详见[3.1.2 Maya手动添加](#"3-1")）来为模型定义表面反射模型（Phong模型光照）    
因为使用Maya计算法向量效率太低，所以后期进行了其他探索，最终选择在OpenGL中导入模型时计算法向量。

2. uv映射和贴图  
代码生成的贴图是和模型的uv映射的契合的，只要贴上贴图即可。由于代码 *.obj* 已经定义了uv映射，因此只要指定贴图文件即可。   
![uv](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/uv.png)
<center>图5. {模型表面的mesh | 模型表面的uv映射 | 纹理图片}的对比</center>  


3. 细化mesh  
在使用[assimp库](http://assimp.sourceforge.net/lib_html/index.html) 导入模型时会将过大的mesh细化为小网格，并且所有mesh均用三角形表示。  
```c++
Assimp::Importer importer;
// aiProcess_SplitLargeMeshes: 将大Mesh分割成小的子Mesh
const aiScene* scene = importer.ReadFile(modelFile, aiProcess_SplitLargeMeshes);
```

由于实时渲染的资源限制，在单次`Draw()`中能绘制的的三角形数目和最大顶点缓冲是有限的。  
通过指定mesh的网格限制和顶点限制可以有效的缓解这个问题。  
```c++  
// Vertice最多个数
#define AI_SLM_DEFAULT_MAX_VERTICES 10000000
// Triangle最多个数
#define AI_SLM_DEFAULT_MAX_TRIANGLES 10000000   
```

## 2.4 代码说明   

1. 说明  
使用OpenGL、glfw库、glad库等来开发本项目。  
主要目的是可视化出论文代码生成的模型，并且尽量简化用户需要的操作。  

2. 主要文件  

```c++
main.cpp    // 定义顶层函数 & 与用户的交互
model.cpp   // 定义模型类 & 导入模型 & 导入纹理
camera.cpp  // 定义了摄像机类 
Shader.h    // 定义了着色器类
```
1. 主要逻辑  
加载模型完成后会进入展示模型的循环。直到用户按下Esc的时候再退出。  
![pipeline](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/pipeline.png)  
<center>图6. 运行逻辑</center>  

3. 库  
```
    glfw      3.2  
    glad      0.1.28  
    glm       0.8.9.5   
    assimp    3.1.1  
```
---

# 3. 遇到的困难

## 3.1 模型与纹理的贴合
在将纹理贴合到模型上时，尝试了几种思路

### 3.1.1 直接改动文件
通过修改 *.obj* 文件，新增 *.mtl* 文件来实现渲染效果  

1. 步骤：
    1. 读取 *.obj* 文件
    1. 在 *.obj* 文件中指定 *.mtl* 文件
    1. 生成与 *.obj* 文件对应的 *.mtl* 文件
    1. 在 *.mtl* 文件中指定模型表面性质与 *.jpg* 纹理文件

1. 缺点：
    1. 面的法向量难以计算
    1. 会改变原有模型

### <span id="3-1">3.1.2 Maya手动添加模型与纹理的映射关系</span>
通过渲染编辑器中的HyperShader来为模型指定表面光照模型和表面纹理，导出文件时生成模型表面法向量。    

1. 操作步骤：  
    1. 导入模型  
    ```
    文件 -> 导入 -> 选择模型文件  
    ```    

    2. 进入HyperShader中为模型添加反射模型（实例中选择了Phong光照模型）    
    ``` 
    进入HyperShader: 
        窗口 -> 渲染窗口 -> HyperShader
    添加光照模型：    
        在左下角窗口的“表面”下选择“Phong”
    ```   
    ![add-phone](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/add-phone.png)  
    <center>图7. 使用Maya添加表面光照模型</center>  

    3. 在HyperShader中为模型添加来自文件的2D纹理，选择与导入的模型对应的纹理图片   
    ```
    添加来自文件的纹理：
        在左下角窗口中的“2D纹理”下选择文件
        在右侧窗口中选择纹理文件所在位置
    ```   
    ![choose-tex](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/choose-tex.png)   
    <center>图8. 使用Maya指定纹理</center>  

    操作2.和3.最终会为模型表面增加两个“节点”。
    ![maya-add-tex](https://github.com/noahcao/Detailed-Human-Avatars-from-Monocular-Video/blob/master/%E6%A8%A1%E5%9E%8B%E6%B8%B2%E6%9F%93%E5%B7%A5%E5%85%B7/assets/maya-add-tex.png)   
    <center>图9. Maya操作总览</center>  

    4. 导出全部文件: *consensus.obj, consensus.mtl, tex-xxx-x-xxx.jpg*   
    ```
    文件 -> 导出全部 -> 选择位置&设置文件名
    ```   

1. 缺点：
    1. 操作周期长，效率低
    2. 会改变原有模型
    3. 需要安装Maya
    3. 在Maya中直接查看可视化效果不好

### 3.1.3 最终方案
不改动论文代码生成的文件，导入模型时计算法向量并直接为 *.obj* 模型文件指定纹理图片。 

1. 步骤： 
修改了 `Model.{h, cpp}` 文件，使用 Assimp 的 Importer 导入模型后，修改判断模型是否有纹理的逻辑代码。  
即使模型没有指定纹理，也在文件夹中搜索和文件夹名匹配的 *.jpg* 文件，如果找到文件名匹配的文件，那么将该文件作为模型的纹理。  

> Model.h
```cpp
// 模型类 
class Model{
    private:
        // 存储了模型的纹理
        vector<Texture> textures_loaded;
    public:
        // 导入纹理
        vector<Texture> loadMaterialTextures(...);
};
```
> Model.cpp
```cpp
vector<Texture> Model::loadMaterialTextures(...){
    for (unsigned int i = 0; i < TextureCount; i++)
    {
        // 如果 .obj 文件中指定了纹理图片
        //     那么从文件中导入纹理并加入到textures_loaded中
    }
    // 如果没有指定文件
    if (textures_loaded.size() == 0) {
        // 从文件夹中寻找对应'tex-文件夹名.jpg'的文件
        // 读取文件并加入到texture_loaded中
    }
}
```

2. 优缺点：
    1. 未修改原模型文件，不用生成新文件
    1. 可移植性好，不用安装多余的软件

## 3.2 *loader.exe* 文件在一些电脑上无法正常启动  
启动程序会报错：`应用程序无法正常启动0xc000007b`

1. 导致这个问题的常见原因  
    - 电脑没有安装 DirectX 9.0 或者 DirectX 9.0 组件损坏  
    - 电脑没有安装 Microsoft Visual C++
    - 电脑上没有安装 .NET

    经过5台环境不同的win10电脑试验后，确认是没有安装 Microsoft Visual C++ 的原因。（安装了 Visual Studio 的电脑可以正常启动）   
    但是考虑到可视化工具应该尽量轻量级，并且使用简单，因此要求用户安装 Microsoft Visual c++ 肯定是不合理的。

2. 本项目中的具体原因   
    OpenGL需要使用32位的库，而之前打包的库为64位的库。  

    由于已经打包了项目所需的所有dll文件，所以运行 *loader.exe* 时并没有提示缺失库文件或者库文件错误。  
    参考[在Windows平台用visual studio编译的可执行文件部署时报：应用程序无法正常启动0xc000007b（跟DirectX9无关的原因）](https://blog.csdn.net/xiejiashu/article/details/61209920),猜测同样是 *.dll* 文件版本不对。  
    将打包的依赖库从VS库文件夹中的 *.dll* 中替换为 *C:\Windows\SysWOW64* 32位库文件夹下的同名 *.dll* 后，程序在前面测试的5台电脑上都可以正常启动，于是确定是库文件位数的原因。  

3. 解决方法  
    将打包的 *.dll* 文件替换为32位的 *.dll* 文件  

# 4. 参考

1. [assimp开源库官方文档-细化mesh](http://assimp.sourceforge.net/lib_html/postprocess_8h.html)

2. <span id="ref-2">[优化Assimp库导入模型的过程](https://learnopengl-cn.github.io/03%20Model%20Loading/03%20Model/)</span>

3. [天空盒资源](http://www.custommapmakers.org/skyboxes.php)
