import os
import getpass

unit_file_name = "python_demo_service.service"
py_serv_file = "python_demo_service.py"
print("get user home")
user_home = os.getenv("HOME")
print("user home " + str(user_home))
# ~/.config/systemd/user/
user_config_dir_base = ".config"
user_systd_in_config = "systemd"
user_systd_user_d = "user"
path_by_levels = [user_config_dir_base, user_systd_in_config, user_systd_user_d]
# l_conf = os.path.join(user_home, user_config_dir_base)
# print("test systd path.... " + str(l_conf))
# is_l_conf = os.path.exists(l_conf)
# print("lconf exists " + str(is_l_conf))
cur_path = user_home
i = 0
while i < len(path_by_levels):
    cur_path = os.path.join(cur_path, path_by_levels[i])
    # print("test if curpath exists " + str(cur_path))
    exists_cur_path = os.path.exists(cur_path)
    if not exists_cur_path:
        print("creating cur path " + str(cur_path))
        os.makedirs(cur_path)
    else:
        print("cur path exists " + str(cur_path))
    i = i + 1
user_service_dir = cur_path
installer_path = __file__[:-len(os.path.basename(__file__))]
print('current script file path:    ', __file__)
print("installer path " + str(installer_path))
unit_file_path = os.path.join(installer_path, unit_file_name)
py_file_path = os.path.join(installer_path, py_serv_file)
print("unit file path " + str(unit_file_path))
service_dest_file = os.path.join(user_service_dir, unit_file_name)
my_py = os.path.join(installer_path, "6FeetUnder/bin/python")
print("env exists " + str(os.path.exists(my_py)))
with open(unit_file_path, 'r') as f:
    text = f.read()
    text = text.replace("§§§pyplaceholder§§§", str(my_py))
    text = text.replace("$$$serviceplaceholder§§§", str(py_file_path))
    print(getpass.getuser())
    text = text.replace("$$$cur_user_replacement$$$", str(getpass.getuser()) )
    print(str(service_dest_file))
    with open(service_dest_file, "w+") as service_file:
        service_file.write(text)
