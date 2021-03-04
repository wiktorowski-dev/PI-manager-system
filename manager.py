import subprocess
import psutil
import os
import time
from common.logs import *


class Manager(Logs):
    def __init__(self):
        super(Manager, self).__init__()
        data = self.__initialize_processes()
        try:
            self.__manage_continuously_work(data)
        except Exception as e:
            self.log_it(str(e), 'e')
            raise Exception(str(e))

    def __initialize_processes(self):
        self.log_it('Initializing a script')
        data = self.__load_processes()
        data = [self.__run_process(x) for x in data]
        return data

    def __load_processes(self,):
        with open('paths.txt') as file:
            file = file.read()
        self.log_it('Splitting elements from file')
        data = file.split('\n')
        split_data = [z.split(',') for z in data]
        data_out = []
        for elem in split_data:
            if len(elem) == 3:
                data = [{'unique_name': x, 'path': c, 'script_start': y} for x, y, c in [elem]][0]
            elif len(elem) == 4:
                data = [{'unique_name': x, 'path': c, 'script_start': y, 'script_argument': q} for x, y, c, q in [elem]][0]
            else:
                print('Valid input size')
                return None
            data_out.append(data)

        return data_out

    def __run_process(self, d):
        path = d['path']
        p_out = self.__move_to_the_folder(path)
        script_start = d['script_start']
        # Unix python declaration
        run_process = [script_start, path]
        self.log_it(f'Running a process: path: {path}')
        if len(d.keys()) == 4:
            run_process.append(d['script_argument'])

        process = subprocess.Popen(run_process)
        self.log_it('Process started')
        d['process_id'] = process.pid
        return d

    @staticmethod
    def __move_to_the_folder(path):
        path_to_move = os.path.split(path)
        os.chdir(path_to_move[0])
        return path_to_move[-1]

    def __manage_continuously_work(self, data):
        self.log_it('Continuous script support starting')
        while True:
            time.sleep(5)
            process_down = False
            actual_working_processes = psutil.pids()
            for i in range(len(data)):
                if data[i]['process_id'] in actual_working_processes:
                    try:
                        process_path = psutil.Process(data[i]['process_id']).cmdline()[-1]
                        #print(process_path)
                        if data[i]['path'] == process_path:
                            continue
                        else:
                            process_down = True

                    except:
                        process_down = True

                else:
                    process_down = True

                if process_down:
                    mpr = self.__is_missed_process_running(data[i])
                    if mpr:
                        data[i]['process_id'] = mpr
                    else:
                        data[i] = self.__run_process(data[i])

    @staticmethod
    def __is_missed_process_running(elem):
        actual_working_processes = psutil.pids()
        stacked_data = []
        for p_id in actual_working_processes:
            try:
                d = [p_id, psutil.Process(p_id).cmdline()]
                stacked_data.append(d)
            except:
                pass

        paths = [c for c in (y for y in (x[-1] for x in (z for z in stacked_data)) if len(y) != 0)]
        paths2 = []
        for e in paths:
            paths2.extend(e)
        paths = [x for x in paths2 if os.path.isfile(x)]
        if not elem['path'] in paths:
            return False

        else:
            another_id = [x[0] for x in stacked_data if elem['path'] in x[-1]][0]
            return another_id


if __name__ == '__main__':
    Manager()
