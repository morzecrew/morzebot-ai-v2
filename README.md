#### START DEVELOPMENT SERVER
1. Start uvicorn server with 
```commandline
    uvicorn server:app --reload
```
2. Start mongo database
```commandline
   sudo docker-compose up mongo 
```

#### Work with JamSpell
* Linux/MacOS Users:
1. Manually download swig3.0.12 via [sourceforce](http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz)
2. Extract the zipped download folder
3. Run the following via terminal:
```
    Downloads/swig-3.0.12/configure && make && make install
```
4. Run:
```python
    pip install jamspell
```
* Windows Users:
1. Manually download swig3 via sourceforge
2. Extract the zipped download folder to the local disk folder
3. Set the environment variable in MY COMPUTER. 
4. Create new variable in the "Path" line with the saved path to the unzipped folder
5. Reboot PC
6. Check in cmd swig version
