# Medium-level body shape reconstruction 

根据face landmark对模型面部vertex进行调整

---
## Usage ##
### 1. 替换文件 ###

> - /lib    
  ---> frame.py    
  ---> rays.py   
> - /models    
  ---> bodyparts.py    
> - --->run_step2.sh    
> - --->step2_consensus.py   
   
### 2. 生成face_landmark.hdf5 ###
使用face2hdf5.py, 根据OpenPose识别出的face keypoint文件生成face_landmark.hdf5

    $ python face2hdf5.py <path_to_subject_directory> <face_landmark.hdf5>
如果使用脚本来运行模型生成过程，则生成的hdf5文件**必须命名为face_landmark.hdf5**，且需要放置在和其他数据文件（如mask.hdf5）同一目录下

### 3. 生成模型 ###
与之前的step2运行方式一致
   
    $ ./run_step2.sh <path_to_subject_directory> <output_directory> [options]"


----------


## 实现代码详解 ##

### (1). face2hdf5.py ###
读取由OpenPose处理得到的每帧画面的face landmark识别结果，将多个json文件中的相关数据将存储为一个dataset，并保存为hdf5格式   
实现过程类似于/prepare_date/2djoints2hdf5.py
```python
    ...
    with h5py.File(out_file, 'w') as f:
        poses_dset = f.create_dataset("face_landmark", (len(pose_files), 70*3), 'f', chunks=True, compression="lzf")
    
        for i, pose_file in enumerate(tqdm(pose_files)):
            with open(pose_file) as fp:
                pose = np.array(json.load(fp)['people'][0]['face_keypoints'])
                poses_dset[i] = pose
```

### (2). bodypart.py ###
定义了函数get_face_vertex_ids()，以获取SMPL模型中面部的vertex id
```python
    def get_face_vertex_ids():
        v_ids = get_bodypart_vertex_ids()
        return v_ids['face']
```        
### (3). frame.py ###
定义了函数setup_frame_rays_paper2，用于替换原有的setup_frame_rays
```python
    def setup_frame_rays(base_smpl, camera, camera_t, camera_rt, pose, trans, mask)
    def setup_frame_rays_paper2(base_smpl, camera, camera_t, camera_rt, pose, trans, mask, face_landmark)
```
新函数比原来多了一个face_landmark参数，指的是这一帧的面部landmark数据
```python
    def setup_frame_rays_paper2(base_smpl, camera, camera_t, camera_rt, pose, trans, mask, face_landmark):
        ... //与原函数相同
        
        # paper2
    
        # shape (70,3)->(x,y,scores)
        f.face_landmark = np.array(face_landmark).reshape(-1, 3) 
        f.face_rays = rays_from_landmark(f.face_landmark, camera)
    
        return f
```
为每一个frame对象新增了face_landmark和face_rays两个属性

```
    face_landmark：对应70个面部关键点的（x, y, confidence_score），shape为（70,3）
    face_rays：由face_landmark得到的2D投影光线，shape为（70, 2, 3）
```

### (4). rays.py ###
1.定义函数rays_from_landmark，由2D landmark构造camera rays 
```python
  def rays_from_landmark(landmark, camera):
        points = landmark[:,:-1] #array((x1,y1)(x2,y2)...)
        rays = rays_from_points(points, camera)
        return rays
```
得到的rays对应论文中提到的：

> the corresponding camera ray r describing the 2D landmark detection in unposed space
    
    
2.定义函数select_rays，对3D vertex和landmark rays进行匹配，并对rays进行unpose处理，整个过程类似于 select_and_unpose 函数
```python
    def select_rays函数中还返回了一个w—_idx,z这一项对应论文中：
    (rays, Vi, smpl, face_ids):
        # find face vertexs 
        v_ids = face_ids
        verts = smpl.r[v_ids]
    
        # calculate vert-ray distance
        n, m = plucker(rays)
        dist = np.linalg.norm(np.cross(verts.reshape(-1, 1, 3), n, axisa=2, axisb=1) - m, axis=2)

        # for every ray, find closest vertex
        ray_matches = np.argmin(dist, axis=0) #for each ray -> idx of closest vertex
        vert_matches = np.argmin(dist, axis=1) #for each vertex -> idx of closest ray
        
        # unpose rays
        ...
        
        # find valid matching
        valid_rays = dist[np.vstack((ray_matches, range(dist.shape[1]))).tolist()] < 0.12
        valid_verts = dist[np.vstack((range(dist.shape[0]), vert_matches)).tolist()] < 0.03
         
        ray_matches = ray_matches[valid_rays]
        
        # idx of w - w: confidence of landmark
        w_idx = np.concatenate((np.arange(rays.shape[0])[valid_rays], vert_matches[valid_verts]))
         
        return np.concatenate((v_ids[ray_matches], v_ids[valid_verts])), \
               np.concatenate((rays_u_r[valid_rays], rays_u_v[valid_verts])),\
               w_idx
```
整个过程对应论文中：

> ...establish a static mapping between landmarks and points on the mesh

