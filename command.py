'''
A normal ripoff command prompt from Windows.

But the difference is:
Supports Windows (NT), MacOS (Darwin), Linux
'''
#imports
import os, sys, psutil
from os import path
import traceback
import re

#custom libraries
import Usage
from config import *

platform = sys.platform
args = []
cpath = os.getcwd().lower()

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append((proc.info['pid'], proc.info['name']))
    return processes

globals()["arg?"] = False
try:
    sys.argv[1]
    globals()["arg?"] = True
except: pass
try:
    while True:
        cmd = ' '.join(sys.argv[1:]) or input(f"{Fore.BLUE}{cpath}{Fore.WHITE} | cmd#>")
        
        if cmd == "shutdown":
            if platform == "win32":
                os.system("shutdown /s /t 0")
            elif platform == "darwin" or platform == "linux":
                os.system("sudo poweroff")

        elif cmd.startswith("chdir") or cmd.startswith("cd"):
            if ":" in cmd:
                try:args.append(cmd.split("chdir ")[1].lower())
                except: 
                    try:args.append(cmd.split("cd ")[1].lower())
                    except: print("No directory/disk to locate"); continue

                try:
                    os.chdir(args[0])
                    cpath = os.getcwd().lower()
                except FileNotFoundError:
                    print("Subdirectory / Disk not found")
                except Exception as e:
                    print("e = ", e)
                args = []
            else:
                try:args.append(cmd.split("chdir ")[1].lower())
                except: 
                    try:args.append(cmd.split("cd ")[1].lower())
                    except: print("No directory/disk to locate"); continue

                try:
                    if args[0] == "..":
                        cpath = os.path.dirname(cpath)
                        os.chdir(cpath)
                    else:
                        os.chdir(path.join(cpath, args[0]))
                        cpath = os.getcwd().lower()
                except FileNotFoundError:
                    print("Subdirectory / Disk not found")
                args = []

        elif cmd.startswith(("exit", "logoff")):
            break

        elif cmd.startswith(("command","cmd")):
            try:
                args.append(cmd.split("command ")[1])
            except:
                try:args.append(cmd.split("cmd ")[1])
                except: continue

            os.system(args.pop(0))

        elif cmd.startswith("pyexec"):
            try:
                args.append(cmd.split("pyexec ")[1])
            except:
                print("No code to run.")
                continue
            if args[0] == "exit()":
                break
            try:
                exec(args.pop(0))
            except:
                print(Fore.RED)
                traceback.print_exc()
                print(Fore.WHITE)

        elif cmd.startswith(("pytaskmgr", "ptask", "python-taskmgr")):
            try:
                args.append(cmd.split("pytaskmgr ")[1].lower())
                running_processes = get_running_processes()
                a = []
                for i in range(0, len(running_processes)):
                    p = running_processes[i]
                    if p[1].lower().startswith(args[0]):
                        a.append(f"PID: {p[0]}, Name: {p[1]}")
                if not a: print(f"There's no process with the name of {args.pop(0)}")
                else:
                    for p in a:
                        print(p)
            except IndexError:
                running_processes = get_running_processes()
                
                for i in range(0, len(running_processes), 2):
                    p1 = running_processes[i]
                    p2 = running_processes[i+1] if i+1 < len(running_processes) else None
                    process1 = f"PID: {p1[0]}, Name: {p1[1]}"
                    a = " "*(70-len(process1))
                    if p2:
                        process2 = f"PID: {p2[0]}, Name: {p2[1]}"
                        print(f"{process1}{a}{process2}")
                    else:
                        print(f"{process1}")

        elif cmd == "clear":
            os.system("cls") if platform == "win32" else os.system("clear")

        elif re.match("^[a-zA-Z]+", cmd) and platform == "win32" and re.search(r":$", cmd):
            try:
                os.chdir(cmd[0:2] + "\\")
                cpath = cmd[0:2] + "\\"
            except FileNotFoundError:
                print("Subdirectory / Disk not found")

        elif cmd == "usage":
            Usage.run()
        else:
            os.system(cmd)
        
        sys.argv = []
        if globals()["arg?"] == True:
            break
        print()
except Exception as e:
    print(Fore.RED)
    print(f"Python \"CMD\" error:\n")
    traceback.print_exc()
    print(Fore.WHITE)
except KeyboardInterrupt:
    os._exit(0)