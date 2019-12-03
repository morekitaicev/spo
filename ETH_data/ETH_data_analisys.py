from web3 import Web3
import matplotlib.pyplot as plt
from collections import Counter
import statistics

def stats(flist, sname):
    file_name = sname + '_output.txt'
    f = open(file_name, 'w')
    f.write('Медиана ' + "{0:.4f}".format(statistics.median(flist)))
    razmah = max(flist) - min(flist)
    f.write('Размах ' + "{0:.4f}".format(razmah))
    f.write('Матожидание ' + "{0:.4f}".format(statistics.mean(flist)))
    f.write('Дисперсия ' + "{0:.4f}".format(statistics.variance(flist)))
    f.write('Отклонение ' + "{0:.4f}".format(statistics.stdev(flist)))

def graph(glist, gname, g_xaxis, g_yaxis):
    glist_cnt = Counter(glist)
    plt.scatter(glist_cnt.keys(), glist_cnt.values())
    plt.title(gname)
    plt.xlabel(g_xaxis)
    plt.ylabel(g_yaxis)
    save_name = gname + '.jpg'
    plt.savefig(save_name)

web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/0da878a13bf145a6b9349a0f738205e8"))

smart_contract = 0
N = 8939400
block_gasUsed = []
block_price = []

for i in range(1000):
    print("Taking block: ", web3.eth.getBlock(N+i)['number'], ' (', str(i+1), 'по номеру прохождения)')
    price = []
    gasUsed = []
    for r in web3.eth.getBlock(N+i)['transactions']:
        tr = web3.eth.getTransaction(r)
        rec = web3.eth.getTransactionReceipt(r)
        gasUsed.append(rec['gasUsed'])
        price.append(tr['gasPrice'])
        if tr['input'] != '0x':
            smart_contract = smart_contract + 1
    block_gasUsed.append(gasUsed)
    block_price.append(price)

block_num = []
block_commision = []
block_rel = []

for i in range(1000):
   commision = 0
   for r in range(len(block_price[i])):
       commision = commision + block_price[i][r] * block_gasUsed[i][r] / (10**18)
   block_num.append(i+N)
   block_commision.append(round(commision, 4))
   block_rel.append(round(((commision / (commision + 2)) * 100), 3))



stats(block_commision, 'Абсолютное значение')
stats(block_rel, 'Относительное значение')

graph(block_commision, 'Группы блоков с одинаковой комиссией', 'Комиссия в ETH', 'Количество блоков в группе')
graph(block_rel, 'Группы блоков с одинаковым процентом комиссии', 'Комиссия в %', 'Количество блоков в группе')

print('Количество смарт контрактов:', smart_contract)