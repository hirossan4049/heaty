import os
import time
import json
import subprocess
import psutil

CONFIG_PATH = "sample_config.json"

json_config = ""
with open(CONFIG_PATH) as f:
    json_config = f.read()

config = json.loads(json_config)

# {id: datetime}
triggerd_data = {}

def cpu_trigger(index, trigger, shell, interval):
    if not '%' in trigger:
        raise "triggerに%がセットされていません"
    # トリガーされた場合はインターバル内ではないかチェック
    if triggerd_time := triggerd_data.get(index):
        current_interval = time.time() - triggerd_time
        if current_interval > interval:
            triggerd_data.pop(index)
        else:
            # pass
            return
    cpu = psutil.cpu_percent(interval=1)
    trigger_per = int(trigger.split('%')[0])
    if cpu > trigger_per:
        triggerd_data[index] = time.time()
        subprocess.call(shell, shell=True)

def mem_trigger(index, trigger, shell, interval):
    if not '%' in trigger:
        raise "triggerに%がセットされていません"
    # トリガーされた場合はインターバル内ではないかチェック
    if triggerd_time := triggerd_data.get(index):
        current_interval = time.time() - triggerd_time
        if current_interval > interval:
            triggerd_data.pop(index)
        else:
            # pass
            return
    mem = psutil.virtual_memory()
    trigger_per = int(trigger.split('%')[0])
    if mem > trigger_per:
        triggerd_data[index] = time.time()
        subprocess.call(shell, shell=True)

def check(index, item):
    item_type = item['type']
    trigger = item['trigger']
    shell = item['shell']
    interval = item['interval']
    print(item_type, trigger, shell, interval)
    if item_type == 'cpu':
        cpu_trigger(index, trigger, shell, interval)
    if item_type == 'mem':
        mem_trigger(index, trigger, shell, interval)
    else:
        "；；"
    


def loop():
    for index, item in enumerate(config):
        check(index, item)

for _ in range(100):
    loop()
    time.sleep(1)
