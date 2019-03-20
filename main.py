from myTRIE import * # TRIE 데이터 구조 모듈
from fileIO import * # Dict, Grammar 파일 입출력용

if __name__ == '__main__':
    myGrammar = Grammar()
    myDict = Dict()

    myGrammar.load('data/grammar.txt') # 문법 불러오기
    myDict.load('data/dictionary.txt') # 사전 불러오기

    mytrie = Trie() # trie 객체 생성

    # 불러온 사전을 Trie 구조로 인덱싱한다.
    for i in range (myDict.numberOfContents) :
        #print(myDict.contents[i]) # 불러온 단어 출력
        mySlice = myDict.contents[i].split('\t') # 불러온 단어를 column 별로 자른다. :
        # 단어 | 품사  | 품사코드
        # 가  | 보조사 | JKG
        myWord = mySlice[0]
        myData = mySlice[1]
        mytrie.add(myWord, myData)

    # Trie 인덱싱 결과
    # print(mytrie)

    # Trie 검색 결과

    # key=input("분석 문장을 입력하세요.\n")
    key = '분노를 참는 것이 사람의 슬기이며 남의 허물을 덮어 주는 것이 자기의 영광이다'
    synWord = key.split(' ') # 문장을 어절 단위로 분리한다.
    lenSynWord = len(synWord) # 어절의 개수를 센다.
    print('문장의 어절은 {}개 입니다'.format(lenSynWord))

    for SynWordIdx in range (lenSynWord):
        lenSyllable = len(synWord[SynWordIdx]) # 음절의 개수를 센다.
        table = [] # parsing용 비어있는 table 정의

        # 이중 for 문을 이용해 비어있는 2차원의 table을 만든다.
        # 원래 tabular parsing을 위한 table은 삼각형 모양이지만
        # 구현의 편의상 정사각형 2차원 배열로 한다.
        for i in range(lenSyllable + 1):
            table.append([])
            for j in range(lenSyllable + 1):
                table[i].append([])


        for i in range (0, lenSyllable):
            for j in range (0,lenSyllable):
                currentWord = synWord[SynWordIdx]
                currentWord = currentWord[i:j+1]
                currentData = mytrie.getData(currentWord)
                if currentData != []:
                    if ' ' in currentData :
                        currentData = currentData.split(' ')
                        table[i][j+1].extend(currentData)
                    else :
                        table[i][j+1].append(currentData)
                else :
                    table[i][j+1].extend(currentData)

                # if currentData is not None :
                #     currentData = currentData.split(',') # 데이터가 여러개일 경우 인덱싱
                # table[i][j+1].extend(currentData)
                # else :
                #     pass#table[i][j+1].append()
                # else :
                #     table[i][j+1] = None
                #     # table.append('({},{}), 단어 : {}, 품사 : {}'.format(i,j+1,currentWord, currentData))
        #print(table)
        # 여기가 tabular parsing 완성! - 1차 passing


        grammar =[]
        for i in range (0,lenSyllable+1):
            for j in range (0, lenSyllable):

                if table[i][j] != []: # TODO 단어에 의미가 여러개 있을 경우도 생각해줘야 한다
                    grammar = table[i][j]
                    # if '' in grammar :
                    #     grammar = grammar.split(' ')

                    for numOfMean in range (len(grammar)) :
                        grammarLoop = grammar[numOfMean]
                        for k in range (j+1, lenSyllable+1):
                            if table[j][k] != []:
                                currentGrammar = table[j][k]
                                # currentGrammar = currentGrammar[0] # currentGrammar에도 뜻이 여러개 있을 수도 있다.
                                # if currentGrammar != [] :
                                #     currentGrammar = currentGrammar.split(' ')

                                for means in range (len(currentGrammar)):
                                    resultGrammar = ''
                                    currentGrammarSeg = currentGrammar[means]
                                    resultGrammar += resultGrammar + grammarLoop + ' '+currentGrammarSeg+' '
                                    resultGrammar = resultGrammar[:-1]
                                    table[i][k].extend([resultGrammar])

                # else :
                #     pass



        #print(table)
        printWord = synWord[SynWordIdx]
        # print(str(printWord[2:3])+str(table[2][3]))

        for i in range(0, lenSyllable) :
            for j in range(1, lenSyllable+1) :
                currentTable = table[i][j]

                for k in range (len(currentTable)):

                    if currentTable[k] in myGrammar.contents : # 사전에서 검색해서 있을 경우 결과 출력
                        print(printWord[i:j]+'/'+str(currentTable[k]))
                    # else : # 검색 결과가 없을 경우 결과를 테이블에서 지운다.
                        # table[i][j] = []



        #print(table)



    # TODO : 좌우 접속 정보 가지고 형태소 분석하기 !


    # item = mytrie.getData(key)
    # try :
    #     # 단어를 찾고 의미 중복이 있을 수 있으므로 ','로 분리한다
    #     item = item.split(',')
    #     print(item)
    #
    # except :
    #     # 찾는 단어가 없을 경우 예외 처리
    #     pass
