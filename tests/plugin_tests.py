from MusicReco.models.db import *
from MusicReco.plugins import fextract_plugin, centroid
import numpy as np
from scipy.stats import multivariate_normal, entropy

def kl_divergence(sigma1, sigma2, mu1, mu2):
    sigma2_inv = np.linalg.inv(sigma2)
    mean_diff = (mu1 - mu2)

    return np.log(np.linalg.det(sigma1)/np.linalg.det(sigma2)) 
    + np.trace(sigma2_inv.dot(sigma1)) - mu1.shape[0] 
    + mean_diff.T.dot(sigma2_inv).dot(mean_diff)

def KLsymmetric(sigma1, sigma2, mu1, mu2):
	#return np.abs(kl_divergence(sigma2, sigma1, mu2, mu1))
	return 0.5*(kl_divergence(sigma1, sigma2, mu1, mu2) + kl_divergence(sigma2, sigma1, mu2, mu1))

def main():
	a = Audio.get()
	a1 =Audio.get(Audio.id==4)
	
	b = Audio.select().join(Tag).where(Tag.genre=='disco').get()
	b1 = Audio.select().join(Tag).where(Tag.genre=='disco' and Audio.id==305).get()

	res1 = fextract_plugin.createVector(a.path)
	res11 = fextract_plugin.createVector(a1.path)

	res2 = fextract_plugin.createVector(b.path)
	res22 = fextract_plugin.createVector(b1.path)

	print(a.id, a1.id, b.id, b1.id)

	# first song
	mean1 = res1.mean(axis=1)
	covar1 = np.cov(res1, rowvar = 1)

	# second song
	mean2 = res11.mean(axis=1)
	covar2 = np.cov(res11, rowvar = 1)

	# third song
	mean3 = res2.mean(axis=1)
	covar3 = np.cov(res2, rowvar = 1)

	# fourth song
	mean4 = res22.mean(axis=1)
	covar4 = np.cov(res22, rowvar= 1)

	x = np.linspace(-100,10,1000)
	print(mean1, mean2, mean3, mean4)

	print(KLsymmetric(covar1, covar2, mean1, mean2))
	print(KLsymmetric(covar1, covar3, mean1.T, mean3.T))
	print(KLsymmetric(covar1, covar4, mean1, mean4))

	print("with 3 & 4")
	print(KLsymmetric(covar3, covar4, mean3, mean4))	

if __name__ == '__main__':
	# Assuming database is loaded
	main()