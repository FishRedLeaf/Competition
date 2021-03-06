import math
import random
import copy
import numpy as np

class Matrix:

    def __init__(self, row, col, fill=0.0):
        self.shape = (row, col)
        self.row = row
        self.col = col
        self.list = [[fill] * col for i in range(row)]

    def __add__(self, N):
        M = Matrix(self.row, self.col)
        for r in range(self.row):
            for c in range(self.col):
                M[r, c] = self[r, c] + N[r, c]
        return M

    def __sub__(self, N):
        M = Matrix(self.row, self.col)
        for r in range(self.row):
            for c in range(self.col):
                M[r, c] = self[r, c] - N[r, c]
        return M

    def __mul__(self, N):
        if isinstance(N, int) or isinstance(N, float):
            M = Matrix(self.row, self.col)
            for r in range(1, self.row + 1):
                for c in range(1, self.col + 1):
                    M[r, c] = self[r, c] * N
        else:
            M = Matrix(self.row, N.col)
            for r in range(1, self.row + 1):
                for c in range(1, N.col + 1):
                    tmp = 0
                    for k in range(1, self.col + 1):
                        tmp += self[r, k] * N[k, c]
                    M[r, c] = tmp
        return M

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.list[index - 1]
        if isinstance(index, tuple):
            return self.list[index[0] - 1][index[1] - 1]

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self.list[index - 1] = copy.deepcopy(value)
        if isinstance(index, tuple):
            self.list[index[0] - 1][index[1] - 1] = value

    def inv(self):
        M = Matrix(self.row, self.col * 2)
        I = self.identity()

        for r in range(1, M.row + 1):
            temp = self[r]
            temp.extend(I[r])
            M[r] = copy.deepcopy(temp)

        for r in range(1, M.row + 1):
            if M[r, r] == 0:
                for rr in range(r + 1, M.row + 1):
                    if M[rr, r] != 0:
                        M[r], M[rr] = M[rr], M[r]
                    break

            tmp = M[r, r]
            for c in range(r, M.col + 1):
                M[r, c] /= tmp

            for rr in range(1, M.row + 1):
                tmp = M[rr, r]
                for c in range(r, M.col + 1):
                    if rr == r:
                        continue
                    M[rr, c] -= tmp * M[r, c]

        N = Matrix(self.row, self.col)
        for r in range(1, self.row + 1):
            N[r] = M[r][self.row:]

        return N

    def transpose(self):
        M = Matrix(self.col, self.row)
        for r in range(self.col):
            for c in range(self.row):
                M[r, c] = self[c, r]
        return M

    def cofactor(self, row, col):
        M = Matrix(self.col - 1, self.row - 1)
        for r in range(self.row):
            if r == row:
                continue
            for c in range(self.col):
                if c == col:
                    continue
                rr = r - 1 if r > row else r
                cc = c - 1 if c > col else c
                M[rr, cc] = self[r, c]
        return M

    def det(self):
        if self.shape == (2, 2):
            return self[1, 1] * self[2, 2] - self[1, 2] * self[2, 1]
        else:
            sum = 0.0
            for c in range(self.col + 1):
                sum += (-1) ** (c + 1) * self[1, c] * self.cofactor(1, c).det()
            return sum

    def identity(self):
        M = Matrix(self.col, self.row)
        for r in range(self.row):
            for c in range(self.col):
                M[r, c] = 1.0 if r == c else 0.0
        return M

