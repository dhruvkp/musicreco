# Music classification System

This app classifies music files in different genres.

### How to run
Edit config.yaml for database name and run 
```
python -m scripts.main
```
This will run main.py under scripts directory. It will create database and populate them from music files. It will also split up the data files in test_size ratio specified in configuration settings and used it later on for accuracy score.

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
