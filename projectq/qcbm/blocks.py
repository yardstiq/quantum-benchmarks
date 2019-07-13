'''quantum circuit building blocks.'''
import numpy as np
from functools import reduce
try:
    from projectq.ops import *
except:
    print('warning: fail to import projectq')

from . import qclibs

class CircuitBlock(object):
    '''
    the building block of a circuit. This is an abstract class.
    '''
    def __init__(self, num_bit):
        self.num_bit = num_bit

    def __call__(self, qureg, theta_list):
        '''
        build a quantum circuit.

        Args:
            theta_list (1darray<float>, len=3*num*bit*(depth+1)): parameters in this quantum circuit, here, depth equals to the number of entanglement operations.

        Return:
            remaining theta_list
        '''
        pass

    @property
    def num_param(self):
        '''
        number of parameters it consume.
        '''
        pass

    def tocsr(self, theta_list):
        '''
        build this block into a sequence of csr_matrices.

        Args:
            theta_list (1darray): parameters,

        Returns:
            list: a list of csr_matrices, apply them on a vector to perform operation.
        '''
        pass

class BlockQueue(list):
    '''
    BlockQueue is a sequence of CircuitBlock instances.
    '''
    @property
    def num_bit(self):
        return self[0].num_bit

    @property
    def num_param(self):
        return sum([b.num_param for b in self])

    def __call__(self, qureg, theta_list):
        for block in self:
            theta_i, theta_list = np.split(theta_list, [block.num_param])
            block(qureg, theta_i)
        np.testing.assert_(len(theta_list)==0)

    def __str__(self):
        return '\n'.join([str(b) for b in self])


class CleverBlockQueue(BlockQueue):
    '''
    Clever Block Queue that keep track of theta_list changing history, for fast update.
    '''
    def __init__(self, *args):
        list.__init__(self, *args)
        self.theta_last = None
        self.memo = None

    def __call__(self, qureg, theta_list):
        if not isinstance(qureg, np.ndarray):
            return super(CleverBlockQueue, self).__call__(qureg, theta_list)
        # cache? if theta_list change <= 1 parameters, then don't touch memory.
        remember = self.theta_last is None or (abs(self.theta_last-theta_list)>1e-12).sum() > 1

        mats = []
        theta_last = self.theta_last
        if remember:
            self.theta_last = theta_list.copy()

        qureg_ = qureg
        for iblock, block in enumerate(self):
            # generate or use a block matrix
            num_param = block.num_param
            theta_i, theta_list = np.split(theta_list, [num_param])
            if theta_last is not None:
                theta_o, theta_last = np.split(theta_last, [num_param])
            if self.memo is not None and (num_param==0 or np.abs(theta_i-theta_o).max()<1e-12):
                # use data cached in memory
                mat = self.memo[iblock]
            else:
                if self.memo is not None and not remember:
                    # update the changed gate, but not touching memory.
                    mat = _rot_tocsr_update1(block, self.memo[iblock], theta_o, theta_i)
                else:
                    # regenerate one
                    mat = block.tocsr(theta_i)
            for mat_i in mat:
                qureg_ = mat_i.dot(qureg_)
            mats.append(mat)

        if remember:
            # cache data
            self.memo = mats
        # update register
        qureg[...] = qureg_
        np.testing.assert_(len(theta_list)==0)


class ArbituaryRotation(CircuitBlock):
    def __init__(self, num_bit):
        super(ArbituaryRotation, self).__init__(num_bit)
        self.mask = np.array([True] * (3*num_bit), dtype='bool')

    def __call__(self, qureg, theta_list):
        gates = [Rz, Rx, Rz]
        theta_list_ = np.zeros(self.num_bit*3)
        theta_list_[self.mask] = theta_list
        for i, (theta, mask) in enumerate(zip(theta_list_, self.mask)):
            ibit, igate = i//3, i%3
            if mask:
                gate = gates[igate](theta)
                gate | qureg[ibit]

    def __str__(self):
        return 'Rotate[%d]'%(self.num_param)

    @property
    def num_param(self):
        return self.mask.sum()

    def tocsr(self, theta_list):
        '''transform this block to csr_matrix.'''
        theta_list_ = np.zeros(3*self.num_bit)
        theta_list_[self.mask] = theta_list
        rots = [qclibs.rot(*ths) for ths in theta_list_.reshape([self.num_bit,3])]
        res = [qclibs._([rot], [i], self.num_bit) for i,rot in enumerate(rots)]
        return res

class CNOTEntangler(CircuitBlock):
    def __init__(self, num_bit, pairs):
        super(CNOTEntangler, self).__init__(num_bit)
        self.pairs = pairs

    def __str__(self):
        pair_str = ','.join(['%d-%d'%(i,j) for i,j in self.pairs])
        return 'CNOT(%s)'%(pair_str)

    def __call__(self, qureg, *args, **kwargs):
        for pair in self.pairs:
            CNOT | (qureg[pair[0]], qureg[pair[1]])

    @property
    def num_param(self):
        return 0

    def tocsr(self, theta_list):
        '''transform this block to csr_matrix.'''
        i, j = self.pairs[0]
        res = qclibs.CNOT(i, j, self.num_bit)
        for i, j in self.pairs[1:]:
            res = qclibs.CNOT(i,j,self.num_bit).dot(res)
        res.eliminate_zeros()
        return [res]


def _rot_tocsr_update1(rot, old, theta_old, theta_new):
    '''
    rotation layer csr_matrix update method.
    
    Args:
        rot (ArbituaryRotation): rotatio layer.
        old (csr_matrix): old matrices.
        theta_old (1darray): old parameters.
        theta_new (1darray): new parameters.

    Returns:
        csr_matrix: new rotation matrices after the theta changed.
    '''
    idiff_param = np.where(abs(theta_old-theta_new)>1e-12)[0].item()
    idiff = np.where(rot.mask)[0][idiff_param]

    # get rotation parameters
    isite = idiff//3
    theta_list_ = np.zeros(3*rot.num_bit)
    theta_list_[rot.mask] = theta_new

    new = old[:]
    new[isite] = qclibs._(qclibs.rot(*theta_list_[isite*3:isite*3+3]), isite, rot.num_bit)
    return new

def get_demo_circuit(num_bit, depth, pairs):
    blocks = []
    # build circuit
    for idepth in range(depth+1):
        blocks.append(ArbituaryRotation(num_bit))
        if idepth!=depth:
            blocks.append(CNOTEntangler(num_bit, pairs))

    # set leading and trailing Rz to disabled
    blocks[0].mask[::3] = False
    blocks[-1].mask[2::3] = False
    return CleverBlockQueue(blocks)
