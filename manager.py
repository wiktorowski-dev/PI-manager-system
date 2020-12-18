import subprocess
import psutil
import os


class Manager(object):
    def __init__(self):
        super(Manager, self).__init__()

    @staticmethod
    def __load_processes():
        with open('paths.txt') as file:
            file = file.read()

        data = file.split('\n')
        data = [{'unique_name': x, 'path': y} for x, y in (z.split(',') for z in data)]
        return data
