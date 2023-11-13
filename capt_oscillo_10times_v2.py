###オシロMSO24の波形画像をPCに取り込む###
import pyvisa
import time
import sys

#VisaAddrの取得
rm = pyvisa.ResourceManager()
print(rm.list_resources())

VISAAddr = rm.list_resources()
VISAAddr_str0 = VISAAddr[0]

inst = rm.open_resource(VISAAddr_str0)

#接続確認 (機器識別コードを返します)
print(inst.query('*IDN?'))

print('\nPlease enter \'quit\' to exit. \n')

count_str = input('How many pict? (def=10): ')
if count_str == '':
    count_str = '10'
if count_str == 'quit':
    print('\n Capture \"NOT\" Completed\n')
    sys.exit()    
count_max = int(count_str)
if count_max > 40:
    y_or_n = input('\nIt will take more than 5min to capture screen.\n\
        Continue? [y or n] ')
    if y_or_n == 'y':
        pass
    else:
        print('\n Capture \"NOT\" Completed\n')
        sys.exit()

type_f = input('Select Format [0:PNG&CSV 1:PNG 2:CSV (def=0)] ')
if type_f == '':
    type_f = '0'
if type_f == '0' or type_f == '1' or type_f == '2':
    pass
else :
    print('\n Invalid Value')
    print('\n Capture \"NOT\" Completed\n')
    sys.exit()

import capt_oscillo
count = 0

while count < count_max:
    #オシロスコープstop
    inst.write('ACQuire:STATE STOP')

    if (count_max//40) > 1:
        if (count%5) == 0:
            print('count = ' + str(count))
    else:
        print('count = ' + str(count))

    capt_oscillo.save_screen(count,inst,type_f)
    count += 1

    #オシロスコープrun
    inst.write('ACQuire:STATE RUN')

    if count < count_max:
        time.sleep(7)   #wait_7sec

import move_file
move_file.main(type_f)

#測定終了
print('\n Capture Completed\n')

#測定終了後にオシロスコープとの通信を切断する
inst.close()
rm.close()

