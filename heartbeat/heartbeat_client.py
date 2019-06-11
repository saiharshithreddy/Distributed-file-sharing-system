
from __future__ import print_function
import logging

import grpc

import heartbeat_pb2
import heartbeat_pb2_grpc
import sys
sys.path.append('../')
import time

from config.config import server_config
from util.utility import getMyIp
class HeartBeatClient():
    def __init__(self, target, stat, index):
        self.ip = getMyIp()
        self.response = {}
        self.target = target
        self.stat = stat
        self.index = index

    def run(self):
        while True:
            channel = grpc.insecure_channel(self.target+ ':' + str(server_config.get('port')))
            stub = heartbeat_pb2_grpc.HearBeatStub(channel)
            response = stub.getStatus(heartbeat_pb2.HeartBeatRequest(ip=self.ip, leader=False))
            self.response['cpu_usage'] = response.cpu_usage
            self.response['mem_usage'] = response.used_mem
            self.stat[self.index] = self.response
            print("Status from server received. Server's response is: {}".format(response))
            time.sleep(2)
