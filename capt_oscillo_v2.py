######## オシロMSO24の波形画像をPCに取り込む ########
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

    # オシロスコープの内蔵HDにテンポラリのキャプチャ画像を保存
    inst.write('SAVE:IMAGe \"C:/Temp.png\"')

    # 画像のキャプチャ処理が終了するまで待つ
    while inst.query('*OPC?')[0]!="1":
        print("Waiting")
        time.sleep(1)   #Wait_1sec

    # 保存された画像ファイルをPC側へ読み出す
    inst.write('FILESystem:READFile \"C:/Temp.png\"')
    img_data = inst.read_raw()

    # PC側に保存する際にdatetimeモジュールを使い、日付＋時間のファイル名で保存する
    dt=datetime.now()
    filename = dt.strftime("IMG" + str(count_sv) + "_%Y%m%d_%H%M%S.png")
    file = open(filename,"wb")
    file.write(img_data)
    file.close()

def save_csv(count_sv, inst):
    import pyvisa
    import time
    from datetime import datetime
    import pandas as pd

    MAX_CH = 4     #オシロスコープの最大チャンネル数
    ch_en=[]
    IsFirstCh = True
    # IsFirstCh = False

    #アクティブ状態のチャンネルを検出する（同時に最も若い番号のチャンネル番号も取得）
    for i in range(MAX_CH):
        ch_en.append(int(inst.query('DISplay:GLObal:CH'+str(i+1)+':STATE?')))
        if ch_en[i] == 1 and IsFirstCh:
            first_ch = i
            print('first_ch = ' + str(first_ch)) #for debug
            IsFirstCh = False

    print('ch_en = ')  #for debug
    print(ch_en)  #for debug

    #チャンネルごとに波形データ取得処理
    csv_lst = [ 0 for i in range(MAX_CH)]

    for n in range(MAX_CH):
        #チャンネルがアクティブなら波形取得処理開始
        print('ch_en[' + str(n) + '] = ' + str(ch_en[n]))   #for debug
        if ch_en[n]==1:
            #チャンネル番号を生成し、PyVISAでオシロスコープの内蔵HDに波形データを保存させる
            ch_no = "CH" + str(n+1)
            print('ch_no = ' + ch_no)   #for debug

            inst.write('SAVE:WAVEform '+ch_no+', \"C:/Temp.csv\"')
            # inst.write('SAVE:WAVEform CH'+str(i+1)+', \"C:/Temp.csv\"')
            
            #PC側へ保存する個別波形データの名前を定義
            filename = "temp_" + ch_no +".csv"
            csv_lst [n] = filename
            print(filename)
            print(csv_lst)

            #波形データの保存処理が終了するまで待つ
            while inst.query('*OPC?')[0]!="1":
                print("Waiting")
                time.sleep(1)
                
            #オシロスコープ上の波形データを読み出す
            inst.write('FILESystem:READFile \"C:/Temp.csv\"')
            wave_data = inst.read_raw()
            
            #読み出した波形データを指定したファイル名でPCに保存
            file = open(filename,"wb")
            file.write(wave_data)
            file.close()
            
            #処理終了を示すメッセージ
            # print("Channel "+ str(ch_no) + " Done")

    #オシロスコープ側のテンポラリ画像ファイルを削除
    inst.write('FILESystem:DELEte \"C:/Temp.csv\"')
    print('Delete temp file.')  #for debug

    ###### 波形データの統合処理 ######
    CSV_HEADER_ROWS = 7
    CSV_SKIP_ROWS = 9

    #アクティブチャンネルを検出した数だけ波形データの格納リストを作る
    ch_wave =[[] for i in range(sum(ch_en))]

    #最も若いチャンネル番号のcsv波形データファイルからヘッダデータと時間軸データを取得
    header = pd.read_csv(csv_lst[first_ch],header = None, nrows = CSV_HEADER_ROWS)
    time_dt = pd.read_csv(csv_lst[first_ch],header = None, usecols=[0],skiprows=CSV_SKIP_ROWS)

    #最大チャンネル数まで波形データが保存されているかをチェックし、あれば格納リストにcsvデータを格納
    wave_cnt = 0
    for i in range(MAX_CH):
        if csv_lst[i]!=0:
            ch_wave[wave_cnt] = pd.read_csv(csv_lst[first_ch],header = None, usecols=[1],skiprows=CSV_SKIP_ROWS)
            ch_wave[wave_cnt].columns =["CH" +str(i+1)]
            wave_cnt +=1
            
    #取得したチャンネルごとの波形データを1つのDataFrameに統合(最初の列は時間軸にする)
    out_dt = time_dt
    for i in range(sum(ch_en)):
        out_dt = pd.concat([out_dt,ch_wave[i]],axis=1)

    # PC側に保存する際にdatetimeモジュールを使い、日付＋時間のファイル名で保存する
    dt=datetime.now()
    wave_filename = dt.strftime("DATA" + str(count_sv) + "_%Y%m%d_%H%M%S.csv")

    #Pandasの機能を使って、DataFrameをcsvに変換。このとき個別のcsvとヘッダデータ部分は共通にする
    header.to_csv(wave_filename,header= False, index = False)
    out_dt.to_csv(wave_filename,header= True, index = False,mode = 'a')
    print("Wave File #" + str(count_sv) + " Output Complete")

#############################################################
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
 
    # 接続確認 (機器識別コードを返します。できない場合はエラーで終了)
    inst = rm.open_resource(VISAAddr_str0)
    print(inst.query('*IDN?'))

    #オシロスコープstop
    inst.write('ACQuire:STATE STOP')

    type_f = input('Select Format[0:PNG&CSV 1:PNG 2:CSV (def=2)] ')
    if type_f == '':
        type_f = '2'
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

    save_screen(100,inst,type_f)
    
    #オシロスコープrun
    inst.write('ACQuire:STATE RUN')

    #測定終了
    print('Capture Completed')

    #測定終了後にオシロスコープとの通信を切断する
    inst.close()
    rm.close()