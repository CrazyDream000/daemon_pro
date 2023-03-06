# ddnsdaemon

A simple python script that gathers data from the clients on which it is installed for monitoring purposes

# Crontab

## install the daemon (short procedure)

* clone the project `git clone https://github.com/takamaka-dev/ddnsdaemon.git`
* enter the project directory `cd ddnsaemon`
* setup the virtual env `python3.9 -m venv /home/ddns/ddnsdaemon/6FeetUnder`
* activate the env
* install the required packages:
  * `pip install wheel`
  * `pip install netifaces psutil`
  * `pip install requests flask_restful http configparser waitress`
* Call `python main.py` The first call will fail by creating stubs of the configuration files
* update the `*.properties` files with the correct settings
* Call `python main.py` to run the server in foregroud

## run service-like

Assuming to you have downloaded the daemon in the following path `/home/ddns/ddnsdaemon` and the virtual env with name `6FeetUnder` inside the daemon folder


```bash
crontab -e
```

The call with execution every 5 minutes:

```crontab
*/5 * * * * cd /home/ddns/ddnsdaemon && screen -d -m /home/ddns/ddnsdaemon/6FeetUnder/bin/python main.py
```

## call update

The ddnsdaemon must be called periodically to collect data from the machine on which it is installed. This is a simple
example of a timed call that takes advantage of the crontab daemon.

I create a file with the curl call to the update route.

```bash
#!/bin/bash
curl -X GET 'http://localhost:13131/cronjob'
```
Assuming to have created the file with name `call.sh` in the path `/home/ddns/call.sh` I proceed to assign it the execution permissions:

```bash
chmod 755 /home/ddns/call.sh
```

To finish I set the crontab call with the command:

```bash
crontab -e
```

The call with execution every minute:

```crontab
* * * * * /home/ddns/call.sh
```

# Install the daemon step-by-step

## requirements

To be able to use this procedure, it is necessary to have a system-wide installation:
* the `crond` daemon
* the `screen` package

### screen

```bash
yum install screen
```

### python

```bash
sudo dnf install python3.9
```

### Git

```bash
sudo dnf install git
```

### crond

```bash
sudo dnf update
sudo dnf install crontabs
```

#### crond FEDORA
```bash
dnf install cronie cronie-anacron
```

#### verify cron

```bash
sudo systemctl start crond.service
sudo systemctl enable crond.service
```
### Test installed daemon:

```bash
sudo systemctl status crond.service
```

#### result

```
● crond.service - Command Scheduler
     Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2021-09-02 17:17:58 CEST; 6 days ago
   Main PID: 1623299 (crond)
      Tasks: 1 (limit: 38304)
     Memory: 2.1M
        CPU: 4min 53.520s
     CGroup: /system.slice/crond.service
             └─1623299 /usr/sbin/crond -n

set 09 12:01:01 my-server CROND[2177336]: (root) CMDEND (run-parts /etc/cron.hourly)
set 09 13:01:01 my-server CROND[2180537]: (root) CMD (run-parts /etc/cron.hourly)
set 09 13:01:01 my-server CROND[2180535]: (root) CMDEND (run-parts /etc/cron.hourly)
set 09 14:01:01 my-server CROND[2183754]: (root) CMD (run-parts /etc/cron.hourly)
set 09 14:01:01 my-server CROND[2183752]: (root) CMDEND (run-parts /etc/cron.hourly)
set 09 15:01:01 my-server CROND[2186925]: (root) CMD (run-parts /etc/cron.hourly)
set 09 15:01:01 my-server CROND[2186923]: (root) CMDEND (run-parts /etc/cron.hourly)
set 09 16:01:01 my-server CROND[2200738]: (root) CMD (run-parts /etc/cron.hourly)
set 09 16:01:01 my-server CROND[2200736]: (root) CMDEND (run-parts /etc/cron.hourly)
set 09 16:48:01 my-server crond[1623299]: (ddns) RELOAD (/var/spool/cron/ddns)

```


## login as root

