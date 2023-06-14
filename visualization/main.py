import h5py
import numpy as np

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ovis.ovis import *
from visualization.utils import get_closest_element_and_index


def main(filename):
    d = h5py.File(filename, 'r')
    for k, v in d.items():
        print(k, v.shape)

    cache = {}
    lidar_name_list = ['lidar1', 'lidar2', 'lidar3']
    
    seq_ts = d['seq_ts'][:]
    person_name_list = [e.decode() for e in d['person_name_list'][:]]
    print(person_name_list)
    pname = person_name_list[0]
    oclear()
    for seq_time in seq_ts[::2]:
        print(seq_time)
        hpc_list = []
        for obj_name in lidar_name_list:
            prefix = obj_name + '_' + pname
            if prefix + '_ts' not in cache:
                cache[prefix + '_ts'] = d[prefix + '_ts'][:]
            ts = cache[prefix + '_ts']
            ele, frame_i = get_closest_element_and_index(ts, seq_time)

            if np.abs(ele - seq_time) < (1 / 20) / 2:
                if prefix + '_pc_len' not in cache:
                    cache[prefix + '_pc_lr'] = np.hstack((np.zeros((1, ), dtype='int32'), np.cumsum(d[prefix + '_pc_len'][:])))
                obj_lr = cache[prefix + '_pc_lr'][frame_i:frame_i+2]
                hpc = d[prefix + '_pc'][obj_lr[0]:obj_lr[1]]
                hpc_list.append((obj_name, hpc))
            
        if len(hpc_list) > 0:
            hpc_center = np.concatenate([e[1] for e in hpc_list], axis=0).mean(axis=0)
            for obj_name, hpc in hpc_list:
                hpc = hpc - hpc_center
                if len(hpc) > 1:
                    opc(obj_name, hpc, 0.01 + 0.3 * lidar_name_list.index(obj_name))
                else:
                    opc(obj_name, np.array([[0, 0, 0], [0, 0, 0]]))
        
        if pname == person_name_list[0]:
            if 'imu_ts' not in cache:
                cache['imu_ts'] = d['imu_ts'][:]
                imu_ts = cache['imu_ts']
            mocap_i = get_closest_element_and_index(imu_ts, seq_time)[1]
            osmpl(d['imu_smpl_pose'][mocap_i], 'mesh', (0, -1, 0))

        owait()

    d.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str)
    args = parser.parse_args()
    main(args.file)