构造mapping关系的方式与第一篇论文中构造boundary vertices和silhouette rays的对应关系的方式相同，即通过计算面部所有vertex和所有face rays之间的距离，分别为每个vertex匹配最近的ray，为每个ray匹配最近的vertex，最后将两个匹配的结果进行合并，返回一一对应的vertex id以及ray矩阵    

注意到在select_rays函数中还返回了一个idx矩阵w_idx, w指的是论文中：

> the conﬁdence of the landmark given by the  CNN

即每个ray的标记可信度，返回的w_idx矩阵这一项被用在了能量项的计算中   


3.定义了ray_face函数，计算E_face能量项

   > $$ E_{face} = \sum_{l,r\in L} w_l\rho (\delta(l_l, r_r)) $$

```python
    def ray_face(f, sigma, base_smpl, camera, face_ids):
        camera.t[:] = f.trans
```
得到static mapping关系和landmark conﬁdence id
```
        f.v_ids, f.rays_u, w_idx = select_rays(f.face_rays, f.Vi, base_smpl, face_ids)
```
获取id对应的vertex，计算点线距离$(\delta(l_l, r_r)) $
```
        f.verts = base_smpl.v_shaped_personal[f.v_ids]
        f.dist = distance_function(f.rays_u, f.verts)
```
根据w_idx获得对应的confidence score，即$w_l$
```
        w = f.face_landmark[:,-1][w_idx].reshape(-1,1) # confidence of landmark
```
这里的GMOf函数即 Geman-McClure robust cost function，对应$\rho$ 
```
        x = GMOf(f.dist, sigma)
```
将$\rho$ 与 $w_l$相乘后返回，乘积即$E_{face}$
```
        fina = x*w
         
        return fina
```

### (5). step2_consencus.py ###
1.main函数中增加了参数face_file, 为预先处理得到的face_landmark.hdf5文件

```python
    def main(pose_file, masks_file, face_file, camera_file, ...):

        # load data
        ...
```
从hdf5中读取face_landmark数据
```python
        # load face_landmark
        # @face_file : file name of face landmarks face_landmarks.hdf5
        face_data = h5py.File(face_file, 'r')
        face_landmark = face_data["face_landmark"][first_frame:last_frame]
    
        # init
        ...
    
        for i in indices_consensus:
            log.info('Set up frame {}...'.format(i))
    
            mask = ...
            pose_i =. ..
            trans_i =...
```
得到这一帧的landmark数据，进行setup
```python
            #paper 2
            face_i = np.array(face_landmark[i], dtype=np.float32)
            frames.append(setup_frame_rays_paper2(base_smpl, camera, camera_t, camera_rt, pose_i, trans_i, mask, face_i))
调用fit_consensus进行模型优化

        log.info('Set up complete.')
        log.info('Begin consensus fit...')
        fit_consensus(frames, base_smpl, camera, frustum, model_data, nohands, icp_count, naked, display)
        
        # save data
        ...
```
     
     
2.在fit_consensus中加入$E_{face}$能量项

        def fit_consensus(...):
          ...
获取面部的vertex

        face_ids = get_face_vertex_ids()
循环优化
```python
        for step, ...:
            log.info('# Step {}'.format(step))
```
这里的各项对应论文中的$E_{regm}$
```python
            ...
            
            # 其他能量项
            E = {
                'laplace': (sp_dot(L, base_smpl.v_shaped_personal) - delta) * w_laplace,
                'model': (base_smpl.v_shaped_personal - model_template) * w_model,
                'symmetry': (base_smpl.v_personal + np.array([1, -1, -1])
                             * base_smpl.v_personal[model_data['vert_sym_idxs']]) * w_symmetry,
           }
```
为每一帧增加能量项$E_{face}$
```python
            log.info('## Matching rays with contours')
            for current, f in enumerate(tqdm(frames)):
                E['silh_{}'.format(current)] = ray_objective(f, sigma, base_smpl, camera, vis_rn_b, vis_rn_m)            
                #paper 2
                E['face_{}'.format(current)] = ray_face(f, sigma, base_smpl, camera, face_ids) 
```
进行优化
```python
        log.info('## Run optimization')
        ch.minimize(
            E,
            [base_smpl.v_personal, model_template.betas],
            ...)
```

----------
## 优化效果展示 ##
左边为优化后的模型，右边为之前的consensus模型    
![female][1]    

![male][2]  

以上分别来自数据集中的female-7-plaza和male-9-plaza 可以看到有一些细微的优化，但是不明显  
我认为纹理图像对模型仿真度的影响最为关键，面部的mesh的优化需要配合更细致的纹理图像才能体现出最佳效果，目前的纹理图像太过于模糊粗糙


----------


  [1]: http://m.qpic.cn/psb?/V13Ti98m05LW5b/rogmPiyHNRYRKnyKsQUGnDBXCwwcUgPmj6S861eXnOA!/b/dFMBAAAAAAAA&bo=jAOGAgAAAAADNxk!&rf=viewer_4
  [2]: http://m.qpic.cn/psb?/V13Ti98m05LW5b/SdP2uMWzwojfxb63xXjzM41mVnJXUbyaudxOlYN14Rw!/b/dL4AAAAAAAAA&bo=4QKIAgAAAAADN3s!&rf=viewer_4
  
