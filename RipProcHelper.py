import asyncio
import os
from pathlib import Path
import platform
from typing import Union

import requests

import RipFileHelper


class RipProcHelper:
    @staticmethod
    def check_pid_running_linux(pid: int) -> Union[None, bool]:
        try:
            os.kill(pid, 0)
            return True
        except OSError as exc:
            return False
        except Exception as exc:
            print("unexpected behaviour " + str(exc))
            print("provide watchdog route")
            exit(7)

    @staticmethod
    async def run(cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        print("Child pid is:" + str(proc.pid))

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    @staticmethod
    def get_pid_file_path_by_os():
        curr_platform = platform.system()
        win_appdata = os.getenv('APPDATA')
        pid_file_path = None
        print("I'm launcher running on: " + curr_platform)
        print("APPDATA: " + str(win_appdata))
        if curr_platform == "Windows":
            # pid_file_path = os.path.dirname(str(win_appdata)[:-len("Roaming")])
            app_data = Path(win_appdata).resolve().parent
            print("APPDATA DIR: " + str(pid_file_path))
            print("parent: " + str(app_data))
            pid_file_path = os.path.join(app_data, "Local", "Temp", RipFileHelper.RipFileHelper.pid_filename)
        elif curr_platform == "Linux":
            pid_file_path = os.path.join(RipFileHelper.RipFileHelper.linux_tempdir,
                                         RipFileHelper.RipFileHelper.pid_filename)
        return pid_file_path

    @staticmethod
    def delete_invalid_pid_file_or_terminate(watchdog_route: str = None):
        pid_file_path = RipProcHelper.get_pid_file_path_by_os()
        pid_file_exists = RipFileHelper.RipFileHelper.file_exists(pid_file_path)

        print("Pid File is " + str(pid_file_path) + " file exists: " + str(pid_file_exists))

        if pid_file_exists is None:
            print("error in file reading")
            # max 127
            exit(3)

        if pid_file_exists:
            saved_pid = RipFileHelper.RipFileHelper.read_pid_file(pid_file_path)
            print("Pid file value is: " + str(saved_pid))
            if saved_pid is None:
                print("invalid pid file")
                print("deleting pid file")
                del_pid_file = RipFileHelper.RipFileHelper.delete_file(pid_file_path)
                if del_pid_file is None:
                    print("unable to handle pid file")
                    exit(4)
                elif del_pid_file:
                    print("invalid pid file successfully deleted")
                else:
                    print("unhandled exception in file removal ")
                    exit(5)
            else:
                if watchdog_route is None:
                    pid_exists = RipProcHelper.check_pid_running_linux(saved_pid)
                else:
                    try:
                        try:
                            r = requests.get(watchdog_route)
                            w_q_res = r.json()
                            print("res " + str(w_q_res))
                            if "my_pid" in w_q_res.keys():
                                try:
                                    watchdog_pid = int(w_q_res["my_pid"])
                                    print("test valid pid " + str(watchdog_pid))
                                    if watchdog_pid == saved_pid:
                                        print("process is running with expected pid")
                                        exit(0)
                                    else:
                                        print("pid mismatch")
                                        pid_exists = False
                                except Exception as exc:
                                    print("invalid response from watchdog")
                                    pid_exists = False
                        except requests.exceptions.RequestException as e:  # This is the correct syntax
                            print("Server is not running with expected configuration " + str(e))
                            pid_exists = False
                    except Exception as exc:
                        print("error in watchdog route handling " + str(exc))
                        exit(8)
                print("pid exists and running " + str(pid_exists))
                if pid_exists:
                    print("skip execution")
                    exit(0)
                else:
                    del_pid_file = RipFileHelper.RipFileHelper.delete_file(pid_file_path)
                    if del_pid_file is None:
                        print("unable to handle pid file")
                        exit(4)
                    elif del_pid_file:
                        print("expired pid file successfully deleted")
                    else:
                        print("unhandled exception in file removal ")
                        exit(6)