CPUTYPE = [0, 1, 1, 1, 2, 2, 2, 4, 4, 4, 8, 8, 8, 16, 16, 16, 32, 32, 32]
MEMTYPE = [0, 1, 2, 4, 2, 4, 8, 4, 8, 16, 8, 16, 32, 16, 32, 64, 32, 64, 128]
DAYNUM2 = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DAYNUM1 = [0, 31, 27, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
YEARS = [0, 365, 365, 365, 365, 366, 365, 365, 365, 366, 365, 365, 365, 366, 365, 365, 365, 366, 365, 365, 365, 366]

def cal(year, month, day):
    """
    函数说明：
        计算日期
    :param year: 输入年份
    :param month: 输入月份
    :param day: 输入天数
    :return: 处理好的日期
    """
    RUNYEAR = 0
    if int(year) % 4 == 0:
        RUNYEAR = 1
    if RUNYEAR == 0:
        datetmp = 0
        for i in range(1, (int)(month)):
            datetmp += DAYNUM1[i]
        datetmp += (int)(day)
    if RUNYEAR == 1:
        datetmp = 0
        for i in range(1, (int)(month)):
            datetmp += DAYNUM2[i]
        datetmp += (int)(day)
    for i in range(1, (int)(year) - 2000 + 1):
        datetmp += (int)(YEARS[i])
    return datetmp

def meanShift(maxDate, data, typeList, predictTime, breakTime):
    """
    函数说明：
        使用滑动平均来对数据进行预测
    :param maxDate: 训练数据的最大日期
    :param data: 训练数据
    :param typeList:flavor类型列表
    :param predictTime:预测时间
    :param breakTime:中间的间隔的时间
    :return:预测数据
    """
    avg = []
    var = []
    for i in range(0, 19):
        avg.append(0)
        var.append(0)
    for i in range(1, 19):
        tmp = 0
        for j in range(1, maxDate + 1):
            tmp += data[j][i]
        avg[i] = (tmp) / (maxDate)

    for i in range(1, 19):
        tmp = 0
        for j in range(1, maxDate + 1):
            tmp += (data[j][i] - avg[i]) ** 2
        var[i] = float(tmp) / float(maxDate)

    for i in range(1, 19):
        for j in range(1, maxDate + 1):
            if data[j][i] > avg[i] * 6:
                data[j][i] = avg[i] * 3.8

    total = 0
    for i in range(1, predictTime + 1):
        for j in typeList:
            tot = 0
            for k in range(maxDate + i - 30, maxDate + i + 1):
                tot += data[k][j]
            tot = math.floor((tot / (30)))
            total += tot
            data[maxDate + i][j] = tot
            # data[maxDate + i][j] += 5.3
    # result.append(data)
    predictList = []
    totaltmp = 0  # total machines needed in all predictTime and all flavor
    for i in range(0, 19):
        predictList.append(0)
    for i in typeList:
        tmp = 0
        for j in range(1, predictTime + 1 - breakTime):
            tmp += data[maxDate + j + breakTime][i]
        tmp = (int)(tmp)
        totaltmp += tmp
        predictList[i] = [i, tmp]

    totaltmp = int(totaltmp)

    for i in range(0, len(predictList)):
        if predictList[i] == 0:
            predictList[i] = [i, 0]

    # TEST = [0, 53, 24, 3, 0, 2, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #      /    ! !  ! ~  +    ~   ~ + 2 ~    + ~  ~  !  ~
    for i in range(1, len(predictList)):
        if predictList[i][1] != 0:
            predictList[i][1] += TEST[i]
            totaltmp += TEST[i]
            
    return totaltmp, predictList

def calError(predictList,testdata, typeList):
    """
    函数说明：
        根据预测数据和真实数据，来计算误差
    :param predictList: 预测数据
    :param testdata: 用于测试的真实数据
    :param typeList: flavor类型列表
    :return: 算法的误差
    """
    error1 = 0
    error2 = 0
    error3 = 0

    for i in range(len(typeList)):
        error1 += float(predictList[i][1] - testdata[i])**2
        error2 += float(predictList[i][1])**2
        error3 += float(testdata[i])**2

    error1_1 = float(error1 / (len(typeList))) ** (1/2)
    error2_1 = float(error2 / (len(typeList))) ** (1 / 2)
    error3_1 = float(error3 / (len(typeList))) ** (1 / 2)

    error = 1 - error1_1/(error2_1 + error3_1)

    return error

def testData(test_lines, startDate, endDate, maxDate):
    """
    函数说明：
        生成测试数据，input要求的测试天数
    :param test_lines: 测试源文件
    :param startDate: 预测开始日期
    :param endDate: 预测结束日期
    :return: 测试的真实数据
    """
    cnt = 0
    dayList = []
    traindata = []
    for i in range(18):
        col = []
        for j in range(90):
            col.append(0)
        traindata.append(col)

    predictDay = [0] * (startDate - endDate)
    testdata = []

    for index, item in enumerate(test_lines):
        cnt += 1
        values = item.split("\t")
        values[1] = values[1].replace('flavor', '')
        flavor = int(values[1]) - 1

        if (int)(values[1]) >= 19:
            cnt -= 1
            continue
        create = values[2].split(" ")
        year = values[2][0:4]
        month = values[2][5:7]
        day = int(values[2][8:10]) - 1

        traindata[flavor][day] = traindata[flavor][day] + 1

    for flavor in range(18):
        temp = 0
        for day in range((startDate - maxDate), (endDate - maxDate + 1)):
            temp += traindata[flavor][day]
        testdata.append(temp)

    return testdata


def predict_vm(ecs_lines, input_lines, test_lines):
    # Do your work from here#
    m = Matrix(4, 4, fill=2.0)
    a = [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]
    for i in range(len(a)):
        m[i + 1] = a[i]
    m = m.inv()
    a = m.list
    result = []
    # result.append(a)
    cnt = 0
    flag = 0
    mode = 0  # mode 1 = optimize CPU, mode 2 = optimize MEM
    typeList = []
    trainData = []
    dayList = []
    data = []

    RUNYEAR = 0  # wheather a year is

    '''
    In order to process data across years, I let (2000,1,1) to be the 1st day, then calculate the date of 
    1st day of train data(let it be x), and then every date of train data = b - x + 1(b is the date transformed 
    according to (2000,1,1)
    '''
    if ecs_lines is None:
        print
        'ecs information is none'
        return result
    if input_lines is None:
        print
        'input file information is none'
        return result

    '''
    Read train data
    in this for loop our target is to get trainData
    which store data like this trainData = [[flavor1, date1, cnt1],[flacor2, date2, cnt2],...]
    '''
    trainData.append(0)

    for index, item in enumerate(ecs_lines):
        cnt += 1
        values = item.split("\t")
        values[1] = values[1].replace('flavor', '')
        if (int)(values[1]) >= 19:
            cnt -= 1
            continue
        create = values[2].split(" ")
        year = values[2][0:4]
        month = values[2][5:7]
        day = values[2][8:10]

        date = cal(year, month, day)

        if cnt == 1:
            startDateOrigin = date - 1
        date = date - startDateOrigin
        dayList.append(date)
        trainData.append([(int)(values[1]), date, cnt])  # trainData = [[type1, date1, cnt1],[]]

    maxDate = dayList[-1]  # Last day of train data, i.e. the day before 1st day to be predicted
    data.append(0)
    for i in range(1, maxDate + 60):
        data.append([i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(1, cnt + 1):
        date = trainData[i][1]
        flavor = trainData[i][0]
        data[date][flavor] += 1  # data = [[day1, type1num,..., type 15num],[day2,type1num,...],[]]

    for index, item in enumerate(input_lines):
        # print "index of input data"
        if index == 1:
            values = str(item)
            values = ' '.join(values.split())
            values = values.split(' ')
            cpuNum = values[1]
            memNum = values[2]
            diskNum = values[3]
        if index == 5:
            typeNum = item.split('\n')
        if item.split(' ')[0].find('flavor') != -1:
            tmp = item.split(' ')[0].replace('flavor', '')
            typeList.append((int)(tmp))
        # if item.find('CPU') != -1:
        #     mode = 1
        # if item.find('MEM') != -1:
        #     mode = 2
        # if item.split(' ')[0].find('-') != -1:
        #     flag += 1
        if item.split(' ')[0].find('201') != -1 and flag == 0:
            startDate = item.split(' ')[0]
            startYear = (int)(startDate[0:4])
            startMonth = (int)(startDate[5:7])
            startDay = (int)(startDate[8:10])
            flag += 1
        if item.split(' ')[0].find('201') != -1 and flag == 1:
            endDate = item.split(' ')[0]
            endYear = (int)(endDate[0:4])
            endMonth = (int)(endDate[5:7])
            endDay = (int)(endDate[8:10])

    flavorNum = []
    for i in range(0, 19):
        flavorNum.append(0)
    for i in range(1, 19):
        flavorNum[i] = [0 for j in range(0, maxDate + 1)]

    for i in range(1, 19):
        for j in range(1, maxDate + 1):
            flavorNum[i][j] = data[j][i]
    # result.append(flavorNum)

    typeList.sort()
    # result.append(typeList)

    currentTime = maxDate + 1
    startDate = cal(startYear, startMonth, startDay)

    endDate = cal(endYear, endMonth, endDay)
    startDate -= startDateOrigin
    endDate -= startDateOrigin
    predictTime = endDate - startDate
    breakTime = startDate - maxDate
    predictTime += breakTime


    # result.append(predictTime)
    # Prediction Process
    '''
    We store the predicted data in data[maxdate][]-data[maxdate+predictTime][]
    '''

    totaltmp, predictList = meanShift(maxDate, data, typeList, predictTime, breakTime)

    testdata = testData(test_lines, startDate, endDate, maxDate)
    print(predictList)
    print(testdata)

    error = calError(predictList,testdata, typeList)

    print(error)

    result.append((int)(totaltmp))  # predictList stores data like [0, [1,flavor1Num],[2,flavor2Num],...]
    for i in typeList:
        result.append('flavor' + str(predictList[i][0]) + ' ' + str((int)(predictList[i][1])))
    result[-1] += '\n'

    copy = predictList
    reTypeList = typeList
    reTypeList.reverse()

    bag = []
    for i in range(0, 20000):
        bag.append([(int)(cpuNum), (int)(memNum), (int)(diskNum)])

    curBag = 1  # currentBag
    usedBag = []
    for i in range(0, 20000):
        usedBag.append([i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    Q = []

    for i in reTypeList:
        cnt = 1
        while (cnt <= (int)(predictList[i][1])):
            Q.append(predictList[i][0]);
            cnt += 1
    # result.append(Q)
    minServer = len(Q)
    dice = []
    bestServer = []
    for i in range(minServer):
        dice.append(i)

    # minServer = -1
    curT = 100.0
    endT = 1
    decRate = 0.996
    count = 0
    while (curT > endT):
        newQ = Q
        random.shuffle(dice)
        tmp = newQ[dice[0]]
        for i in range(len(Q) - 1):
            newQ[dice[i]] = newQ[dice[i + 1]]
        newQ[dice[len(Q) - 1]] = tmp
        # newQ[dice[0]], newQ[dice[1]] = newQ[dice[1]], newQ[dice[0]]

        bag = []
        for i in range(0, 20000):
            bag.append([(int)(cpuNum), (int)(memNum), (int)(diskNum)])
        usedBag = []
        for i in range(0, 20000):
            usedBag.append([i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        curBag = 1

        for i in newQ:
            ratioMax = 1e9
            index = -1
            for j in range(1, curBag + 1):
                if bag[j][0] - CPUTYPE[(int)(i)] >= 0 and bag[j][1] - MEMTYPE[(int)(i)] >= 0:
                    bag[j][0] -= CPUTYPE[(int)(i)]
                    bag[j][1] -= MEMTYPE[(int)(i)]
                    # usedBag[j][(int)(i)] += 1
                    ratio = bag[j][0] + bag[j][1]
                    bag[j][0] += CPUTYPE[(int)(i)]
                    bag[j][1] += MEMTYPE[(int)(i)]
                    if ratio < ratioMax:
                        ratioMax = ratio
                        index = j
            # if j == curBag:
            # curBag += 1
            if index != -1:
                bag[index][0] -= CPUTYPE[(int)(i)]
                bag[index][1] -= MEMTYPE[(int)(i)]
                usedBag[index][(int)(i)] += 1
            else:
                curBag += 1
                bag[curBag][0] -= CPUTYPE[(int)(i)]
                bag[curBag][1] -= MEMTYPE[(int)(i)]
                usedBag[curBag][(int)(i)] += 1

        while (1):
            totTest = 0
            for i in range(1, 19):
                totTest += usedBag[curBag][i]
            if totTest != 0:
                break;
            else:
                curBag -= 1

        serverNum = 0
        totCPU = 0
        totMEM = 0
        for i in range(1, curBag + 1):
            totCPU += bag[i][0]
            totMEM += bag[i][1]
        usageCPU = float(totCPU) / ((int)(cpuNum) * curBag)
        usageMEM = float(totMEM) / ((int)(memNum) * curBag)

        if mode == 1:
            serverNum = (usageCPU + usageMEM) / 2
            # serverNum = (usageCPU + usageMEM)/2
        else:
            serverNum = (usageCPU + usageMEM) / 2
            # serverNum = (usageCPU + usageMEM)/2
        # if count == 0:
        # print serverNum
        # print curBag
        # count += 1
        if serverNum < minServer:
            print
            serverNum
            print
            curBag
            minServer = serverNum
            bestServer = usedBag
            # Q = newQ
        else:
            pass
            # if math.exp((minServer-serverNum)/curT) > random.random():
            #     print serverNum
            #     print curBag
            #     minServer = serverNum
            #     bestServer = usedBag
            # Q = newQ
        curT = decRate * curT

    usedBag = bestServer

    while (1):
        totTest = 0
        for i in range(1, 19):
            totTest += usedBag[curBag][i]
        if totTest != 0:
            break;
        else:
            curBag -= 1

    result.append('General ' + str(curBag))
    typeList.reverse()
    for i in range(1, curBag + 1):
        out = 'General-' + str(i) + ' '
        for j in typeList:
            if usedBag[i][j] != 0:
                out += 'flavor' + str(j) + ' ' + str(usedBag[i][j]) + ' '
        out = out.rstrip(' ')
        result.append(out)
    # result.append('This is a TEST!!!')
    return result