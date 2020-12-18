import subprocess
import psutil
import os


class Manager(object):
    def __init__(self):
        super(Manager, self).__init__()
        data = self.__initialize_processes()

    def __initialize_processes(self):
        data = self.__load_processes()
        data = [self.__run_process(x) for x in data]
        return data

    @staticmethod
    def __load_processes():
        with open('paths.txt') as file:
            file = file.read()

        data = file.split('\n')
        data = [{'unique_name': x, 'path': y} for x, y in (z.split(',') for z in data)]
        return data

    @staticmethod
    def __run_process(d):
        path = d['path']
        process = subprocess.Popen(['python', path])
        d['process_id'] = process.pid
        return d
