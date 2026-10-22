"""Centered 78-bin softmax mean model, fitted by proper cross entropy."""
import numpy as np
from scipy.special import logsumexp
from scipy.optimize import minimize


def objective(theta, x, q, penalty):
    """Mean daily cross entropy + lambda/2 sum(b_k**2); centered parameters."""
    ab = theta.reshape(2, 78); ab = ab-ab.mean(axis=1, keepdims=True)
    logits = ab[0]+x[:, None]*ab[1]
    logp = logits-logsumexp(logits, axis=1, keepdims=True)
    delta = (np.exp(logp)-q)/len(x)
    grad = np.array([delta.sum(axis=0), (delta*x[:, None]).sum(axis=0)+penalty*ab[1]])
    grad -= grad.mean(axis=1, keepdims=True)
    return float(-(q*logp).sum()/len(x)+penalty/2*(ab[1]**2).sum()), grad.ravel()


def fit(z, q, penalty=.001):
    """Training-only standardization; 154 identifiable free coefficients."""
    mean, sd = float(np.mean(z)), float(np.std(z)); x = (z-mean)/sd
    a = np.log(np.maximum(q.mean(axis=0), 1e-15)); a -= a.mean()
    result = minimize(objective, np.r_[a, np.zeros(78)], args=(x,q,penalty), jac=True,
                      method='L-BFGS-B', options=dict(maxiter=2000,ftol=1e-13,gtol=1e-9,maxls=40))
    ab = result.x.reshape(2,78); ab -= ab.mean(axis=1,keepdims=True)
    _, g = objective(ab.ravel(), x, q, penalty)
    if not result.success or np.max(abs(g)) > 2e-6:
        raise ValueError(f'M8_SOLVER_FAILED: {result.message}; gradient={np.max(abs(g))}')
    return dict(ab=ab.tolist(),mean=mean,sd=sd,penalty=penalty,objective=float(result.fun),
                success=bool(result.success),message=str(result.message),iterations=int(result.nit),
                gradient_max=float(np.max(abs(g))),identifiable_df=154,penalty_denominator='none; sum slope squares')


def predict(model, z):
    ab = np.asarray(model['ab']); logits = ab[0]+((np.asarray(z)-model['mean'])/model['sd'])[:,None]*ab[1]
    return np.exp(logits-logsumexp(logits,axis=1,keepdims=True))
