# 이파일은 참고문헌 PYTHON PROGRAMMING IN CONTEXT 235쪽을 참고한 코드입니다.
# replit 과 같은 클라우드 개발 환경에서는 matplotlib으로 사용 안됨. (방법 찾는중)
# pycharm 또는 idle, jupyter-notebook 에서는 됨.

import random
import math

import matplotlib.pyplot as plt
from time import sleep

# plot Scatter (coding: CSY, BDS)
# dataSet의 타입dict, Clusters타입은 2차원 리스트
def plotScatter(dataSet, Clusters, centroids):
    colors = ['red', 'pink', 'green', 'blue']
    markers = ['o', 'x', 'x', 'x']

    clusterNum = 0
    for students in Clusters:  # student is list
        x = []
        y = []
        for student in students:
            x.append(dataSet[student][0])
            y.append(dataSet[student][1])

        plt.scatter(x, y, color=colors[clusterNum],
                    marker=markers[clusterNum],
                    label='exam')

        plt.scatter(centroids[clusterNum][0],centroids[clusterNum][1], color=colors[clusterNum],
                    marker='v',
                    label='exam')

        clusterNum = clusterNum + 1



    plt.grid()
    plt.show()


def euclidD(point1, point2):
    total = 0
    for index in range(len(point1)):
        diff = (point1[index] - point2[index]) ** 2
        total = total + diff

    euclidDistance = math.sqrt(total)
    return euclidDistance


def readFile(filename):
    with open(filename, "r") as dataFile:
        dataDict = {}

        key = 0
        aLine = dataFile.readline()
        while aLine != "":
            key = key + 1

            # 학생별 데이터가 1개인 경우
            # score = int(aLine)
            # dataDict[key] = [score]

            # 학생별 데이터가 2보다 크거나 같은 경우
            scores = aLine.split()
            print(scores)
            scores_int = [int(score) for score in scores]
            dataDict[key] = scores_int

            aLine = dataFile.readline()

    return dataDict


def createCentroids(k, dataDict):
    centroids = []
    centroidCount = 0
    centroidKeys = []

    # 1에서 dataDict 의 수만큼, 즉 1번학생에서 n번 학생중에서
    # 임의로(무작위) 초기 중심점 centroids 을 만든다.
    while centroidCount < k:
        rKey = random.randint(1, len(dataDict))
        if rKey not in centroidKeys:  # 이미 존재하는 학번이 아니라면 중심중 추가
            centroids.append(dataDict[rKey])
            centroidKeys.append(rKey)
            centroidCount = centroidCount + 1

    return centroids


def createClusters(k, centroids, dataDict, repeats):
    for aPass in range(repeats):
        print("****PASS", aPass + 1, "****")
        clusters = []  # 텅빈 리스트 정의
        for i in range(k):  # 리스트터안에 텅빈 리스트 만들기
            clusters.append([])  # 리스트에 텅빈 리스트 추가

        # --------각 학생을 가장 가까운 중심점의 clusters에 넣기------------------------------#
        # aKey는 학생번호임. 모든 학생데이터에 대해서 가장 가까운 무게중심점을 찾고 그 중심점에 포함시키기
        for aKey in dataDict:  # 하나의 데이터(키가 aKey인 딕트)가 모든 무게중심과의 거리를 모두 산출
            distances = []  # 거리값 저장용 리스트 생성
            for clusterIndex in range(k):  # k 개의 무게중심(centroid)점과 거리계산을 위해서 반복
                dToC = euclidD(dataDict[aKey], centroids[clusterIndex])  # 거리 계산
                distances.append(dToC)  # 계산된 값을 리스트에 추가

            # aKey 에 데이터가 무게중심(클러스터)과 가장 가까운지 판별하고 aKey(학생번호) 를 클러스터에
            minDist = min(distances)  # distances 리스트에서 최소값을 찾기
            index = distances.index(minDist)  # 최소데이터의 인덱스 찾기
            clusters[index].append(aKey)  # 인덱스가 가리키는 클러스터에 학생번호 추가
        # ---------------------------------------------------------------------------#

        # --------index번째 clusters에 속한 학생의 평가정보 기반으로 다시 중심점 구하기------------#
        # 데이터 딕트(학번: 평가정보)의 value(평가정보)의 차원(길이)을 구한다.
        dimensions = len(dataDict[1])
        # k 개의 클러스터 만큼 반복
        for clusterIndex in range(k):
            # sums 다차원 이며 예를 들면, 클러스터 집합에 속한 학생들의 시험점수의 합계, 과제점수의 합계임
            sums = [0] * dimensions  # 데이터 차원 만큼 0을 채운 sum 리스트 만들기

            # clusterIndex번째 클러스터에서 학번을 가져와 aKey에 저장하고,
            for aKey in clusters[clusterIndex]:
                # dataPoints는 한 학생에 대한 리스트 정보이며 예를 들면, 1차원일 경우는 시험점수만
                # 2차원 일경우는 과목별 시험점수 또는 시험점수, 과제기여도라 할 수 있음
                dataPoints = dataDict[aKey]  # 학생 점수를 읽어서 dataPoints 에 저장
                # dataPoints 내에 존재하는 값을 누적합(accumulation) 한다.
                for ind in range(len(dataPoints)):  # 데이터 번호를 ind 변수에 저장한다.
                    # 데이터 번호(ind) 번째 데이터를 sums의 ind번째 데이터에 누적합해서 저장한다.
                    sums[ind] = sums[ind] + dataPoints[ind]  # 누적합 계산

            for ind in range(len(sums)):  # 합계 리스트의 인덱스 번호를 ind 변수에 저장한다.
                # clusters 클러스터에서 clusterIndex번째에 리스트에 존재하는 학생수를 구한다.
                # clusterLen 는  clusters 리스트의 clusterIndex 번째에 있는 리스트 데이터의 원소 수
                clusterLen = len(clusters[clusterIndex])
                if clusterLen != 0:  # 학생수가 0이 아니라면
                    sums[ind] = sums[ind] / clusterLen  # 각 데이터 항목별 평균을 산출한다.
            centroids[clusterIndex] = sums  # 산출된 평균값을 새로운 중심점값으로 바꾼다.
        # ----------------------------------------------------------------------------#

        # --------데이터 표시 --------------------------#
        # clusters 리스트에서 원소하나를 빼서 c에 저장함.
        for c in clusters:
            print("CLUSTER")
            # c 에 존재하는 학생번호를 가져와 프린트 하기
            for key in c:
                print(dataDict[key], end=" ")
            print()
        # --------------------------------------------#
        
        #그래프 그리기 
        keysList = list(dataDict.keys())
        anyKey = keysList[0]
        if len(dataDict[anyKey]) >= 2: #데이터 차원이 2보다 큰지 확인후 2차원 그래프 그리기 
           plotScatter(dataDict, clusters, centroids)
           
        sleep(2) #2초 기다리기

    return clusters, centroids


def clusterAnalysis(dataFile):
    examDict = readFile(dataFile)
    print('examDict =', examDict)
    examCentroids = createCentroids(4, examDict)
    examClusters, examCentroids = createClusters(4, examCentroids, examDict, 5)

    #keysList = list(examDict.keys())
    #anyKey = keysList[0]
    #if len(examDict[anyKey]) >= 2: #데이터 차원이 2보다 큰지 확인후 2차원 그래프 그리기 
    #    plotScatter(examDict, examClusters, examCentroids)


clusterAnalysis("exam.txt")
