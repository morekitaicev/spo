from __future__ import print_function
import requests, bs4
import numpy as np
import matplotlib.pyplot as plt

f = open('election_final.txt', 'w')

pages_to_parse = ['http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&root=1&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217417&type=222']

table = requests.get('http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&root=1&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217417&type=222')
soup = bs4.BeautifulSoup(table.text, "html.parser")
collect = soup.find('body')
b_tags_on_page = collect.findAll('b')

start_table = []

for x in b_tags_on_page:
    start_table.append(str(x))


for i in range(len(start_table)):
    start_table[i] = start_table[i].replace('<b>', '')
    start_table[i] = start_table[i].replace('</b>', '')
    start_table[i] = start_table[i].replace('\xa0', '0')

result_table = []
for i in range(15):
    result_table.append(start_table[4+i])
del start_table[0:19]


TIK = {}
for i in range(31):
    TIK[i] = []

count_big_table = 0
big_table = np.zeros((14, 31))



for i in range(14):
    for j in range(31):
        big_table[i,j] = start_table[count_big_table]
        count_big_table += 1

np.set_printoptions(suppress=True)


for i in range(31):
    link = str(419+i)
    pages_to_parse = ['http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217'+link+'&type=222']
    table = requests.get('http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217'+link+'&type=222')
    soup = bs4.BeautifulSoup(table.text, "html.parser")
    collect = soup.find('body')
    b_tags_on_page = collect.findAll('b')
    start_table = []
    for x in b_tags_on_page:
      start_table.append(str(x))
    for j in range(len(start_table)):
        start_table[j] = start_table[j].replace('<b>', '')
        start_table[j] = start_table[j].replace('</b>', '')
        start_table[j] = start_table[j].replace('\xa0', '0')
    del start_table[0:19]
    number = len(start_table) // 14
    TIK[i] = np.zeros((15, number))
    count_big_table = 0
    for r in range(14):
        for j in range(number):
            TIK[i][r, j] = start_table[count_big_table]
            TIK[i] = np.array(TIK[i])
            count_big_table += 1


TIK[30] = np.zeros((14, 1))
for i in range(14):
    TIK[30][i,0] = big_table [i, 30]

UIK = {}
for i in range(31):
    UIK[i] = []



for i in range(30):
    link = str(419+i)
    pages_to_parse = ['http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217'+link+'&type=222']
    table = requests.get('http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217'+link+'&type=222')
    soup = bs4.BeautifulSoup(table.text, "html.parser")
    collect = soup.find('body')
    nobr_tags_on_page = collect.findAll('nobr')
    uik_start_table = []
    for x in nobr_tags_on_page:
      uik_start_table.append(str(x))
    for j in range(len(uik_start_table)):
        uik_start_table[j] = uik_start_table[j].replace('<b>', '')
        uik_start_table[j] = uik_start_table[j].replace('<nobr>', '')
        uik_start_table[j] = uik_start_table[j].replace('</b>', '')
        uik_start_table[j] = uik_start_table[j].replace('</nobr>', '')
        uik_start_table[j] = uik_start_table[j].replace('\xa0', '0')
    for p in range(len(uik_start_table)):
        if  uik_start_table[p][0] == 'У':
            UIK[i].append(uik_start_table[p])


for i in range(30):
    for j in range(TIK[i].shape[1]):
        TIK[i][14,j] = int(''.join(filter(str.isdigit, UIK[i][j])))


vibros = []

for j in range(30):
    y_axis = []
    for i in range(TIK[j].shape[1]):
        y_axis.append((TIK[j][2, i] + TIK[j][3, i]) / TIK[j][0, i])
    sd = np.std(y_axis)
    sr = np.mean(y_axis)
    for i in range(TIK[j].shape[1]):
        if ((TIK[j][2, i] + TIK[j][3, i]) / TIK[j][0, i]) - sr >= 2*sd:
            vibros.append(TIK[j][14,i])

f.write(str(vibros))


x_axis = []
y_axis = []
y_axis_beglov = []

fig = plt.figure()

for j in range(31):
    x_axis = []
    y_axis = []
    y_axis_beglov = []
    for i in range(TIK[j].shape[1]):
        x_axis.append(1 + i)
        y_axis.append((TIK[j][2,i]+TIK[j][3,i]) / TIK[j][0,i])
        y_axis_beglov.append(TIK[j][12,i] / TIK[j][0,i])
    plt.subplot(7, 5, j+1)
    plt.bar(x_axis, y_axis)
    plt.bar(x_axis, y_axis_beglov)
    str_TIK = 'ТИК №' + str(j+1)
    plt.title(str_TIK)

plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.25, hspace=0.7)
plt.show()

x_axis = []
y_axis = []

for j in range(31):
    for i in range(TIK[j].shape[1]):
        x_axis.append(TIK[j][0,i])
        y_axis.append((TIK[j][2,i]+TIK[j][3,i]) / TIK[j][0,i])

fig,axs = plt.subplots(1, 2)
axs[0].scatter(x_axis, y_axis)
axs[0].set_xlabel('Количество избирателей')
axs[0].set_ylabel('Явка')
fig.suptitle('Зависимость явки от количества избирателей')
axs[1].bar(x_axis, y_axis)
axs[1].set_xlabel('Количество избирателей')
axs[1].set_ylabel('Явка')
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.25, hspace=0.7)
plt.show()


x_axis = []
y_axis = []

for j in range(31):
        x_axis.append(TIK[j].shape[1])
        y_axis.append((big_table[2,j]+big_table[3,j]) / big_table[0,j])

fig,axs = plt.subplots(1, 2)
axs[0].scatter(x_axis, y_axis)
axs[0].set_xlabel('Количество УИКов')
axs[0].set_ylabel('Явка')
fig.suptitle('Зависимость явки от количества избирателей')
axs[1].bar(x_axis, y_axis)
axs[1].set_xlabel('Количество УИКов')
axs[1].set_ylabel('Явка')
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.25, hspace=0.7)
plt.show()