######## オシロの波形画像をPCに取り込むpython ########
import pyvisa
import time
import sys

# VisaAddrの取得
rm = pyvisa.ResourceManager()
print(rm.list_resources())

#### GPIB制御とかしようとするとここらへんでエラー吐くかも? ####
VISAAddr = rm.list_resources()
VISAAddr_str0 = VISAAddr[0]
#### GPIB制御とかしようとするとここらへんでエラー吐くかも? ####

inst = rm.open_resource(VISAAddr_str0)

# 接続確認 (機器識別コードを返します。できない場合はエラーで終了)
id_osc = inst.query('*IDN?')
print(id_osc)

import re
if 'DPO' or 'TDS' or 'TBS' in id_osc:
    # todo 'DPO' or 'TDS' or 'TBS'->サポートオシロリストを変数に入れたい
    id_osc = re.search(r'(DPO|TDS|TBS)',id_osc) #オシロ判定（使いたいオシロがこのプログラムにサポートされているか確認）
    id_osc = id_osc.group()
    print(id_osc + ' is supported "only PNG" in this version.')
    # sys.exit()  #未完成のためここで終了
elif 'MSO' in id_osc:
    id_osc = 'MSO'
else:
    print('\n This oscilloscope is \"NOT\" supported.\n')
    sys.exit()
# プログラムを終了させるときは'quit'をEnter
print('\nPlease enter \'quit\' to exit. \n')

# キャプチャ枚数確認(現Ver：7秒毎に1枚)
#   秒数オプションも実装した方が良い?
t_wait = 7
count_max = input('How many pict? (def=10): ') or '10'
if count_max == 'quit':
    print('\n Capture \"NOT\" Completed\n')
    sys.exit()
count_max = int(count_max)

# 40枚を超えるときはYes/No 確認
if count_max > 40:
    y_or_n = input('\nIt will take a long time to capture screen.\n\
                    Continue? [y or n] ') or 'y'
    if y_or_n == 'y':
        pass
    else:
        print('\n Capture \"NOT\" Completed\n')
        sys.exit()

# 保存フォーマットの確認
type_f = input('Select Format [0:PNG&CSV 1:PNG 2:CSV (def=0)] ') or '0'
try:
    int_f=int(type_f)
except ValueError as e:
    print(type_f)
    print('\n Capture \"NOT\" Completed\n')
    sys.exit()
if int_f >= 0 and int_f <= 2 :
    pass
else :
    print('\n Invalid Value')
    print(' Capture \"NOT\" Completed\n')
    sys.exit()

# アクティブなチャネルを確認
MAX_CH = 4

print('\n')
# todo Enable_CHを判断しCSV出力
if id_osc == 'MSO':
    for i in range(MAX_CH):
        print('Enable CH' + str(i+1) +': ' + inst.query('DISplay:GLObal:CH'+str(i+1)+':STATE?'))    #このコマンドはMSOでしか使えなさそう

import capt_oscillo_v2
import capt_oscillo_v3
count = 0

auto_capt = input('"Auto[A]" or "Manual[M]"? : ') or 'A'
if 'Auto' in auto_capt or auto_capt == 'A':
    auto_capt = 'A'
    capt_ready = input('Ready? "y" or "n" :') or 'y'
    while capt_ready !="y":
        print("\n Waiting...\n")
        time.sleep(1)
        capt_ready = input('Ready? "y" or "n" :') or 'y'
        if capt_ready == 'quit':
            print('\n Capture \"NOT\" Completed\n')
            sys.exit()
elif 'Manual' in auto_capt or auto_capt == 'M':
    auto_capt = 'M'
else:
    print('\n Invalid Value')
    print(' Capture \"NOT\" Completed\n')
    sys.exit()
# exit()  #for debug

# [count_max]枚をキャプチャする
while count < count_max:
    if auto_capt == 'M':
        capt_ready = input('Ready? "y" or "n" :') or 'y'
        if capt_ready == 'quit':
            print('\n Capture canceled\n')
            break

        while capt_ready !="y":
            print("\n Waiting...\n")
            time.sleep(1)
            capt_ready = input('Ready? "y" or "n" :') or 'y'
            if capt_ready == 'quit':
                break
        if capt_ready == 'quit':
            print('\n Capture canceled\n')
            break
        
    # オシロスコープstop
    if auto_capt == 'A':
        inst.write('ACQuire:STATE STOP')

    if (count_max//40) > 1:
        if (count%5) == 0:
            print(' count = ' + str(count))
    else:
        print(' count = ' + str(count))

    if id_osc == 'MSO':
        capt_oscillo_v2.save_screen(count,inst,type_f)
    elif id_osc == 'DPO' or id_osc == 'TDS':
        capt_oscillo_v3.save_screen(count,inst,type_f)

    count += 1

    # オシロスコープrun
    if auto_capt == 'A':
        inst.write('ACQuire:STATE RUN')

    if count < count_max:
        time.sleep(t_wait)   # wait_7sec

# 保存したファイルを指定したディレクトリに移動
import move_file
move_file.main(type_f)

# 測定終了
print('\n Capture Completed\n')

# 測定終了後にオシロスコープとの通信を切断する
inst.close()
rm.close()

