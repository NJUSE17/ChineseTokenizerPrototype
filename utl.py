import time

previous = time.time()


def count(label="no label", print_to_console=True):
    current = time.time()
    global previous
    diff = current - previous
    previous = current
    if print_to_console:
        print("#timer# %s：%.7fs" % (label, diff))
    return diff


def log(msg, level='DEBUG'):
    level = level.upper()
    if level == 'DEBUG':
        print(msg)
    elif level == 'INFO':
        print("\033[1;32m%s\033[0m" % msg)
    elif level == 'WARN':
        print("\033[1;31m%s\033[0m" % msg)


def info(msg):
    log(msg, level='INFO')


def warn(msg):
    log(msg, level='WARN')


conf = {
    "mongo-ip": None
}
