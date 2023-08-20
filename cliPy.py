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
from typing import *

globals()["arg?"] = False
try:
            sys.argv[1]
            globals()["arg?"] = True
except: pass

#custom libraries
import Usage
from config import *
class python_commandprompt:
    def __init__(self) -> None:
        self.platform = sys.platform
        self.args = []
        self.cpath = os.getcwd().lower()
        self.init()
        
    def remove_inside_quote(self, string: str=None):
        return string[1:-1]
    
    def get_arg(self,cmd: str) -> str:
        if cmd:
            return cmd.split(" ")[1].lower()
        else: return ""

    def get_listarg(self,cmd: str) -> list[str]: 
        if cmd:
            return re.findall(r'"[^"\']*"|\'[^\']*\'|\S+', cmd)[1:]
        else: return []

    def get_running_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            processes.append((proc.info['pid'], proc.info['name']))
        return processes
    
    def encrypt(self, a: str=None, passphrase: str=None):
        if not passphrase:
            return "Passphrase is required."

        if not a:
            return "Input string is required."

        passint = sum(ord(char) for char in passphrase)
        
        ans = ""
        a1 = ""
        for chr in a:
            if chr == " ":
                a1 += "-/"
            else:
                a1 += str(ord(chr)+passint) + "/"
        
        return a1.encode().hex()

    def decrypt(self, a: str=None, passphrase: str=None):
        if not passphrase:
            return "Passphrase is required."

        if not a:
            return "Input string is required."
        
        passint = sum(ord(char) for char in passphrase)

        ans = ""
        b = bytes.fromhex(a).decode("utf-8")
        formatted = b.split("/")

        for obj in formatted:
            if obj == "-":
                    ans += " "
            elif obj == "": pass
            else:
                ans += chr(int(obj)-passint)
        return ans
    
    def init(self):
        try:
            print(ASCII_ART.art)
            while True:
                cmd = ' '.join(sys.argv[1:]) or input(f"{Fore.BLUE}{self.cpath}{Fore.WHITE} | cmd#>")
                
                if cmd == "shutdown":
                    if self.platform == "win32":
                        os.system("shutdown /s /t 0")
                    elif self.self.platform == "darwin" or self.platform == "linux":
                        os.system("sudo poweroff")

                elif cmd.startswith("chdir") or cmd.startswith("cd"):
                    if ":" in cmd:
                        try:print(self.get_arg(cmd)); self.args.append(self.get_arg(cmd))
                        except: print("No subdirectory/disk name to locate"); continue

                        try:
                            os.chdir(self.args[0])
                            self.cpath = os.getcwd().lower()
                        except FileNotFoundError:
                            print("Subdirectory / Disk not found")
                        except Exception as e:
                            print("e = ", e)
                        self.args = []
                    else:
                        try:self.args.append(self.get_arg(cmd))
                        except: print("No subdirectory/disk name to locate"); continue

                        try:
                            if self.args[0] == "..":
                                self.cpath = os.path.dirname(self.cpath)
                                os.chdir(self.cpath)
                            else:
                                os.chdir(path.join(self.cpath, self.args[0]))
                                self.cpath = os.getcwd().lower()
                        except FileNotFoundError:
                            print("Subdirectory / Disk not found")
                        self.args = []

                elif cmd.startswith(("exit", "logoff")):
                    break

                elif cmd.startswith(("command","cmd")):
                    try:
                        self.args.append(cmd.split("command ")[1])
                    except:
                        try:self.args.append(cmd.split("cmd ")[1])
                        except: continue

                    os.system(self.args.pop(0))
                elif cmd.startswith("encrypt"):
                    argd = self.get_listarg(cmd)
                    try : text, passphrase = argd[0], argd[1]
                    except IndexError: print("Seems like you forgot something, the syntax of the command is: encrypt 'text' passphrase"); continue
                    if re.match(r'^["\'].*["\']$', text): text = self.remove_inside_quote(text)
                    if re.match(r'^["\'].*["\']$', passphrase): passphrase = self.remove_inside_quote(passphrase)
                    print(self.encrypt(text, passphrase))

                elif cmd.startswith("decrypt"):
                    argd = self.get_listarg(cmd)
                    try : text, passphrase = argd[0], argd[1]
                    except IndexError: print("Seems like you forgot something, the syntax of the command is: decrypt 'encrypted text' passphrase"); continue
                    if re.match(r'^["\'].*["\']$', text): text = self.remove_inside_quote(text)
                    if re.match(r'^["\'].*["\']$', passphrase): passphrase = self.remove_inside_quote(passphrase)
                    print(self.decrypt(text, passphrase))

                elif cmd.startswith("pyexec"):
                    try:
                        self.args.append(self.get_arg(cmd))
                    except:
                        print("No code to run.")
                        continue
                    if self.args[0] == "exit()":
                        break
                    try:
                        exec(self.args.pop(0))
                    except:
                        print(Fore.RED)
                        traceback.print_exc()
                        print(Fore.WHITE)

                elif cmd.startswith(("pytaskmgr", "ptask", "python-taskmgr")):
                    try:
                        self.args.append(self.get_arg(cmd))
                        running_processes = self.get_running_processes()
                        a = []
                        for i in range(0, len(running_processes)):
                            p = running_processes[i]
                            if p[1].lower().startswith(self.args[0]):
                                a.append(f"PID: {p[0]}, Name: {p[1]}")
                        if not a: print(f"There's no process with the name of {self.args.pop(0)}")
                        else:
                            for p in a:
                                print(p)
                    except IndexError:
                        running_processes = self.get_running_processes()
                        
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
                elif cmd == "netstat":
                        conns = psutil.net_connections()
                        
                        for i in range(0,len(conns),2):
                            local1 = conns[i].laddr
                            local2 = conns[i+1].laddr if i+1 < len(conns) else None
                            radd1  = conns[i].raddr
                            radd2  = conns[i+1].raddr if i+1 < len(conns) else None
                            stat1  = conns[i].status
                            stat2  = conns[i+1].status if i+1 < len(conns) else None
                            msg1 = f"Local Address: {local1.ip}:{local1.port}"
                            msg2 = f"Local Address: {local2.ip}:{local2.port}" if local2 else ''
                            msg3 = f"Foreign Address: {radd1.ip}:{radd1.port}" if radd1 else ''
                            msg4 = f"Foreign Address: {radd2.ip}:{radd2.port}" if radd2 else ''
                            msg5 = f"Status: {stat1}"
                            msg6 = f"Status: {stat2}" if stat2 else ''
                            a = " "*(50 - len(msg1))
                            b = " "*(50 - len(msg3)) if msg3 != None and msg4 != None else None    
                            c = " "*(50 - len(msg5))
                            if msg2:
                                print(f"{msg1}{a}{msg2}")
                                print(f"{msg3}{b}{msg4}") if radd1 or radd2 else print()
                                print(f"{msg5}{c}{msg6}")
                                print("-"*100)
                            else:
                                print(f"{msg1}")
                                print(f"{msg3}")
                                print(f"{msg5}")
                                print("-"*100)

                elif cmd == "clear":
                    os.system("cls") if self.platform == "win32" else os.system("clear")

                elif re.match("^[a-zA-Z]+", cmd) and self.platform == "win32" and re.search(r":$", cmd):
                    try:
                        os.chdir(cmd[0:2] + "\\")
                        self.cpath = cmd[0:2] + "\\"
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


python_commandprompt()
