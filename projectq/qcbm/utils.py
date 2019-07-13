import numpy as np
from sys import platform
import os

def unpacknbits(arr, nbit, axis=-1):
    '''unpack numbers to bits.'''
    nd = np.ndim(arr)
    if axis < 0:
        axis = nd + axis
    return (((arr & (1 << np.arange(nbit - 1, -1, -1)).reshape([-1] + [1] * (nd - axis - 1)))) > 0).astype('int8')


def packnbits(arr, axis=-1):
    '''pack bits to numbers.'''
    nd = np.ndim(arr)
    nbit = np.shape(arr)[axis]
    if axis < 0:
        axis = nd + axis
    return (arr * (1 << np.arange(nbit - 1, -1, -1)).reshape([-1] + [1] * (nd - axis - 1))).sum(axis=axis, keepdims=True).astype('int')


def sample_from_prob(x, pl, num_sample):
    '''
    sample x from probability.
    '''
    pl = 1. / pl.sum() * pl
    indices = np.arange(len(x))
    res = np.random.choice(indices, num_sample, p=pl)
    return np.array([x[r] for r in res])


def prob_from_sample(dataset, hndim, packbits):
    '''
    emperical probability from data.
    '''
    if packbits:
        dataset = packnbits(dataset).ravel()
    p_data = np.bincount(dataset, minlength=hndim)
    p_data = p_data / float(np.sum(p_data))
    return p_data

def openfile(filename):
    '''
    Open a file.

    Args:
        filename (str): the target file.

    Return:
        bool: succeed if True.
    '''
    if platform == "linux" or platform == "linux2":
        os.system('xdg-open %s' % filename)
    elif platform == "darwin":
        os.system('open %s' % filename)
    elif platform == "win32":
        os.startfile(filename)
    else:
        print('Can not open file, platform %s not handled!' % platform)
        return False
    return True


