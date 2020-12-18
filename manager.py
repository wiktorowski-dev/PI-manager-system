import subprocess
import psutil
import os


class Manager(object):
    def __init__(self):
        super(Manager, self).__init__()
        data = self.__initialize_processes()
        self.__manage_continuously_work(data)

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
        # Unix python declaration
        process = subprocess.Popen(['python3', path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        d['process_id'] = process.pid
        return d

    def __manage_continuously_work(self, data):
        while True:
            process_down = False
            actual_working_processes = psutil.pids()
            for i in range(len(data)):
                if data[i]['process_id'] in actual_working_processes:
                    try:
                        process_path = psutil.Process(data[i]['process_id']).cmdline()[-1]
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
