import rpyc
import time
from rpyc.utils.server import ThreadedServer
from multiprocessing import Process

RPYC_CONFIG = rpyc.core.protocol.DEFAULT_CONFIG
RPYC_CONFIG['allow_pickle'] = True

class LoopService(rpyc.Service):
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.data = []
        self.conn = None
        print("LoopService object with name: ", name," and port: ", port)

    def on_connect(self, conn):
        print("Connected to ", self.name, " trough ", conn, " with root object: ", conn.root)

    def on_disconnect(self, conn):
        print("Disconnected from", self.name)
    
    def connect(self, port):
        self.conn = rpyc.connect("localhost", port=port, config=RPYC_CONFIG)
        print(self.name, " connected with conn ", self.conn, " with root object: ", self.conn.root)
    
    def register_loop_function(self, loop_function):
        self.loop_function = loop_function

    def _start_service(self):
        print("Starting ", self.name, " rpyc treadh with self: ", self)
        self.rpyc_thread = ThreadedServer(self, port=self.port, protocol_config=RPYC_CONFIG)
        self.rpyc_thread.start()
   
    def start_service(self):
        print("Starting ", self.name, " service with self: ", self)
        self.rpyc_process = Process(target=self._start_service)
        self.rpyc_process.start()

    def run(self):
        print("Starting ", self.name, " loop with self: ", self)
        self.loop_process = Process(target=self.loop_function)
        self.loop_process.start()
    
    def exposed_get_data(self):
        print(self.name, " get_data was called and returns data: ", self.data)
        return self.data

class GenerateData(LoopService):
    def __init__(self):
        LoopService.__init__(self, "GENDATA", 18861 )
        LoopService.register_loop_function(self, self.loop)

    def loop(self):
        i = 0
        while True:
            self.data.append(i)
            print(self.name, " appended ", i , " to self.data: ", self.data)
            i += 1
            time.sleep(1)

class ProcessData(LoopService):
    def __init__(self):
        LoopService.__init__(self, "PROCESSDATA", 18862)
        LoopService.register_loop_function(self, self.loop)

    def loop(self):
        while True:
            data = self.conn.root.get_data()
            print(self.name, " got data: ", data)
            processed = self.process_data(data)
            self.data.append(processed)
            time.sleep(3)
    
    def process_data(self, data):
        return sum(data)


if __name__ == "__main__":
    gen_data = GenerateData()
    gen_data.run()
    gen_data.start_service()
    

    process_data = ProcessData()
    process_data.connect(gen_data.port)
    process_data.run()

    while True:
        pass

