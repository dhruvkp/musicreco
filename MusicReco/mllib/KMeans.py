from .base import Base

class KMeans(Base):

	def train(self, data=None):
		""" Training through KMeans """
		X = data['GMM']
		# It contains 1 X N mean vectors and N X N covariance matrix where N is
		# spectral features in MFCC.

		print(X[0].shape)
		# create clusters of these features
		

		pass

	def predict(self,file):
		""" GUESS the output of single file """
		# TODO: Unimplemented, Using random guess
		return super(KMeans, self).predict(file)