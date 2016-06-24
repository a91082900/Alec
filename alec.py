#-*- coding: utf-8 -*-

import random, os, time, datetime, sys

def error(cause):
    cause = str(cause)
    print('抽選失敗=口=\n原因：', cause, sep="")
    os.system("pause")
    sys.exit(1)
m_is_12 = 0

month = int(time.strftime('%m'))
today_day = int(time.strftime('%d'))
week = int(time.strftime('%w'))
year = int(time.strftime('%Y'))
retry_cnt = 0
version = "V1.1.61 16/03/02"

f = open('result.txt', 'a', encoding = 'UTF-8') #開檔

print("阿雷克吃飯了！", version, sep="")
print("{0}/{1}/{2}".format(year, str(month).zfill(2), str(today_day).zfill(2)), sep="") #sep為分隔符號，end為結尾符號

prev = []
try:
    dont_repeat = int(input('請問隔多少天後才能出現相同結果(預設3，必須為正整數):'))
    if dont_repeat<=0:
        raise ValueError('它必須要是正整數') #引發Error，跳到except
except:
    dont_repeat = 3
print(dont_repeat)
if today_day>=15:
    while 1:
        try:
            if month==12:
                m_is_12 = 1
                input_month = int(input("請問要抽12月還是1月:"))
            else:
                input_month = int(input("請問要抽" + str(month) + "月還是" + str(month+1) + "月:"))
                # input只能用一個參數，故把變數部份變為字串並串接
        except:
            input_month = 0
        if input_month==month+1 or (m_is_12 == 1 and input_month==1):
            if input_month==month+1:
                month = input_month
                today_day = 1
            elif m_is_12 == 1 and input_month==1:
                year += 1
                month = input_month
            print(month, "月\n注意：若未更新holiday.txt，請更新後再抽選", sep="")
            break
        if input_month==month:
            break

if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
    lastday = 31
elif month==4 or month==6 or month==9 or month==11:
    lastday = 30
else:
    if year%400==0 or (year%4==0 and year%100!=0):
        lastday = 29
    else:
        lastday = 28


print("請按任意鍵開始抽選")
os.system("pause>nul")
try:
    holiday = list(open("holiday.txt", 'r', encoding = 'UTF-8'))
    i = 0
    while i<len(holiday):
        holiday[i] = int(holiday[i]) #整數化（換行自動清除）
        i += 1
except:
    holiday = [0]

    
while 1:
    result = str(year) + "/" + str(month).zfill(2) + "/" + str(today_day).zfill(2) + '\n'
    subtotal = []
    try:
        store = list(open("store.txt", 'r', encoding = 'big5')) #有中文，若不特別改檔案編碼無法使用UTF-8
    except:
        error('找不到store.txt')
    i = 0
    while i<len(store):

        store[i] = store[i].strip("\n") #清除換行
        if store[i]=='.':
            delimiter1 = i
        if store[i]==',':
            delimiter2 = i
        i += 1
        subtotal.append(0)

    store_closed = {}

    i = 0
    while i<len(store):

        len_cnt = 1 #必須跳過店家
        try:
            #print("try", i)
            closed_len = len(store[i].split(" ")) - 1 #扣掉店家

            split_temp = store[i].split(" ")
            a = 0
            for j in split_temp:#j = split_temp[a]
                if j=='7':
                    split_temp[a] = '0'
                a += 1
            store[i] = split_temp[0]
        
            if closed_len>1:
                store_closed[store[i]] = [] #list
                while len_cnt<=closed_len:
                    store_closed[store[i]].append(int(split_temp[len_cnt]))
                    len_cnt += 1
            else:
                store_closed[store[i]] = int(split_temp[1])
        except:
            #print("except", i)
            store_closed[store[i]] = -1

        i += 1

    day = today_day
    prev_rand = -1
    prev2_rand = -1
    
    con = 0
    retry_cnt2 = 0
    while day<=lastday:
        
        week = int(datetime.datetime(year, month, day).strftime('%w'))
        if day in holiday and con==0:
            result += '*'
        if day+1 in holiday:
            rand = random.randint(delimiter1+1,len(store)-1)
        else:
            rand = random.randint(0,delimiter2-1)
        try:
            if week in store_closed[store[rand]]:
                i = -1
            else:
                i = 0
        except:
            if week==store_closed[store[rand]]:
                i = -1
            else:
                i = 0
    
        if retry_cnt2>=5000:
            error('無法抽選出當日結果')
        if store[rand]=='.' or store[rand]==',' or rand in prev or i ==-1 or (rand>delimiter2 and ((len(store)-1 - delimiter2 <=1 and subtotal[rand]>=2) or (len(store)-1 - delimiter2 >1 and subtotal[rand]>=1))):
            con = 1
            retry_cnt2 += 1
            continue
        con = 0
        if len(prev)>=dont_repeat:
            prev.pop(0)
        prev.append(rand)
        #print('rand = ', rand, ' prev = ', prev, '\n', rand in prev, '\n', sep='')
        result += str(month) + "月" + str(day) + "日("
        if week==0:
            result += '日'
        elif week==1:
            result += '一'
        elif week==2:
            result += '二'
        elif week==3:
            result += '三'
        elif week==4:
            result += '四'
        elif week==5:
            result += '五'
        else:
            result += '六'
        result += '):' + store[rand] + "\n"
        subtotal[rand] += 1
        day += 1
    subtotal.pop(delimiter1)
    i = 0
    a = 0
    normal = []
    while a<delimiter1:
        normal.append(subtotal.pop(i))
        a += 1
    subtotal.pop(delimiter2-1-a)
    feast = []
    i = delimiter2-1
    while i<=len(store)-2-1:#-2分隔號&索引值
        feast.append(subtotal.pop(delimiter2-1-a))
        i += 1

    if retry_cnt>=1000:
        error('無法抽選出全部結果')

    if feast!=[] and normal!=[]:#11
        if (max(subtotal)-min(subtotal)>2 or sum(feast)<1 or max(subtotal)-min(normal)>3) and retry_cnt<=500:
            retry_cnt += 1
            continue
        elif retry_cnt>500:
            if max(subtotal)-min(subtotal)>2 or max(subtotal)-min(normal)>3:
                retry_cnt += 1
                continue
    elif feast==[] and normal==[]:#00
        if max(subtotal)-min(subtotal)>2:
                retry_cnt += 1
                continue
    elif feast!=[] and normal==[]:#10
        if (max(subtotal)-min(subtotal)>2 or sum(feast)<1) and retry_cnt<=500:
            retry_cnt += 1
            continue
        elif retry_cnt>500:
            if max(subtotal)-min(subtotal)>2:
                retry_cnt += 1
                continue
    else:#01
        if (max(subtotal)-min(subtotal)>2 or max(subtotal)-min(normal)>3) and retry_cnt<=500:
            retry_cnt += 1
            continue     
    break
result += '----------------------------\n'
i = 0
subtotal = normal + subtotal + feast
for item in store:
    if item=="." or item==",":
        if item==store[0] or item==store[-1]:
            result += '無\n'
        result += '---------------------\n'
    else:
        result += item + ':' + str(subtotal[i]) + '次(' + str(round(subtotal[i]/(lastday-today_day+1)*100, 3)) + '%)\n'
        i += 1
result += '\n----------抽選結束----------\n'
print(result)
print(result, file=f)
f.close()
os.system("pause")

 
