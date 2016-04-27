from MusicReco.models.db import *
#import MusicReco
def main():
	a = Audio.get()
	print(a)


if __name__ == '__main__':
	# Assuming database is loaded
	main()
