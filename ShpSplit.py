#!/usr/bin/python
import getopt
import numbers
import os
import sys

from osgeo import ogr


def main(argv):
    inputFile = ''
    featureNumber = 0
    try:
        opts, args = getopt.getopt(argv, "hi:n", ["i=", "nFeature="])
    except getopt.GetoptError:
        print('ShpSplit.py inputfile numberOfFeatureInFile')
        sys.exit(2)
    if len(args) != 2:
        print('ShpSplit.py inputfile numberOfFeatureInFile')
        sys.exit(2)
    else:
        fileExist = os.path.exists(args[0])
        isNumber = isinstance(int(args[1]), numbers.Number)
        if (not fileExist or not isNumber):
            print('ShpSplit.py inputfile numberOfFeatureInFile')
            sys.exit(2)
        inputFile = args[0]
        featureNumber = int(args[1])
        splitShp(inputFile, featureNumber)


def splitShp(inputFile, featurenNmber):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(inputFile, 0)
    layer = dataSource.GetLayer()
    featureCount = layer.GetFeatureCount()
    print("Fearute in layer: " + str(featureCount))
    # Split data
    i = 0;
    toCreate = list()
    tempList = list()
    for feature in layer:
        tempList.append(feature)
        i += 1
        if i == featurenNmber:
            toCreate.append(tempList)
            i = 0
            tempList = list()
    # Add last interaction
    toCreate.append(tempList)
    print("Will be created " + str(len(toCreate)) + " files")

    # Create directory output (always a new numbered output dir)
    dirName = createOutDir("out", 0)
    print("Output directory " + dirName)
    # Prepare data for file
    spatialReference = layer.GetSpatialRef()
    print("New file spatial reference: \n" + str(spatialReference))

    baseFileName = inputFile.split(sep=".")[0]
    layerDefinition = layer.GetLayerDefn()
    createShpFiles(dirName, baseFileName, toCreate, spatialReference, layerDefinition)


# Create shp files
def createShpFiles(outDir, baseFileName, dataFiles, srs, layerDefinition):
    print("Field definition \n")
    for i in range(layerDefinition.GetFieldCount()):
        fieldName = layerDefinition.GetFieldDefn(i).GetName()
        fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
        fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
        fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
        GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()
        print(fieldName + " - " + fieldType + " " + str(fieldWidth) + " " + str(GetPrecision))
    # start processing
    i = 0
    for data in dataFiles:
        outFileName = baseFileName + "_" + str(i) + ".shp"
        fullPaht = os.path.join(outDir, outFileName)
        print("Creating file " + fullPaht)
        # set up the shapefile driver
        driver = ogr.GetDriverByName("ESRI Shapefile")
        # create the data source
        data_source = driver.CreateDataSource(fullPaht)
        # create the layer
        layer = data_source.CreateLayer(fullPaht, srs, data[0].GetGeometryRef().GetGeometryType())
        # create layer definition
        for j in range(layerDefinition.GetFieldCount()):
            layer.CreateField(layerDefinition.GetFieldDefn(j))
        # add features
        for feature in data:
            layer.CreateFeature(feature)

        i += 1


# Create output dir recursively
def createOutDir(name, interaction):
    dirName = name
    if interaction != 0:
        dirName += str(interaction)
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        return dirName
    else:
        return createOutDir(name, interaction + 1)


if __name__ == "__main__":
    main(sys.argv[1:])
