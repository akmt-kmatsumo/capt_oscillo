###オシロMSO24の波形画像をPCに取り込む###
import pyvisa
import pandas as pd

#VisaAddrの取得
rm = pyvisa.ResourceManager()
print(rm.list_resources())

VISAAddr = rm.list_resources()
#print(VISAAddr[0])

VISAAddr_str0 = VISAAddr[0]
#print(VISAAddr_str0)

import time
from datetime import datetime
 
 #接続確認 (機器識別コードを返します)
inst = rm.open_resource(VISAAddr_str0)
print(inst.query('*IDN?'))

count = 0
while count < 10:
    #オシロスコープstop
    inst.write('ACQuire:STATE STOP')

    #アクティブ状態のチャンネルを検出する（同時に最も若い番号のチャンネル番号も取得）
    for i in range(MAX_CH):
        ch_en.append(int(inst.query('DISplay:GLObal:CH'+str(i+1)+':STATE?')))
        if ch_en[i] == 1 and IsFirstCh:
            first_ch = i
            IsFirstCh = False

    #チャンネルごとに波形データ取得処理
    csv_lst = [ 0 for i in range(MAX_CH)]

    #オシロスコープの内蔵HDにテンポラリのキャプチャ画像を保存
    inst.write('SAVE:IMAGe \"C:/Temp.png\"')

    #画像のキャプチャ処理が終了するまで待つ
    while inst.query('*OPC?')[0]!="1":
        print("Waiting")
        time.sleep(1)   #Wait_1sec

    #保存された画像ファイルをPC側へ読み出す
    inst.write('FILESystem:READFile \"C:/Temp.png\"')
    img_data = inst.read_raw()

    #PC側に保存する際にdatetimeモジュールを使い、日付＋時間のファイル名で保存する
    dt=datetime.now()
    filename = dt.strftime("IMG" + str(count_sv) + "_%Y%m%d_%H%M%S.png")
    file = open(filename,"wb")
    file.write(img_data)
    file.close()

    #オシロスコープrun
    inst.write('ACQuire:STATE RUN')
    time.sleep(7)   #Wait_7sec
    count += 1

#測定終了
print('Capture Completed')

#測定終了後にオシロスコープとの通信を切断する
inst.close()
rm.close()
