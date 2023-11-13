###オシロMSO24接続確認###
def set_osillo():

    import pyvisa

    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

    VISAAddr = rm.list_resources()
    print(VISAAddr[0])

    VISAAddr_str0 = VISAAddr[0]
    print(VISAAddr_str0)

    import time
    from datetime import datetime
     
    #接続確認 (機器識別コードを返します)
    inst = rm.open_resource(VISAAddr_str0)
    print(inst.query('*IDN?'))

if __name__ == "__main__":
    set_osillo