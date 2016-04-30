from config import settings
from MusicReco.Manager import Manager
from MusicReco.models.db import Audio, Plugin
import MusicReco.models.db
from utils import load_collection

def main():
    # import settings
    tags = settings['tags']
    plugins = settings['plugins']
    train_dir = settings['training_dataset']
    test_size = float(settings['test_size'])

    model = MusicReco.models.db
    manager = Manager(model)

    # initialize_storage
    manager.initialize_storage()
    
    # load collection
    manager.load_collection(tags, train_dir, test_size)
    manager.load_plugins(plugins)

    # Create feature vector of songs
    manager.use_plugin(plugin='GMM')
    #manager.init_vectors(limit = 10)
    #manager.init_vectors()

    # learning algorithms
    manager.train()

    psamples, nsamples =  manager.test()

    manager.accuracy_score(psamples, nsamples)

if __name__ == '__main__':
    main();
