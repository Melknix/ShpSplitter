# ShpSplitter
Esri Shapefile file splitter

This simple script split a shapefile in n file and every file contains X (passed as param) number of feature except the last file.


## Usage
```bash
ShpSplit.py inputfile numberOfFeatureInFile
```

* Parameter inputfile is the path of the shp file
* Parameter numberOfFeatureInFile is an integer value that is the number of feature in every file (except the last)

The script will generate an out directory with all the shp file named orginalname_X.shp where X is the number of the file

Every execution generate a numbered out directory like out, out1, out2 and so on...