from .base import Base

class KMeans(Base):

	def train(self, data=None):
		""" Training through KMeans """
		pass

	def predict(self,file):
		""" GUESS the output of single file """
		# TODO: Unimplemented, Using random guess
		return super(KMeans, self).predict(file)