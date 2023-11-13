###オシロMSO24の波形画像をPCに取り込む###
def main(type_f):
    if type_f == "0":
        move_img()
        move_csv()
    elif type_f == "1":
        move_img()
    elif type_f == "2":
        move_csv()

def move_img():
    import sys
    import os
    import shutil
    import glob

    current_dir = os.getcwd()

    save_into = input('Save png into ' + current_dir + '\\pict\\[dir_name] \n\
    dir_name (def=test) =  ')
    if save_into == '':
        save_into = 'test'
    if save_into == 'quit':
        print('\n Caution : File still remains in ' + current_dir)
        print('\n Capture \"NOT\" Completed\n')
        sys.exit()

    path_ok = os.path.isdir(current_dir + '\\pict\\' + save_into)
    if path_ok == False:
        if os.path.isdir(current_dir + '\\pict\\') == False:
            os.mkdir(current_dir + '\\pict\\')
        os.mkdir(current_dir + '\\pict\\' + save_into)

    for p in glob.glob(current_dir + '\\IMG*.png', recursive=True):
        shutil.move(p, current_dir + '\\pict\\' + save_into)

def move_csv():
    import sys
    import os
    import shutil
    import glob

    current_dir = os.getcwd()

    save_into = input('Save csv into ' + current_dir + '\\csv\\[dir_name] \n\
    dir_name (def=test) = ')
    
    if save_into == '':
        save_into = 'test'
    if save_into == 'quit':
        print('\n Caution : File still remains in ' + current_dir)
        print('\n Capture \"NOT\" Completed\n')
        sys.exit()

    path_ok = os.path.isdir(current_dir + '\\csv\\' + save_into)
    if path_ok == False:
        if os.path.isdir(current_dir + '\\csv\\') == False:
            os.mkdir(current_dir + '\\csv\\')
        os.mkdir(current_dir + '\\csv\\' + save_into)
    
    for p in glob.glob(current_dir + '\\DATA*.csv', recursive=True):
        shutil.move(p, current_dir + '\\csv\\' + save_into)

if __name__ == "__main__":
    import sys

    print('\nPlease enter \'quit\' to exit. \n')

    type_f = input('Select Format [0:PNG&CSV 1:PNG 2:CSV (def=0)] ')
    if type_f == '':
        type_f = '0'
    if type_f == '0' or type_f == '1' or type_f == '2':
        pass
    elif type_f == 'quit':
        print('\n Quit')
        print('\n Capture \"NOT\" Completed\n')
        sys.exit()
    else :
        print('\n Invalid Value')
        print('\n Capture \"NOT\" Completed\n')
        sys.exit()

    main(type_f)
    print('\n Completed\n')
