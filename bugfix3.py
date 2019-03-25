import rpyc
import time
from rpyc.utils.server import ThreadedServer
from multiprocessing import Process
import numpy as np

RPYC_CONFIG = rpyc.core.protocol.DEFAULT_CONFIG
RPYC_CONFIG['allow_pickle'] = True

class DataService(rpyc.Service):
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.data = []
        print("DataService object with name: ", name," and port: ", port)

    def on_connect(self, conn):
        print("Connected to ", self.name, " trough ", conn, " with root object: ", conn.root)

    def on_disconnect(self, conn):
        print("Disconnected from", self.name)
    
    def start_service(self):
        print("Starting ", self.name, " rpyc treadh with self: ", self)
        self.rpyc_thread = ThreadedServer(self, port=self.port, protocol_config=RPYC_CONFIG)
        self.rpyc_thread.start() #blocking call
    
    def exposed_add_data(self, data):
        print(self.name, " add_data was called with data: ", data)
        if isinstance(data, list): 
            self.data += data
        elif isinstance(data, np.ndarray):
            self.data = np.append(self.data, data)
        else:
            self.data.append(data)
        print(self.name, " self.data is now: ", self.data)

    def exposed_get_data(self):
        print(self.name, " get_data was called and returns data: ", self.data)
        return self.data

class DataServiceHelper():
    def __init__(self, name):
        self.name = name

    def connect(self, port):
        self.conn = rpyc.connect("localhost", port=port, config=RPYC_CONFIG)
        print(self.name, " connected with conn ", self.conn, " with root object: ", self.conn.root) 
    
class GenerateData(DataServiceHelper):
    def __init__(self):
        DataServiceHelper.__init__(self, "GENDATA" )

    def loop(self):
        i = 0
        while True:
            self.conn.root.add_data(i)
            print(self.name, " called add_data with ", i)
            i += 1
            time.sleep(1)

class ProcessData(DataServiceHelper):
    def __init__(self):
        DataServiceHelper.__init__(self, "PROCESSDATA" )

    def loop(self):
        while True:
            data = self.conn.root.get_data()
            print(self.name, " got data: ", data)
            processed = self.process_data(data)
            print(self.name, " processed data with result: ", processed)
            #self.data.append(processed)
            time.sleep(3)
    
    def process_data(self, data):
        return sum(data)

def data_service():
    data_service = DataService("GENDATASERVICE", 18861)
    data_service.start_service()

def generate_data():
    gen_data = GenerateData()
    gen_data.connect(18861)
    gen_data.loop()

def process_data():
    process_data = ProcessData()
    process_data.connect(18861)
    process_data.loop()

if __name__ == "__main__":
    data_service_process = Process(target=data_service)
    data_service_process.start()
    
    gen_data_process = Process(target=generate_data)
    gen_data_process.start()

    pro_data_process = Process(target=process_data)
    pro_data_process.start()

    while True:
        pass

