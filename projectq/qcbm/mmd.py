import numpy as np

class RBFMMD2(object):
    def __init__(self, sigma_list, num_bit, is_binary):
        self.sigma_list = sigma_list
        self.num_bit = num_bit
        self.is_binary = is_binary
        self.basis = np.arange(2**num_bit,dtype='int32')
        self.K = mix_rbf_kernel(self.basis, self.basis, self.sigma_list, is_binary)

    def __call__(self, px, py):
        '''
        Args:
            px (1darray, default=None): probability for data set x, used only when self.is_exact==True.
            py (1darray, default=None): same as px, but for data set y.

        Returns:
            float, loss.
        '''
        pxy = px-py
        return self.kernel_expect(pxy, pxy)

    def kernel_expect(self, px, py):
        res = px.dot(self.K.dot(py))
        return res

def mix_rbf_kernel(x, y, sigma_list, is_binary):
    if is_binary:
        dx2 = np.zeros([len(x)]*2, dtype='int64')
        num_bit = int(np.round(np.log(len(x))/np.log(2)))
        for i in range(num_bit):
            dx2 += (x[:,None]>>i)&1 != (y>>i)&1
    else:
        dx2 = (x[:, None] - y)**2
    return _mix_rbf_kernel_d(dx2, sigma_list)

def _mix_rbf_kernel_d(dx2, sigma_list):
    K = 0.0
    for sigma in sigma_list:
        gamma = 1.0 / (2 * sigma)
        K = K + np.exp(-gamma * dx2)
    return K
