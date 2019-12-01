import os
import hashlib

#Get paths of all files in the selected directory
def getFiles(dirName):
    listOfFiles = os.listdir(dirName)
    allFiles = list()

    for entry in listOfFiles:
        #Get full file paths
        fullPath = os.path.join(dirName, entry)
        #Check whether it's a file or a folder
        if os.path.isdir(fullPath):
            #If it's a folder, adding the files in it to the list by iterating
            allFiles = allFiles + getFiles(fullPath)
        else:
            #If it's a file, adding it to the files list
            allFiles.append(fullPath)

    return allFiles

#Get a list of all filenames in the selected directory
def getFileNames(dirName):
    listOfFileNames = os.listdir(dirName)
    allFileNames = list()

    for entry in listOfFileNames:
        #Get full file paths
        fullPath = os.path.join(dirName, entry)
        #Check whether it's a file or folder
        if os.path.isdir(fullPath):
            #If it's a folder, adding the files in it to the list by iterating
            allFileNames = allFileNames + getFileNames(fullPath)
        else:
            #If it's a file, adding it to the files list
            allFileNames.append(entry)
    
    return allFileNames

#Get a list of filesizes in the selected directory
def getFileSizes(dirName):
    listOfFileNames = os.listdir(dirName)
    allFileSizes = list()

    for entry in listOfFileNames:
        #Get full file paths
        fullPath = os.path.join(dirName, entry)
        #Check whether it's a file or folder
        if os.path.isdir(fullPath):
            #If it's a folder, adding the files in it to the list by iterating
            allFileSizes = allFileSizes + getFileSizes(fullPath)
        else:
            #If it's a file, calculating its size
            fileSize = os.path.getsize(fullPath)
            #...and adding it to the file sizess list
            allFileSizes.append(fileSize)

    return allFileSizes

#Get a list of Hashes of the files in the selected directory
def getFileHashes(dirName):
    listOfFileNames = os.listdir(dirName)
    allFileHashes = list()

    for entry in listOfFileNames:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFileHashes = allFileHashes + getFileHashes(fullPath)
        else:
            shaHash = hashlib.sha256()
            with open(fullPath,"rb") as f:
                #Read and update hash string value on blocks of 4K
                for byte_block in iter(lambda: f.read(4096),b""):
                    shaHash.update(byte_block)
                hashCode = shaHash.hexdigest()
            allFileHashes.append(hashCode)

    return allFileHashes

#Get an array of indexes of the files with the same size
def getSameSize(fileSizes):
    sameSize = list()
    for i in range(len(fileSizes)-1):
        for j in range(i+1, len(fileSizes)):
            if(fileSizes[i] == fileSizes[j]):
                n = 0
                for m in range(len(sameSize)):
                    if(j == sameSize[m]):
                        n = n + 1
                if(n == 0):
                    sameSize.append(j)
                k = 0
                for l in range(len(sameSize)):
                    if(i == sameSize[l]):
                        k = k + 1
                if(k == 0):
                    sameSize.append(i)

    return sameSize

#Get an array of indexes of the files with the same hash
def getsameHash(fileHashes):
    sameHash = list()
    for i in range(len(fileHashes)-1):
        for j in range(i+1, len(fileHashes)):
            if(fileHashes[i] == fileHashes[j]):
                n = 0
                for m in range(len(sameHash)):
                    if(j == sameHash[m]):
                        n = n + 1
                if(n == 0):
                    sameHash.append(j)
                k = 0
                for l in range(len(sameHash)):
                    if(i == sameHash[l]):
                        k = k + 1
                if(k == 0):
                    sameHash.append(i)

    return sameHash

#Delete Files 
def deleteFiles(filesToDelete, sameHashFiles, filePaths):
    deletionError = 0
    for i in range(len(filesToDelete)):
        try:
            os.remove(filePaths[sameHashFiles[filesToDelete[i]]])
        except OSError:
            deletionError += 1
        except SystemError:
            deletionError += 1
    
    if deletionError == 0:
        return True
    elif deletionError > 0:
        return False

#Check whether the entered directory is valid or not
def isDirValid(dirName):
    if os.path.isdir(dirName):
        return True
    else:
        return False

def getReadableFileSizes(size_in_bytes):
    SIZE_UNITS = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    float(size_in_bytes)
    size_in_bytes = round(size_in_bytes, 3)
    try:
        return f'{size_in_bytes} {SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

def duplicates(dirPath):
    filePaths = getFiles(dirPath)
    fileNames = getFileNames(dirPath)
    fileSizes = getFileSizes(dirPath)
    fileHashes = getFileHashes(dirPath)
    sameHashFiles = getsameHash(fileHashes)

    dupFiles = list()
    num = 0
    for entry in sameHashFiles:
        dup = {
            'id' : num,
            'FileName' : fileNames[entry],
            'FilePath' : filePaths[entry],
            'FileSize' : getReadableFileSizes(fileSizes[entry])
        }
        dupFiles.append(dup)
        num += 1

    return dupFiles