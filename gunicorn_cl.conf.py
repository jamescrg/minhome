

# reload app when code changes
reload = True

# Redirect stdout/stderr to specified file in errorlog
# capture_output = True

# set log file locations
accesslog = "-"
errorlog = "-"

# set log level
loglevel = 'debug'

# number of subprocesses
workers = 3

# location of socket file for nginx server
bind = "0.0.0.0:8000"

# ssl config
keyfile = "/home/james/.ssl/mh/dev_minhome_app.key"
certfile = "/home/james/.ssl/mh/dev_minhome_app.crt"
