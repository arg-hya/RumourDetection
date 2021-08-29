import os

from Twitterutils import GraphVisualization

def readFile(dirPath, fileName):
    #dirPath = 'D:/Twitter/rumdetect2017/rumor_detection_acl2017/twitter15'
    #fileName = '80084555733803009'
    filePath = dirPath + '/tree/' + fileName + '.txt'

    print(filePath)
    # Driver code
    G = GraphVisualization()

    print('Loading file...')

    with open(filePath) as fp:
        #next(fp)
        for line in fp:
            #print(line)
            result = line.split("'")[1::2]
            #print(result)
            if result[0] == 'ROOT' :
                print('Root found...')
                parent = 0
            else :
                parent = int(result[0])
            child = int(result[3])
            #print("Parent = " , parent)
            #print("Child = " , child)
            G.addEdge(parent, child)

        #print("Graph building done...")
        G.save(dirPath, fileName)
        #print("Program Ended")

def makeGraphDB() :
    dirPath = 'D:/Twitter/rumdetect2017/rumor_detection_acl2017/twitter15'
    filePath = dirPath + '/' + 'label.txt'

    os.mkdir(dirPath + '/graph')

    with open(filePath) as fp:
        for line in fp :
            id = line.split(':')[1]
            #print (id)
            readFile(dirPath, id.strip('\n'))

