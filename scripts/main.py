from config import settings
from MusicReco.Manager import Manager
from MusicReco.models.db import Audio, Plugin
import MusicReco.models.db
from utils import load_collection

def main():
    # load collection
    model = MusicReco.models.db
    manager = Manager(model)

    # initialize_storage
    manager.initialize_storage()
    tags = ['blues' , 'classical' , 'country' , 'disco' , 'hiphop' , 'jazz',	'metal',  'pop',  'reggae' , 'rock']
    
    files = load_collection(tags)

    for path, file, tag in files:
        manager.add_file(path, file, tag)

    plugins = [ ('centroid', 'MusicReco.plugins.centroid'),
                ('fextract', 'MusicReco.plugins.centroid')]

    for name, plugin in plugins:
        manager.add_plugin(name, plugin)

    # Init vectors
    manager.init_vectors()

    # learning algorithms

if __name__ == '__main__':
    main();
