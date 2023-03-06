import os
from pathlib import Path

from typing import Union


class RipFileHelper:
    pid_filename = "ddnsdaemon.pid"
    linux_tempdir = "/tmp"

    @staticmethod
    def file_exists(path: str) -> Union[bool, None]:
        try:
            the_file = Path(path)
            res = the_file.is_file()
            return res
        except Exception as exc:
            return None

    @staticmethod
    def read_pid_file(path: str) -> Union[int, None]:
        try:
            with open(file=path, mode="r") as pid_f:
                res = int(pid_f.readline())
                print("PID: " + str(res))
                return res
        except Exception as exc:
            print("Invalid pidfile with error " + str(exc))
            return None

    @staticmethod
    def delete_file(path: str) -> Union[None, bool]:
        try:
            os.remove(path)
            return True
        except Exception as exc:
            print("error deleting file " + str(exc))
            return None

    @staticmethod
    def new_pid_file(pid_file: str, pid: int):
        try:
            with open(file=pid_file, mode="w") as pid_f:
                res = int(pid_f.write(str(pid)))
                print("PID: " + str(res))
                return res
        except Exception as exc:
            print("Invalid pidfile with error " + str(exc))
            return None