After connecting to the server with the root user, create a user with standard permissions.

```bash
adduser ddns
su ddns
```

## Using the newly created ddns user

From the user's home, clone the latest version of the ddns daemon.

```bash
# go to home
cd
# clone the last version of the software
git clone https://github.com/takamaka-dev/ddnsdaemon.git
# go to ddnsdaemon
cd ddnsdaemon
# create virtualenv
python3.9 -m venv /home/ddns/ddnsdaemon/6FeetUnder
# enable virtualenv
source 6FeetUnder/bin/activate
# upgrade pip
pip install --upgrade pip
# install the required dependencies
pip install wheel
pip install flask_restful requests configparser waitress 
pip install netifaces psutil

```

## daemon setup

Edit the daemon config file:

```bash
nano /home/ddns/ddnsdaemon/config.properties
```

To save `CTRL + X` and than `Y`

## test the daemon startup

```bash
# enter the project folder
cd /home/ddns/ddnsdaemon
# load the virtualenv
source 6FeetUnder/bin/activate
# run the daemon
python main.py
```

If all dependencies are met, the server will start in debug mode.

```
Pid File is /tmp/ddnsdaemon.pid file exists: True
PID: 2201431
Pid file value is: 2201431
Server is not running with expected configuration HTTPConnectionPool(host='localhost', port=13131): Max retries exceeded with url: /watchdog (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fbcb9a71880>: Failed to establish a new connection: [Errno 111] Connection refused'))
pid exists and running False
expired pid file successfully deleted
My pid is 2201504
I'm launcher running on: Linux
APPDATA: None
PID: 7
Mode True
lion_67
debug
 * Serving Flask app 'main' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://192.168.0.194:13131/ (Press CTRL+C to quit)
```

## first daemon call

We now make the first call to the daemon and if everything is correctly configured, we get the following response from `curl.

### request

```bash
curl -X GET http://localhost:13131/cronjob
```

### response

```json
{"result": "record updated", "request": "update-machine-registration"}
```

## switch to production mode

We stop the daemon with `CTRL + C` in the shell where it was launched.

We edit the `config.properties` file to switch from the test server to the production server.

```bash
nano /home/ddns/ddnsdaemon/config.properties
```

Edit the debug line in the `[app]` section as follows

### old value

```properties
[app]
debug = True
```

### new value

```properties
[app]
debug = False
```

To save `CTRL + X` and than `Y`

## the "daemon" part

We configure `crontab` to restart the server in the event of a malfunction or reboot.

It is also possible to create a service for `systemctl` but it is beyond the scope of this guide and would only apply to distros that use this service boot mode.

Assuming to you have downloaded the daemon in the following path `/home/ddns/ddnsdaemon` and the virtual env with name `6FeetUnder` inside the daemon folder

```bash
crontab -e
```

The call with execution every 5 minutes:

```crontab
*/5 * * * * cd /home/ddns/ddnsdaemon && screen -d -m /home/ddns/ddnsdaemon/6FeetUnder/bin/python main.py
```



## the "update" part
```bash
nano /home/ddns/call.sh
```

We insert the following command in the file.

```bash
#!/bin/bash
curl -X GET 'http://localhost:13131/cronjob'
```

To save `CTRL + X` and than `Y`

The ddns daemon must be called periodically to collect data from the machine on which it is installed. This is a simple
example of a timed call that takes advantage of the crontab daemon.

Assuming to have created the file with name `call.sh` in the path `/home/ddns/call.sh` I proceed to assign it the execution permissions:

```bash
chmod 755 /home/ddns/call.sh
```

To finish I set the crontab call with the command:

```bash
crontab -e
```

The call with execution every minute:

```crontab
* * * * * /home/ddns/call.sh
```

### verify the crontab

Crontab log

```bash
cat /var/log/cron
```

### verify if the daemon server is running

Login as `ddns`

```bash
screen -ls
```

#### result

```
There is a screen on:
        2203249..my-server  (Detached)
1 Socket in /run/screen/S-ddns.
```
