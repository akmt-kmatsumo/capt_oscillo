###オシロMSO24の波形画像をPCに取り込む###
def save_screen(count_i,inst,type_f):
    if type_f == "0":
        save_img(count_i,inst)
        save_csv(count_i,inst)
    if type_f == "1":
        save_img(count_i,inst)
    if type_f == "2":
        save_csv(count_i,inst)

def save_img(count_sv,inst):
    import pyvisa
    import time
    from datetime import datetime

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

def save_csv(count_sv, inst):
    import pyvisa
    import time
    from datetime import datetime

    #チャンネル1の波形データを内蔵HDにcsv形式で保存する
    inst.write('SAVE:WAVEform CH1, \"C:/Temp.csv\"')

    #波形データの保存処理が終了するまで待つ
    while inst.query('*OPC?')[0]!="1":
        print("Waiting")
        time.sleep(1)   #Wait_1sec

    #保存されたcsvファイルをPC側へ読み出す
    inst.write('FILESystem:READFile \"C:/Temp.csv\"')
    wave_data = inst.read_raw()

    #PC側に保存する際にdatetimeモジュールを使い、日付＋時間のファイル名で保存する
    dt=datetime.now()
    filename = dt.strftime("DATA" + str(count_sv) + "_%Y%m%d_%H%M%S.csv")
    file = open(filename,"wb")
    file.write(wave_data)
    file.close()



if __name__ == "__main__":
    import pyvisa

    #VisaAddrの取得
    rm = pyvisa.ResourceManager()
    #print(rm.list_resources())

    VISAAddr = rm.list_resources()
    #print(VISAAddr[0])

    VISAAddr_str0 = VISAAddr[0]
    #print(VISAAddr_str0)

    import time
    from datetime import datetime
 
     #接続確認 (機器識別コードを返します)
    inst = rm.open_resource(VISAAddr_str0)
    #print(inst.query('*IDN?'))

    #オシロスコープstop
    inst.write('ACQuire:STATE STOP')

    type_f = input('Select Format[0:PNG&CSV 1:PNG 2:CSV] ')
    save_screen(100,inst,type_f)
    
    #オシロスコープrun
    inst.write('ACQuire:STATE RUN')

    #測定終了
    print('Capture Completed')

    #測定終了後にオシロスコープとの通信を切断する
    inst.close()
    rm.close()