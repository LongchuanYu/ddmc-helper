import time
def log_print(msg):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' ' + msg)


if __name__ == '__main__':
    log_print('hello')
