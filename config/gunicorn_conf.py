import multiprocessing


loglevel = 'info'
errorlog = "-"
accesslog = "-"

bind = '0.0.0.0:5000'

workers = 1 #multiprocessing.cpu_count()

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True
