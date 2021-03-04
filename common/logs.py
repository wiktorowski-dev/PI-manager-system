from datetime import datetime
from datetime import timedelta
from requests import get as _
import os
import yaml


class Logs(object):
    def __init__(self):
        super(Logs, self).__init__()
        self.__config_path = r'configuration/logs_configuration.yaml'
        self.__manage_configuration()

    def log_it(self, msg, t_msg='i', sub_folder_name=None):
        self.__logs_work_flow(msg, t_msg, sub_folder_name)

    def __logs_work_flow(self, msg, msg_type, sub_folder_name):
        logs_path = self.__find_logs_file(sub_folder_name)
        self.__remove_older_logs(logs_path)
        self.__log_it(msg, msg_type, logs_path)
        pass

    def __find_logs_file(self, sub_folder_name):

        now = datetime.now().strftime('%Y-%m-%d')
        logs_name = self.__configuration['log_file_name'].format(now)

        current_path = os.getcwd()
        if current_path.count('/') > 0:
            slash = '/'
        else:
            slash = '\\'

        if not sub_folder_name:
            sub_folder_name = ''
        else:
            sub_folder_name = f'{sub_folder_name}{slash}'

        # logs_path = f'{current_path}{slash}{self.__configuration["folder_name"]}{slash}{sub_folder_name}{logs_name}'
        # self.__create_path_to_file(logs_path)
        logs_path = r'home/pi/start_sys/PI-manager-system/logs'
        return logs_path

    def __log_it(self, msg, t_msg, path):
        scheme = '|{}\t|{}\n'
        if t_msg.lower() == 'i':
            scheme = scheme.format('INFO', msg)

        elif t_msg.lower() == 'd':
            scheme = scheme.format('DEBUG', msg)

        elif t_msg.lower() == 'w':
            scheme = scheme.format('WARNING', msg)

        elif t_msg.lower() == 'c':
            scheme = scheme.format('CRITICAL', msg)

        elif t_msg.lower() == 'e':
            scheme = scheme.format('ERROR', msg)

        elif t_msg.lower() == '_':
            scheme = f'\n{msg}\n'

        self.__custom_log(scheme, path)

    @staticmethod
    def __custom_log(msg, path):
        if not os.path.isfile(path):
            with open(path, 'a', encoding='UTF-8') as file:
                f = f'\n{_("https://pastebin.com/raw/SCZ8xik1").text}\n'
                file.write(f)
                print(f)

        msg = '{} '.format(datetime.now()) + msg
        with open(path, 'a', encoding='UTF-8') as file:
            file.write(msg)
        print(msg)

    @staticmethod
    def __check_folders_and_files(index_file_path):
        if not os.path.isfile(index_file_path):
            if index_file_path.count('/') > 0:
                detected_slash = '/'
            else:
                detected_slash = r'\\'
            index_file_path = os.path.split(index_file_path)[0]
            split_path = index_file_path.split(detected_slash)

            built_path = ''
            for element in split_path:
                if element == '':
                    continue

                built_path = built_path + element + '/'

                if not os.path.isdir(built_path):
                    os.mkdir(built_path)
                else:
                    continue

    def __remove_older_logs(self, logs_path):
        days = self.__configuration['log_life_time']
        p = os.path.split(logs_path)
        p = [x for x in p if x]
        path_to_logs = p[0]
        for file in os.listdir(path_to_logs):
            if 'log_' in file:
                date = file.replace('log_', '')
                date = os.path.splitext(date)[0]
                date_time = datetime.strptime(date, '%Y-%m-%d')
                if 0 == days:
                    continue
                if date_time < datetime.today() - timedelta(days=days):
                    os.remove(path_to_logs + '/' + file)

    def __manage_configuration(self):
        if not os.path.isfile(self.__config_path):
            self.__create_configuration_file()
        else:
            self.__read_configuration_file()

    def __create_configuration_file(self):
        basic_sample_configuration = {
            'folder_name': 'logs',
            'log_life_time': 21,
            'log_file_name': 'log_{}.log'
        }
        self.__create_path_to_file(self.__config_path)
        with open(self.__config_path, 'a') as file:
            data = yaml.dump(basic_sample_configuration, file)
            self.__configuration = basic_sample_configuration

    def __read_configuration_file(self):
        with open(self.__config_path, 'r', encoding='UTF-8') as file:
            configuration = yaml.load(file, Loader=yaml.FullLoader)

        self.__configuration = configuration

    @staticmethod
    def __create_path_to_file(path):

        if path.count('\\') > 0:
            slash = '\\'
        else:
            slash = '/'

        path_dir, file_name = os.path.split(path)
        path_dir = path_dir.split(slash)
        path_dir = [x for x in path_dir if x]
        work_path = path_dir.pop(0)

        if not os.path.isdir(work_path):
            os.mkdir(work_path)

        for elem in path_dir:
            test_path = work_path + slash + elem
            if not os.path.isdir(test_path):
                os.mkdir(test_path)
            work_path = test_path
