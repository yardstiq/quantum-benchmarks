import numpy as np
from scipy.optimize import minimize

def train(bm, theta_list, method, max_iter=1000, step_rate=0.1):
    '''
    train a Born Machine.
    
    Args:
        bm (QCBM): quantum circuit born machine training strategy.
        theta_list (1darray): initial parameters.
        method ('Adam'|'L-BFGS-B'):
            * L-BFGS-B: efficient, but not noise tolerant.
            * Adam: noise tolerant.
        max_iter (int): maximum allowed number of iterations.
        step_rate (float): learning rate for Adam optimizer.
        
    Returns:
        (float, 1darray): final loss and parameters.
    '''
    theta_list = np.array(theta_list)
    if method == 'Adam':
        from climin import Adam
        optimizer = Adam(wrt=theta_list, fprime=bm.gradient,step_rate=step_rate)
        for info in optimizer:
            step = info['n_iter']
            loss = bm.mmd_loss(theta_list)
            print('step = %d, loss = %s'%(step, loss))
            if step == max_iter:
                break
        return bm.mmd_loss(theta_list), theta_list
    else:
        res = minimize(bm.mmd_loss, x0=theta_list,
                       method=method, jac = bm.gradient, tol=1e-12,
                       options={'maxiter': max_iter, 'disp': 2, 'gtol':1e-12, 'ftol':0},
                       )
        return res.fun, res.x
