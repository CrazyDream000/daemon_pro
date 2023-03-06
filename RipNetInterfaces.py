import builtins
import copy
import json
import sys

import netifaces
import platform
import subprocess

import psutil as psutil
from psutil import cpu_percent

from RipFunCall import RipFunCall


class RipNetInterfaces:
    ListString = list[str]
    InetSystemAttr = {v: k for k, v in netifaces.address_families.items()}
    # LoadArray = [
    #     psutil.cpu_percent,
    #     psutil.virtual_memory,
    #     psutil.swap_memory,
    #     psutil.cpu_count,
    #     psutil.cpu_freq,
    #     psutil.cpu_stats,
    #     psutil.cpu_times,
    #     psutil.cpu_times_percent,
    #     psutil.disk_io_counters,
    #     (psutil.disk_usage, "/"),
    #     (psutil.disk_usage, "/mnt/linExtra"),
    #     psutil.boot_time,
    #     psutil.users,
    #     # (psutil.sensors_temperatures, False),
    #     (getattr(psutil, "sensors_temperatures"), None, {"fahrenheit": False}),
    #     # (psutil.disk_io_counters, (False, False)),
    #     # (psutil.disk_io_counters, None, {"perdisk": False, "nowrap": False}),
    #     # (psutil.disk_io_counters, True, {"nowrap": False}),
    #
    # ]

    SafeLoadArray = [
        (psutil, "cpu_percent", None, {"interval": 5, "percpu": True}),
        (psutil, "sensors_temperatures", None, {"fahrenheit": False}),
        (psutil, "virtual_memory"),
        (psutil, "swap_memory"),
        (psutil, "cpu_count", None, {"logical": True}),
        (psutil, "cpu_freq", None, {"percpu": True}),
        # (psutil, "cpu_freq", None, {"percpu": False}),
        (psutil, "cpu_stats"),
        (psutil, "cpu_times", None, {"percpu": True}),
        (psutil, "cpu_times_percent", None, {"interval": 5, "percpu": True}),
        (psutil, "disk_io_counters", None, {"perdisk": True, "nowrap": True}),
        (psutil, "disk_partitions", None, {"all": False}),  # only valid file system (skip cdrom...)
        # (psutil, "disk_usage", "/"),
        (psutil, "boot_time"),
        (psutil, "users"),
    ]

    SafeWrapPlatformArray = [
        (platform, "node"),
        (platform, "platform"),
        (platform, "platform_compiler"),
        (platform, "machine"),
        (platform, "release"),
        (platform, "architecture"),
        (platform, "java_ver"),
        (platform, "libc_ver"),
        (platform, "system"),
        (platform, "uname"),
        (platform, "mac_ver"),
        (platform, "win32_edition"),
        (platform, "win32_is_iot"),
        # (platform, "processor"), #NetBSD Only
        (platform, "win32_ver"),
    ]

    @staticmethod
    def list_interfaces() -> ListString:
        try:
            net_ifcs = netifaces.interfaces()
            # print(type(net_ifcs))
            return net_ifcs
        except Exception as exc:
            print(str(exc))
            return None

    @staticmethod
    def list_gateways() -> ListString:
        # netifaces.gateways()
        try:
            net_ifcs = netifaces.gateways()
            # print(type(net_ifcs))
            return net_ifcs
        except Exception as exc:
            print(str(exc))
            return None

    @staticmethod
    def collect_data_to_dict(interface_info):
        if interface_info is not None:
            d_res = {}
            try:
                for k in RipNetInterfaces.InetSystemAttr.keys():
                    if RipNetInterfaces.InetSystemAttr[k] in interface_info:
                        try:
                            d_res[k] = interface_info[RipNetInterfaces.InetSystemAttr[k]]

                        except Exception as exc:
                            print("error in key access " + str(exc))
            except Exception as exc:
                print(str(exc))
                return None
            return d_res
        else:
            return None

    @staticmethod
    def collect_gw_to_dict(gw_info):
        if gw_info is not None:
            d_res = {}
            print("GW INFO: " + str(gw_info))

            try:
                if "default" in gw_info.keys():
                    try:
                        d_gw = {
                            "addr": gw_info["default"][0] if gw_info["default"][0] is not None else None,
                            "interface": gw_info["default"][1] if gw_info["default"][1] is not None else None
                        }

                        d_res["gw_default"] = d_gw

                    except Exception as exc:
                        print("exception reading default gateway" + str(exc))
                        print("TEST DICT: " + str(type(gw_info["default"]) is dict))
                        if type(gw_info["default"]) is dict:
                            print("PROVIAMO DICT")
                            for key, value in gw_info["default"].items():
                                print(str(value))
                                d_res["gw_default"] = {
                                    "addr": value[0] if value[0] is not None else None,
                                    "interface": value[1] if value[1] is not None else None
                                }
                                print("IL VINCITORE E: " + str(d_res['gw_default']))

                for k in RipNetInterfaces.InetSystemAttr.keys():
                    if RipNetInterfaces.InetSystemAttr[k] in gw_info:
                        try:
                            # d_res[k] = interface_info[RipNetInterfaces.InetSystemAttr[k]]
                            print("key " + str(k))
                            print("val " + str(gw_info[RipNetInterfaces.InetSystemAttr[k]]))
                            gateways = {}
                            i = 0
                            for gw_el in gw_info[RipNetInterfaces.InetSystemAttr[k]]:
                                gateways["gw_" + str(i)] = {
                                    "addr": gw_el[0] if gw_el[0] is not None else None,
                                    "interface": gw_el[1] if gw_el[1] is not None else None,
                                    "default": gw_el[2] if gw_el[2] is not None else None,
                                }
                                i += 1
                            d_res["all_gateways"] = gateways
                        except Exception as exc:
                            print("error in key access " + str(exc))
            except Exception as exc:
                print(str(exc))
                return None
            print("THE WINNER IS " + str(d_res))
            return d_res
        else:
            return None

    @staticmethod
    def descr_interfaces(inets: ListString):
        # print(RipNetInterfaces.InetSystemAttr)
        if inets is not None:
            interf_dict = {}
            for inet in inets:
                interface_info = netifaces.ifaddresses(inet)
                print(interface_info)
                interf_dict[str(inet)] = RipNetInterfaces.collect_data_to_dict(interface_info)
            return interf_dict

    @staticmethod
    def descr_gateways(gws: ListString):
        # print(RipNetInterfaces.InetSystemAttr)
        if gws is not None:
            interf_dict = {}
            # for gw in gws:
            #     # interface_info = netifaces.ifaddresses(inet)
            #     print(gw)

            interf_dict = RipNetInterfaces.collect_gw_to_dict(gws)
            return interf_dict

    @staticmethod
    def get_platform_details() -> dict:
        res = {}
        try:
            s_w_a_p = RipFunCall.safe_wrap_fun_array_duplicate_rename(fun_arr=RipNetInterfaces.SafeWrapPlatformArray)
            print("SWAP: " + json.dumps(s_w_a_p))
            res["platform_check"] = s_w_a_p

            # res['hostname'] = platform.node()
            # res['platform'] = platform.platform()
            # res['python-compiler'] = platform.python_compiler()
            # res['machine'] = platform.machine()
            # res['release'] = platform.release()
            # res['architecture'] = platform.architecture()
            # res['java_ver'] = platform.java_ver()
            # res['libc_ver'] = platform.libc_ver()
            # res['system'] = platform.system()
            # res['uname'] = platform.uname()
            # res['mac-ver'] = platform.mac_ver()
            # res['win32-edition'] = platform.win32_edition()
            # res['win32-is-iot'] = platform.win32_is_iot()
            # res['processor'] = platform.processor()
            # res['win32-ver'] = platform.win32_ver()
        except Exception as exc:
            res["platform_check_error"] = str(exc)
        return res

    @staticmethod
    def get_default_java() -> dict:
        res = {}
        try:
            res['java'] = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode(
                sys.stdout.encoding).replace("\n", " | ")
        except Exception as exc:
            res["java_check_error"] = str(exc)
        return res

    @staticmethod
    def get_sys_load() -> dict:
        res = {}
        try:
            # f_a_r = RipFunCall.wrap_fun_array_duplicate_rename(fun_arr=RipNetInterfaces.LoadArray)

            # (psutil, "disk_partitions", None, {"all": False})
            # (psutil, "disk_usage", "/")
            disk_list = RipFunCall.safe_wrap_fun_array_duplicate_rename(
                fun_arr=[(psutil, "disk_partitions", None, {"all": False})])
            print("Disk List " + str(disk_list))
            extended_safe_list = None
            try:
                list_of_partitions = disk_list['disk_partitions!0']["result"]["disk_partitions"]
                print("LIST PART: " + json.dumps(list_of_partitions))
                part_list = []
                for partition in list_of_partitions:
                    try:
                        """
                        [
                            "/dev/sdb5",
                            "/",
                            "xfs",
                            "rw,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota",
                            255,
                            4096
                        ]
                        """
                        if "rw" in partition[3]:
                            print("RW PATH " + partition[0])
                            part_list.append((psutil, "disk_usage", partition[1]))
                    except Exception as exc:
                        print("partition read error " + str(exc))
                if len(part_list) <= 0:
                    extended_safe_list = None
                else:
                    extended_safe_list = []
                    for el in RipNetInterfaces.SafeLoadArray:
                        extended_safe_list.append(el)
                    for el in part_list:
                        extended_safe_list.append(el)
            except Exception as exc:
                print("disk detection failure " + str(exc))
            if extended_safe_list is None:
                f_a_r = RipFunCall.safe_wrap_fun_array_duplicate_rename(fun_arr=RipNetInterfaces.SafeLoadArray)
            else:
                f_a_r = RipFunCall.safe_wrap_fun_array_duplicate_rename(fun_arr=extended_safe_list)
            print("FAR: " + json.dumps(f_a_r))
            res["load_check"] = f_a_r
            # res["cpu_percent"] = psutil.cpu_percent()
            # r, e = RipFunCall.wrap_fun(psutil.cpu_percent)
            # print("R: " + str(r) + " E: " + str(e))
            # res["virtual_memory"] = psutil.virtual_memory()
            # res["swap_memory"] = psutil.swap_memory()
            # res["cpu_count"] = psutil.cpu_count()
            # res["cpu_freq"] = psutil.cpu_freq()
            # res["cpu_stats"] = psutil.cpu_stats()
            # res["cpu_times"] = psutil.cpu_times()
            # res["cpu_times_percent"] = psutil.cpu_times_percent()
            # res["disk_io_counters"] = psutil.disk_io_counters()
            # res["disk_usage"] = psutil.disk_usage("/")
            # print("DRY CALL ------------------------------")
            # # compl_call = (psutil.disk_io_counters, None, {"path": "/"})
            # # r, e = RipFunCall.wrap_fun(compl_call[0], compl_call[1:])
            # # print("R: " + str(r) + " E: " + str(e))
            # print("DRY CALL ------------------------------ END")
            # res["boot_time"] = psutil.boot_time()
            # res["users"] = psutil.users()
            # res["sensors_temperatures"] = psutil.sensors_temperatures(fahrenheit=False)
        except Exception as exc:
            res["load_check_errors"] = str(exc)
        return res
