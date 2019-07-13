'''
Quantum Circuit Born Machine training framework.
'''

import numpy as np

from .contexts import ScipyContext, ProjectQContext

class QCBM(object):
    '''
    Quantum Circuit Born Machine,

    Args:
        circuit (BlockQueue): the circuit architechture.
        batch_size (int|None): introducing sampling error, None for no sampling error.
    '''
    def __init__(self, circuit, mmd, p_data, batch_size=None):
        self.circuit = circuit
        self.mmd = mmd
        self.p_data = p_data
        self.batch_size = batch_size
        self.context = ScipyContext
        self._loss_histo = []

    @property
    def depth(self):
        return (len(self.circuit)-1)//2

    def viz(self, theta_list=None):
        '''visualize this Born Machine'''
        if not self.context == ProjectQContext:
            raise AttributeError('Can not visualize, unless you use projectQ context.')
        if theta_list is None:
            theta_list = np.zeros(self.circuit.num_param)
        with self.context( self.circuit.num_bit, 'draw') as cc:
            self.circuit(cc.qureg, theta_list)

    def pdf(self, theta_list):
        '''get probability distribution function'''
        with self.context( self.circuit.num_bit, 'simulate') as cc:
            self.circuit(cc.qureg, theta_list)
        pl = np.abs(cc.wf)**2
        # introducing sampling error
        if self.batch_size is not None:
            pl = prob_from_sample(sample_from_prob(np.arange(len(pl)), pl, self.batch_size),
                    len(pl), False)
        return pl

    def mmd_loss(self, theta_list):
        '''get the loss'''
        # get probability distritbution of Born Machine
        self._prob = self.pdf(theta_list)
        # use wave function to get mmd loss
        loss = self.mmd(self._prob, self.p_data)
        self._loss_histo.append(loss)
        return loss

    def gradient(self, theta_list):
        '''
        cheat and get gradient.
        '''
        # for stability consern, we do not use the cached probability output.
        prob = self.pdf(theta_list)
        # for performance consern in real training, prob can be reused!
        #prob = self._prob

        grad = []
        for i in range(len(theta_list)):
            theta_list_ = theta_list.copy()
            # pi/2 phase
            theta_list_[i] += np.pi/2.
            prob_pos = self.pdf(theta_list_)
            # -pi/2 phase
            theta_list_[i] -= np.pi
            prob_neg = self.pdf(theta_list_)

            grad_pos = self.mmd.kernel_expect(prob, prob_pos) - self.mmd.kernel_expect(prob, prob_neg)
            grad_neg = self.mmd.kernel_expect(self.p_data, prob_pos) - self.mmd.kernel_expect(self.p_data, prob_neg)
            grad.append(grad_pos - grad_neg)

        return np.array(grad)

    def gradient_numerical(self, theta_list, delta=1e-2):
        '''
        numerical differenciation.
        '''
        grad = []
        for i in range(len(theta_list)):
            theta_list[i] += delta/2.
            loss_pos = self.mmd_loss(theta_list)
            theta_list[i] -= delta
            loss_neg = self.mmd_loss(theta_list)
            theta_list[i] += delta/2.

            grad_i = (loss_pos - loss_neg)/delta
            grad.append(grad_i)
        return np.array(grad)
