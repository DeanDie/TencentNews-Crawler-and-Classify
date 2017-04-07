#
import pymysql
import os
import shutil

map = ['news', 'ent', 'sports', 'finance', 'tech', 'games', 'auto', 'edu', 'house']
def database2File():
    db = pymysql.connect('localhost', 'root', 'yongheng', 'webspyder', charset='utf8')

    cursor = db.cursor()

    cursor.execute('select * from news where id > 160138')

    data = cursor.fetchall()

    count = 0
    for line in data:
        if map[line[1]] not in os.listdir('./data/trainingSet'):
            os.makedirs('./data/trainingSet/' + map[line[1]])
            print('Makedirs Succeed!')
        try:
            f = open('./data/trainingSet/' + map[line[1]] + '/' + str(line[0])  + '.txt', 'w')
            f.write(line[2])
            f.close()
        except:
            count += 1
            print('delete a row!')

    print(count)
    cursor.close()
    db.close()


def distiguish():
    for class_id in os.listdir('./data/trainingSet'):
        list = os.listdir('./data/trainingSet/' + class_id)
        if class_id not in os.listdir('./data/testSet'):
            os.makedirs('./data/testSet/' + class_id)
        for i in range(10000):
            shutil.move('./data/trainingSet/' + class_id + '/' + list[i], './data/testSet/' + class_id)
            print('Move OK')


def partition(string):
    import jieba.posseg as jp
    returnDict = {}
    content = jp.cut(string)
    for word, value in content:
        if value[0] == 'n':
            if returnDict.get(word):
                returnDict[word] += 1
            else:
                returnDict[word] = 1
    # print(returnDict)
    return returnDict


def tmp():
    textList =os.listdir('./data/trainingSet/finance')
    for fileName in textList:
        f = open('./data/trainingSet/finance/' + fileName, 'r', encoding='utf8', errors='ignore')
        parted = partition(f.read())
        f.close()

        f = open('./data/trainingParted/finance/' + fileName, 'w')
        for key, value in parted.items():
            f.write(key + ' ' + str(value) + '\n')
        f.close()



def load_data(dirName):
    dirs = os.listdir('./data/' + dirName)

    for class_index in range(6 if dirName == "trainingSet" else 0, len(dirs)):
        fileList = os.listdir('./data/testingSet/' + dirs[class_index])
        if dirName == 'trainingSet' and (not os.path.exists('./data/trainingParted/' + dirs[class_index])):
            os.makedirs('./data/' + 'trainingParted/' + dirs[class_index])
        if dirName == 'testingSet' and (not os.path.exists('./data/testingParted/' + dirs[class_index])):
            os.makedirs('./data/' + 'testingParted/' + dirs[class_index])
        try:
            for fileName in fileList:
                f = open('./data/' + dirName + '/' + dirs[class_index] + '/' + fileName, 'r')
                parted = partition(f.read().strip())
                f.close()

                f = open('./data/' + dirName[:-3] + 'Parted/' + dirs[class_index] + '/' + fileName, 'w')
                for key, value in parted.items():
                    f.write(key + ' ' + str(value) + '\n')
                f.close()
        except:
            for fileName in fileList:
                f = open('./data/' + dirName + '/' + dirs[class_index] + '/' + fileName, 'r', encoding='utf8', errors='ignore')
                parted = partition(f.read().strip())
                f.close()

                f = open('./data/' + dirName[:-3] + 'Parted/' + dirs[class_index] + '/' + fileName, 'w')
                for key, value in parted.items():
                    f.write(key + ' ' + str(value) + '\n')
                f.close()
        print('Category ' + dirs[class_index] + ' parted success!')


if __name__ == '__main__':
    # distiguish()
    path = ['trainingSet', 'testingSet']
    # load_data(path[0])
    # load_data(path[1])
    tmp()
