from myTRIE import * # TRIE 데이터 구조 모듈
from fileIO import * # Dict, Grammar 파일 입출력용
import numpy as np

if __name__ == '__main__':
    myGrammar = Grammar()
    myDict = Dict()

    myGrammar.load('data/grammar.txt') # 문법 불러오기
    myDict.load('data/dictionary.txt') # 사전 불러오기

    mytrie = Trie() # trie 객체 생성

    # ---------------------------------------- #
    # STEP 1 : 불러온 사전을 Trie 구조로 인덱싱한다. #
    # ---------------------------------------- #

    for i in range (myDict.numberOfContents) :
        mySlice = myDict.contents[i].split('\t')
        # 불러온 단어를 column 별로 자른다.
        # -------------------- #
        # 단어 | 품사  | 품사코드  #
        # 가  | 보조사 | JKG     #
        # -------------------- #
        myWord = mySlice[0]
        myData = mySlice[1]
        mytrie.add(myWord, myData)

    print(" TRIE 사전 구축을 완료하였습니다. ! \n")
    # Trie 인덱싱 결과
    #print(mytrie) ## 주석 해제하면 Trie 구조로 사전 출력 !


    # plain 사전 text 파일을 이용하여 TRIE 구조를 가지는 사전 구축 완료 ! #

    sentence=input("분석 문장을 입력하세요.\n")
    # sentence = '지혜로운 아들은 자기 아버지가 타이르는 말을 주의 깊게 듣지만 거만한 자는 꾸지람을 들으려고 하지 않는다. '
    #@ 디버그 용도 !
    synWord = sentence.split(' ') # 문장을 어절 단위로 분리한다.
    lenSynWord = len(synWord) # 어절의 개수를 센다.
    print('문장의 어절은 {}개 입니다'.format(lenSynWord))
    print('문장 분석 결과는 다음과 같습니다.')

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

        # ----------------------------------------------- #
        # STEP 2 : Tabluar Parsing을 이용하여 형태소 분석 시작  #
        # ----------------------------------------------- #

        for i in range (0, lenSyllable):
            for j in range (0, lenSyllable):
                currentWord = synWord[SynWordIdx]
                currentWord = currentWord[i:j+1] # 음절별로 처리할 단어를 자른다.
                currentData = mytrie.getData(currentWord) # Trie 사전에 해당 단어에 대한 문법 정보를 요청한다.
                if currentData != []:
                    if ' ' in currentData : # 단어에 해당하는 문법이 여러개일 경우 나눠서 저장한다.
                        currentData = currentData.split(' ')
                        table[i][j+1].extend(currentData)
                    else : # 단어에 해당하는 문법이 하나일 경우 저장한다.
                        table[i][j+1].append(currentData)
                else : # 문법이 없을 경우에 대한 예외처리
                    table[i][j+1].extend(currentData)
        # print(table)
        # print('Tablular parsing 1차 passing 완료 ')
        # 여기가 tabular parsing 완성! - 1차 passing

        grammar =[]
        for i in range (0,lenSyllable+1):
            for j in range (0, lenSyllable):

                if table[i][j] != []:
                    grammar = table[i][j] # table에 이미 저장되어있는

                    # 단어에 의미가 여러개 있을 경우도 생각해줘야 한다
                    for numOfMean in range (len(grammar)) :
                        grammarLoop = grammar[numOfMean]
                        for k in range (j+1, lenSyllable+1):
                            if table[j][k] != []:
                                currentGrammar = table[j][k]
                                # currentGrammar에도 뜻이 여러개 있을 수도 있다.
                                for means in range (len(currentGrammar)):
                                    resultGrammar = ''
                                    currentGrammarSeg = currentGrammar[means]
                                    resultGrammar += resultGrammar + grammarLoop + ' '+currentGrammarSeg+' '
                                    resultGrammar = resultGrammar[:-1]
                                    table[i][k].extend([resultGrammar])
        #print(table)
        printWord = synWord[SynWordIdx]

        # ------------------------------------------- #
        # STEP 3 : 문법 정보를 이용하여 결과를 출력하는 단계  #
        # ------------------------------------------- #
        for i in range(0, lenSyllable) :
            for j in range(1, lenSyllable+1) :
                currentTable = table[i][j]

                for k in range (len(currentTable)):

                    # 문법 정보를 검색해서 가능한 문법일 경우 결과 출력
                    # 검색 하기 전에 사전 포맷에 맞게 변경해야 함!
                    searchPattern = ''
                    if '/' in currentTable[k]:
                        searchKey = currentTable[k].replace('/', ' ').split(' ')
                        for reIdx in range(len(searchKey)):
                            if reIdx%2 == 1:
                                if searchPattern == '':
                                    searchPattern += searchKey[reIdx]
                                else :
                                    searchPattern = searchPattern +' '+searchKey[reIdx]
                    if searchPattern in myGrammar.contents :

                        print(str(currentTable[k]).replace(' ', '+'))