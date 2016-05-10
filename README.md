# Music classification System

This app classifies music files in different genres.

### How to run
Edit config.yaml for database name and run 
```
python -m scripts.main
```
This will run main.py under scripts directory. It will create database and populate them from music files. It will also split up the data files in test_size ratio specified in configuration settings and used it later on for accuracy score.

  Note: Database creation may take hours since it calculates all features written in plugins. To quickly bypass we have already computed features for our audio files and stored in sqlite database. Simply copy database to destination if you want to quickly work on machine learning algorithms.

To copy database run
```
cp simreco1_FINAL_ALL.db simreco.db
```
## Plugins
Audio feature extraction is done as a plugin architecture where each plugin extracts desired audio features. Multiple features can be added and removed from the project. To add a plugin, simply edit config.yaml and specify the plugin module path.
When main script is run then all features are computed and stored in sqlite database. it is then later used as features to train machine learning algorithms.

### How to write plugins
Simply add plugin in plugins directory. Plugin should contain atleast

```python
	def createVector(filename):
		return []
```
This function should take a filename, process it to extract audio featuers.

### How to test plugins
Edit test_plugin.py in tests folder and run
```
python -m tests.test_plugin
```

### MLlib
MLlib folder contains different machine learning algorithms which can be tested on audio features. Adding a machine learning algorithm is fairly easy where a file can be added with required signature in the folder and then changing main script to invoke your trainer

### How to write MLLib library
Simply add a python script in MLLib directory. MLLib should contain atleast
```python
def train(data):
end

def predict(filename):
end()
```

### How to test MLLib library
Simply change main.py in scripts folder and invoke your MLLib library by changing
```
manager.use_ml("<NEW_MODULE_NAME>")
```

### Report
Please look at report.pdf in reports folder for music genre classification accuracy.

