from bs4 import BeautifulSoup
import matplotlib as plt
import requests
import pandas as pd
#import numpy as np
url = "http://www.pogodaiklimat.ru/history/27612.htm"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
response = requests.get(url, headers=headers)
print(response)
bs = BeautifulSoup(response.content, "lxml")
bs.encoding = 'utf-8'
print(bs)
ind = bs.find('div', 'chronicle-table-left-column')
nameRows = []
for elemInd in ind.find_all('td'):
    nameRows.append(elemInd.text)
print(nameRows)
elements = bs.find('div', 'chronicle-table')
masTable = []
for row in elements.find_all('tr'):
    masRow = []
    for atomElem in row.find_all('td'):
        masRow.append(atomElem.text)
    masTable.append(masRow)
print(masTable)

tableDict = dict()
for i in range(len(masTable) - (2023 - 1821 + 1) - 1, len(masTable) - 1):
    for j in range(0, len(masTable[i])):
        if masTable[i][j] == '999.9':
            masTable[i][j] = str((float(masTable[i-1][j]) + float(masTable[i+1][j])) / 2.0)
    tableDict[nameRows[i]] = masTable[i]
print(tableDict)
tableDF = pd.DataFrame.from_dict(tableDict, orient='index', columns=masTable[0])
print(tableDF)
tableDF.to_excel("ML_LR5.xlsx", sheet_name='Погода в Москве по годам')
read_file = pd.read_excel("ML_LR5.xlsx", index_col=0)
print(read_file)
read_file.to_csv("ML_LR5.csv", index=True, header=True)
read_csv = pd.DataFrame(pd.read_csv("ML_LR5.csv", index_col=0))
print(read_csv)


