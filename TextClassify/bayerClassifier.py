
import numpy
import os
import re
import math
from preTreated import partition


class BayerClassifer(object):
    def __init__(self, dataset):
        self.classDetail = [0] * 10
        self.totalWords = {}
        self.pre_likehood = []
        self.conditionnal_prob = []
        self.feature = set()
        self.dirs = []
        self.each_class_feature = [0] * 10
        self.class_count = [0] * 10
        self.trainingFile = []
        self.fileCount = 0


    def loadTrainingData(self):
        self.dirs = os.listdir('./data/trainingParted')

        for class_index in range(len(self.dirs)):
            fileList = os.listdir('./data/trainingParted/' + self.dirs[class_index])
            self.classDetail[class_index] = {}
            self.trainingFile.append([0,{}])
            for fileName in fileList:
                self.fileCount += 1
                self.trainingFile[class_index][0] += 1
                f = open('./data/trainingParted/' + self.dirs[class_index] + '/' + fileName, 'r')
                for line in f.readlines():
                    key, value = line.strip().split()
                    value = int(value)
                    if self.classDetail[class_index].get(key):
                        self.classDetail[class_index][key] += value
                    else:
                        self.classDetail[class_index][key] = value
                        if self.trainingFile[class_index][1].get(key):
                            self.trainingFile[class_index][1][key] += 1
                        else:
                            self.trainingFile[class_index][1][key] = 1

                    if self.totalWords.get(key):
                        self.totalWords[key] += 1
                    else:
                        self.totalWords[key] = 1
                f.close()
            print('Read category ' + self.dirs[class_index] + ' nurns success!')


    def del_StopWords(self):
        f = open('./data/stop_words.txt', 'r')
        stopWords = partition(f.read().strip())
        for category_id in range(len(self.dirs)):
            for word in stopWords.keys():
                if self.classDetail[category_id].get(word):
                    del self.classDetail[category_id][word]
                if self.totalWords.get(word):
                    del self.totalWords[word]
        f.close()
        print('Delete stop_words Succeed!')


    def getCHI(self):
        for index in range(len(self.dirs)):
            returnDict,self.each_class_feature[index] = {}, {}
            temp = dict(self.classDetail[index])
            for word, value in temp.items():
                if value < 350:
                    del self.classDetail[index][word]
                    continue
                A = self.trainingFile[index][1][word]
                B = 0
                for i in range(len(self.dirs)):
                    B += self.trainingFile[i][1][word] if self.trainingFile[i][1].get(word) else 0
                B = B - A
                C = self.trainingFile[index][0] - A
                D = self.fileCount - A - B - C
                returnDict[word] = pow(A * D - B * C, 2) / ((A +C) * (A + B) * (B + D) *(C + D))
            sortedWords = sorted(returnDict.items(), key=lambda item: item[1], reverse=True)
            self.each_class_feature[index] = {word for word, CHI in sortedWords[:550]}
            i,count = 550, 0
            wordList = list(self.feature & self.each_class_feature[index])
            while len(self.feature | self.each_class_feature[index]) - len(self.feature) < 200 and len(sortedWords) > i:
                if sortedWords[i][0] not in self.feature and sortedWords[i][1] and sortedWords[i][1] > 220:
                    self.each_class_feature[index] |= {sortedWords[i][0]}
                    self.each_class_feature[index].remove(wordList[count])
                    count += 1
                else:
                    del self.classDetail[index][sortedWords[i][0]]
                i += 1
            self.feature |= self.each_class_feature[index]
            print(len(self.feature))
            for word_index in range(i, len(sortedWords)):
                del self.classDetail[index][sortedWords[word_index][0]]
            self.class_count[index] = sum(self.classDetail[index].values())

        del_word = []
        for word, value in self.totalWords.items():
            if word not in self.feature:
                del_word.append(word)
        for word in del_word:
            del self.totalWords[word]
        self.feature = list(self.feature)

        f = open('./data/totalCount.txt', 'w')
        for feature in self.feature:
            f.write(feature + ' ')
        f.close()
        f = open('./data/totalFeature.txt', 'w')
        for word, value in self.totalWords.items():
            f.write(word + ' ' + str(value) + '\n')
        f.close()
        for className in self.dirs:
            f = open('./data/' + className + '.txt', 'w')
            for feature, value in self.classDetail[self.dirs.index(className)].items():
                f.write(feature + ' ' + str(value) + '\n')
            f.close()

            f = open('./data/' + className + 'Feature.txt', 'w')
            for word in list(self.each_class_feature[self.dirs.index(className)]):
                f.write(word + ' ')
            f.close()

        print('The length of feature: %d' % len(self.feature))
        print('Get CHI Completed!')



    def trainModel(self):
        # self.dirs = os.listdir('./data/trainingParted')
        print("Training Model...")

        totalNums = sum(self.totalWords.values())

        for category_index in range(len(self.dirs)):
            self.pre_likehood.append(self.trainingFile[category_index][0] / self.fileCount)

            self.conditionnal_prob.append([0.] * len(self.feature))
            for word, value in self.classDetail[category_index].items():
                self.conditionnal_prob[category_index][self.feature.index(word)] = \
                    self.classDetail[category_index][word] / self.class_count[category_index]


    def file2vector(self, path):
        returnMat = [0.] * len(self.totalWords)
        f = open(path, 'r')
        for line in f.readlines():
            word, frequent = line.strip().split()
            if word in self.feature:
                returnMat[self.feature.index(word)] = float(int(frequent))
        f.close()

        return returnMat


    def test(self):
        correct = 0.
        totalFile = 0

        file = os.path.split(__file__)[0]
        dirs = os.listdir('./data/testingParted/')

        print("Test Model...")
        for category in dirs:
            # if category != 'finance':
            #     continue
            path = './data/testingParted/' + category
            textList = os.listdir(path)
            real_value = self.dirs.index(category)
            for textName in textList:
                totalFile += 1
                vector = self.file2vector(path + '/' + textName)
                # score = vector * self.conditionnal_prob
                score = [0] * 10
                for class_index in range(len(self.dirs)):
                    score[class_index] = sum((map((lambda x, y: math.log(x * y + 1)), vector, self.conditionnal_prob[class_index])))
                    score[class_index] += math.log(self.pre_likehood[class_index])
                index = score.index(max(score))
                if real_value == index:
                    correct += 1

                if totalFile % 100 == 0:
                    print('The Predicted category of No.%d file is :%s, real category is %s' \
                          %(totalFile, self.dirs[index], self.dirs[real_value]), end='')
                    print('; temporary Accuracy is: %.2f%%' % ((correct / totalFile) * 100))

        print('###########################################################')
        print("Training file: %d, testing file: %d" % (self.fileCount, totalFile))
        print("This Model's accuracy is: %.2f%%" % ((correct / totalFile) * 100))

    def start(self):
        self.loadTrainingData()
        self.del_StopWords()
        self.getCHI()
        self.trainModel()
        self.test()

if __name__ == '__main__':
    bc = BayerClassifer('..')
    bc.start()