######## オシロMSO24の波形画像をPCに取り込むpython ########
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
print(inst.query('*IDN?'))

# プログラムを終了させるときは'quit'をEnter
print('\nPlease enter \'quit\' to exit. \n')

# キャプチャ枚数確認(現Ver：7秒毎に1枚)
#   秒数オプションやマニュアル操作も実装した方が良い?
count_str = input('How many pict? (def=10): ')
if count_str == '':
    count_str = '10'
if count_str == 'quit':
    print('\n Capture \"NOT\" Completed\n')
    sys.exit()

# 40枚を超えるときはYes/No 確認
count_max = int(count_str)
if count_max > 40:
    y_or_n = input('\nIt will take more than 5min to capture screen.\n\
        Continue? [y or n] ')
    if y_or_n == 'y':
        pass
    else:
        print('\n Capture \"NOT\" Completed\n')
        sys.exit()

# 保存フォーマットの確認
type_f = input('Select Format [0:PNG&CSV 1:PNG 2:CSV (def=0)] ')
if type_f == '':
    type_f = '0'
if type_f == '0' or type_f == '1' or type_f == '2':
    pass
else :
    print('\n Invalid Value')
    print('\n Capture \"NOT\" Completed\n')
    sys.exit()

# アクティブなチャネルを確認
MAX_CH = 4
print('\n')
for i in range(MAX_CH):
    print('Enable CH' + str(i+1) +': ' + inst.query('DISplay:GLObal:CH'+str(i+1)+':STATE?'))

import capt_oscillo_v2
count = 0

# [count_max]枚をキャプチャする
while count < count_max:
    # オシロスコープstop
    inst.write('ACQuire:STATE STOP')

    if (count_max//40) > 1:
        if (count%5) == 0:
            print(' count = ' + str(count))
    else:
        print(' count = ' + str(count))

    capt_oscillo_v2.save_screen(count,inst,type_f)
    count += 1

    # オシロスコープrun
    inst.write('ACQuire:STATE RUN')

    if count < count_max:
        time.sleep(7)   # wait_7sec

# 保存したファイルを指定したディレクトリに移動
import move_file
move_file.main(type_f)

# 測定終了
print('\n Capture Completed\n')

# 測定終了後にオシロスコープとの通信を切断する
inst.close()
rm.close()

