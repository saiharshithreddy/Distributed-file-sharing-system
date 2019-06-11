import sys
sys.path.append('../')
import fileIO.server as super_server
import heartbeat.heartbeat_client as hb_client
import threading
from config.config import server_config
import grpc
import fileIO.payload_pb2 as payload_pb2
import fileIO.payload_pb2_grpc as payload_pb2_grpc
import time
from concurrent import futures


ips = ['localhost', 'ip2', 'ip3']

stat = [None]*len(ips)

for i, ip in enumerate(ips):
    hb = hb_client.HeartBeatClient(ip,stat,i)
    t = threading.Thread(target=hb.run())
    t.start()

#TODO: fix simple file service to read and write. right now just write
#TODO: implement system file logging to understand where the file is
class SimpleFileService(payload_pb2_grpc.RouteServiceServicer):
    def __init__(self):
        self.data = ""
        i = 0

    def request(self, request, context):
        self.i += 1
        self.data = request.data
        ip = self.getLeastBusyServer()
        self.sendFile(ip, self.id,self.data)

    def getLeastBusyServer(self):
        least = 0
        ip = ""
        for s in stat:
            if s.cpu_usage < least:
                ip = s.ip
                least = s.cpu_usage
        return ip

    def sendFile(ip, id, payload):
        channel = grpc.insecure_channel(ip + ':' + str(server_config.get('port')))
        stub = payload_pb2_grpc.RouteServiceStub(channel)
        response = stub.request(payload_pb2.Route(id=id, payload=payload))
        print("Status from server received. response is : {}".format(response))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payload_pb2_grpc.add_RouteServiceServicer_to_server(super_server.SimpleFileService(), server)
    server.add_insecure_port(server_config.get('host')+ ':' + str(server_config.get('port')))
    server.start()
    try:
        while True:
            time.sleep(super_server._ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

serve()