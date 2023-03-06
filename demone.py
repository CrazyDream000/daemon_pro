import daemon
import configparser
from flask import Flask, json

import RipConf

props_conf = configparser.ConfigParser()
conf_file_name = "config.properties"
app = Flask(__name__)
RipConf.RipConf.load_app_conf(props_conf=props_conf, conf_file_name=conf_file_name)



def main():
    print("Mode " + props_conf['app']['debug'])
    if props_conf['app'].getboolean('debug'):
        print("debug")
        app.run(props_conf['app_debug']['bind_address'], int(props_conf['app_debug']['bind_port']),
                props_conf['app_debug'].getboolean('debug'))
    else:
        from waitress import serve

        serve(
            app,
            host=props_conf['app']['bind_address'],
            port=props_conf['app']['bind_port'])


with daemon.DaemonContext():
    main()