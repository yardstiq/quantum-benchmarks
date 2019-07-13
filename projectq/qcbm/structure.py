'''
Structures for entangle layers.
'''

import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

def chowliu_tree(pdata):
    '''
    generate chow-liu tree.

    Args:
        pdata (1darray): empirical distribution in dataset

    Returns:
        list: entangle pairs.
    '''
    X = mutual_information(pdata)
    Tcsr = -minimum_spanning_tree(-X)
    Tcoo = Tcsr.tocoo()
    pairs = list(zip(Tcoo.row, Tcoo.col))
    print('Chow-Liu tree pairs = %s'%pairs)
    return pairs

def random_tree(num_bit):
    '''
    generate random tree.
    '''
    X = np.random.random([num_bit, num_bit])
    Tcsr = -minimum_spanning_tree(-X)
    Tcoo = Tcsr.tocoo()
    pairs = list(zip(Tcoo.row, Tcoo.col))
    print('Random tree pairs = %s'%pairs)
    return pairs

def nearest_neighbor(geometry):
    '''
    generate nearest neighbor pairs.

    Args:
        geometry (tuple): square lattice size.
    '''
    num_bit = np.prod(geometry)
    if len(geometry) == 2:
        nrow, ncol = geometry
        res = []
        for ij in range(num_bit):
            i, j = ij // ncol, ij % ncol
            res.extend([(ij, i_ * ncol + j_)
                        for i_, j_ in [((i + 1) % nrow, j), (i, (j + 1) % ncol)]])
        return res
    elif len(geometry) == 1:
        res = []
        for inth in range(2):
            for i in range(inth, num_bit, 2):
                res = res + [(i, i_ % num_bit) for i_ in range(i + 1, i + 2)]
        return res
    else:
       raise NotImplementedError('')

def mutual_information(pdata):
    '''
    calculate mutual information I = \sum\limits_{x,y} p(x,y) log[p(x,y)/p(x)/p(y)]

    Args:
        pdata (1darray): empirical distribution in dataset

    Returns:
        2darray: mutual information table.
    '''
    sl = [0, 1]  # possible states
    d = len(sl)  # number of possible states
    num_bit = int(np.round(np.log(len(pdata))/np.log(2)))
    basis = np.arange(2**num_bit, dtype='uint32')

    pxy = np.zeros([num_bit, num_bit, d, d])
    px = np.zeros([num_bit, d])
    pdata2d = np.broadcast_to(pdata[:,None], (len(pdata), num_bit))
    pdata3d = np.broadcast_to(pdata[:,None,None], (len(pdata), num_bit, num_bit))
    offsets = np.arange(num_bit-1,-1,-1)

    for s_i in sl:
        mask_i = (basis[:,None]>>offsets)&1 == s_i
        px[:,s_i] = np.ma.array(pdata2d, mask=~mask_i).sum(axis=0)
        for s_j in sl:
            mask_j = (basis[:,None]>>offsets)&1 == s_j
            pxy[:,:,s_i,s_j] = np.ma.array(pdata3d, mask=~(mask_i[:,None,:]&mask_j[:,:,None])).sum(axis=0)

    # mutual information
    pratio = pxy/np.maximum(px[:,None,:,None]*px[None,:,None,:], 1e-15)
    for i in range(num_bit):
        pratio[i, i] = 1
    I = (pxy*np.log(pratio)).sum(axis=(2,3))
    return I


