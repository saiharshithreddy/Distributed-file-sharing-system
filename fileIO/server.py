from concurrent import futures
import os
import sys
import time
import logging
import grpc
import payload_pb2
import payload_pb2_grpc
import redis

import sys
sys.path.append('../')

from config.config import server_config

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
DEBUG = True

class FileService(payload_pb2_grpc.RouteServiceServicer):

    def openDB(self):
        r = redis.Redis(
            host='localhost',
            port=6379)

        return r

    def store_data(self, id, data):
        r = self.openDB()
        r.set(id, data)
        if DEBUG:
            print "Inside store data. Data stored with id : {} successfully".format(id)

    def get_data(self, id):
        r = self.openDB()
        data = r.get(id)
        if DEBUG:
            print "Inside get data. Data is : {}".format(id)
        return data

    def is_data_available(self, id):
        r = self.openDB()
        if r.get(id):
            return True
        else:
            return False

    def request(self, request, context):
        if DEBUG:
            print("Request recieved from client. Message is : {}".format(request))
        if self.is_data_available(request.id):
            data = self.get_data(request.id)
            return payload_pb2.Route(payload = data)
        else:
            self.store_data(request.id, request.payload)
            return payload_pb2.Route(
                payload= "Stored successfully!!"
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payload_pb2_grpc.add_RouteServiceServicer_to_server(FileService(), server)
    server.add_insecure_port(server_config.get('host')+ ':' + str(server_config.get('port')))
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
#
# if __name__ == '__main__':
#     logging.basicConfig()
#     serve()
