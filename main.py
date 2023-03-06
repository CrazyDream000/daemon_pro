import configparser
import os
from http import HTTPStatus

from flask import Flask, json
from flask_restful import Resource, Api

import RipConf
import RipNetInterfaces
import RipProcHelper
import RipRepack
import RipWelcome
import RipFileHelper

rn = RipNetInterfaces.RipNetInterfaces
rr = RipRepack.RipRequest
props_conf = configparser.ConfigParser()
conf_file_name = "config.properties"
app = Flask(__name__)
RipConf.RipConf.load_app_conf(props_conf=props_conf, conf_file_name=conf_file_name)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_interfaces():
    int_list = rn.list_interfaces()
    rn.descr_interfaces(int_list)


class Watchdog(Resource):
    @staticmethod
    def get():
        try:
            return {"my_pid": os.getpid()}, HTTPStatus.OK
        except Exception as exc:
            return {"error": "error retriving the pid " + str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR


class CronJob(Resource):
    @staticmethod
    def get():
        print("cronjob called")
        ip_and_interfaces_conf = {}
        # get local inet configuration
        int_list = rn.list_interfaces()
        gws_list = rn.list_gateways()
        internal_interfaces = rn.descr_interfaces(int_list)
        internal_gateways = rn.descr_gateways(gws_list)
        try:
            my_ext_ip = rr.retrieve_my_ip(props_conf['ddns_server']['ip_retrieval_url'])
            ip_and_interfaces_conf["ext_ip"] = my_ext_ip.exploded if my_ext_ip is not None else None
        except Exception as exc:
            msg = "Error retrieving public ip " + str(exc)
            print(msg)
            ip_and_interfaces_conf["ext_ip"] = None
            ip_and_interfaces_conf["ext_ip_error"] = msg
        # print("Internal interfaces " + str(internal_interfaces))
        # print("Internal gateways " + str(internal_gateways))
        ip_and_interfaces_conf["interfaces"] = internal_interfaces
        ip_and_interfaces_conf["gateways"] = internal_gateways
        # print(my_ext_ip.exploded)
        ip_and_interfaces_conf["request-type"] = "update-machine-registration"
        ip_and_interfaces_conf["uuid"] = props_conf['ddns_server']['uuid']
        ip_and_interfaces_conf["nickname"] = props_conf['ddns_server']['nickname']
        ip_and_interfaces_conf["platform"] = rn.get_platform_details()
        ip_and_interfaces_conf["java"] = rn.get_default_java()
        ip_and_interfaces_conf["load"] = rn.get_sys_load()
        print("PLATFORM " + json.dumps(ip_and_interfaces_conf["platform"]))
        print("JAVA " + json.dumps(ip_and_interfaces_conf["java"]))
        print("LOAD \n" + json.dumps(ip_and_interfaces_conf["load"]) + "\n")
        res = None
        try:
            res = RipRepack.RipRequest.json_hmac_request(
                destination_server_url=props_conf['ddns_server']['delivery_url'],
                api_user=props_conf['keys']['api_user'],
                api_key=props_conf['keys']['dns_key'],
                api_key_number=props_conf['keys']['api_key_number'],
                dictionary_payload=ip_and_interfaces_conf,
                submit_method="POST")
            print(res.text)
            j_data = json.loads(res.text)
            return j_data, res.status_code
        except Exception as exc:
            print("Error submitting data: " + str(exc))
            if res is not None:
                j_data = json.loads(res.text)
                return j_data, res.status_code
            else:
                return {}, HTTPStatus.INTERNAL_SERVER_ERROR


api = Api(app)
api.add_resource(RipWelcome.RipWelcome, '/')
api.add_resource(CronJob, '/cronjob')
api.add_resource(Watchdog, '/watchdog')

if __name__ == "__main__":
    RipProcHelper.RipProcHelper.delete_invalid_pid_file_or_terminate(
        "http://localhost:" + props_conf['app_debug']['bind_port'] + "/watchdog")
    my_pid = os.getpid()
    print("My pid is " + str(my_pid))
    pid_path = RipProcHelper.RipProcHelper.get_pid_file_path_by_os()
    RipFileHelper.RipFileHelper.new_pid_file(pid_file=pid_path, pid=my_pid)
    print("Mode " + props_conf['app']['debug'])
    print(props_conf['ddns_server']['nickname'])
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
