import numpy as np
from sklearn import gaussian_process
def f(x):
	return x * np.sin(x)
X = np.atleast_2d([1., 3., 5., 6., 7., 8.]).T
y = f(X).ravel()
x = np.atleast_2d(np.linspace(0, 10, 1000)).T
gp = gaussian_process.GaussianProcess(theta0=1e-2, thetaL=1e-4, thetaU=1e-1)
gp.fit(X, y)  

y_pred, sigma2_pred = gp.predict(x, eval_MSE=True)

print(y_pred)