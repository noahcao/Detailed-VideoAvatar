# Detailed Video Avatar

We did several works in this project, including:

1. Based on [videoavatar](https://github.com/thmoa/videoavatars)，which is the officially released source code of the paper [“Video Based Reconstruction of 3D People Models”](http://arxiv.org/abs/1803.04758), the project did human body reconstruction.
3. We implemented the "mesh subdivision" and "medium-level shape reconstruction" techniques proposed in the paper ["Detailed human avatars from monocular video"](https://arxiv.org/abs/1808.01338)(Detailed Avatars), achieving detailed reconstruction of human body.
4. We built a version of videoavatar with supporting Python3.x, [chumpy](https://github.com/mattloper/chumpy)and [opendr are rewritten to support it.
5. We developed a convenient model rendering and visualization tools, to get the final visualization results of video avatar with texture added.

We note that: although this README is written in English, many other texts in this project is written in Chinese, please feel free to contact us if you find anything hard to understand. Besides, some other features in "Detailed Avatar" are still to be implemented, we only realized the main two.

# File Organization

```shell
|-- Render: rendering tools 
|-- snapshot：a demo based on one teammate\'s handsome selfie
|-- docs					
	|-- final_report：a conclusion report in Chinese
	|-- Notes：other notes, nothing to do with the project
|-- code					
	|--	MLBSR: implementation of Medium-level Body-shape Reconstruction
	|-- SSBM: implementation of Subdivided SMPL model
	|-- Portable_py3.x：Python 3.x support of opendr and chumpy
	|-- videoavatar：original videoavatar project files
```

# DEMO

![](./assets/base_demo.gif)

With several simply obtained selfies, we can build the 3D body reconstruction as follows. We note that the camera parameters are important to produce reliable reconstruction.

![](assets/snapshot1.png)

![](assets/snapshot2.png)

We produce the face reconstruction w/ and w/o techniques proposed in the "Detailed Avatar" paper. The right faces in the following two images are produced with those techniques. 

![](./assets/face_adjust.png)

We produce the body reconstruction in a cloud point manner w/ and w/o techniques proposed in the "Detailed Avatar" paper. The comparison effect is remarkable.

![](./assets/subdivision.png)

---

*Members of our team：[Jinkun Cao](https://github.com/noahcao)、[Yuqi Hu](https://github.com/ReimuYk)、[Yuchen Luo](https://github.com/592McAvoy)、[Nuo Chen](https://github.com/199ChenNuo)、[Erhu Feng](https://github.com/fengerhu1)*. *Thanks for their contributions, and especially for the selfies provided by handsome Erhu Feng*

*Note that this project is just a non-official attempt of implementing detailed-avatars, to refer this work, please cite the original publication.*

