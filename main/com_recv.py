import serial
import threading
import time
import re
import json

class COM_RECV():

    def __init__(self):
        self.x=serial.Serial('COM2',115200)
        t1 = threading.Thread(target=self.jieshou,name="jieshou")
        t1.start()

    def fasong(self):
        while True:
            myinput=input('shuru>')
            myinput=myinput.encode(encoding="utf-8")
            self.x.write(myinput)

    def jieshou(self):
        myout = ""
        data = ""
        end_flag = "end"

        jsondata = {}
        row_idx = 0

        while True:
            while self.x.inWaiting() > 0:
                data = self.x.readline().decode()
                pattern = re.compile(r"(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)\r\n")
                match = pattern.match(data)
                if match:
                    # print(match.groups())
                    jsondata[row_idx] = list( match.groups() )
                    row_idx = row_idx + 1
                    
            # 完整接收了一帧串口数据
            if end_flag in data:
                # print(jsondata)
                self.updated_data = jsondata
                data = ""
                # jsondata = {}
                row_idx = 0

                self.x.close()


