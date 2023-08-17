'''
python usage. text-based.
'''
import time
import psutil
import os

def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
def display(cpu,mem,sw_mem,bar=45):
        cpu_percentage = (cpu / 100.0)
        cpu_bars = "█" * int(cpu_percentage * bar) + "-" * (bar - int(cpu_percentage * bar))
        
        mem_percentage = (mem / 100.0)
        mem_bars = "█" * int(mem_percentage * bar) + "-" * (bar - int(mem_percentage * bar))
        
        print(f"\rCPU usage: |{cpu_bars}| {cpu:.2f}% || ", end="")
        print(f"Virual MEMORY usage: |{mem_bars}| {mem:.2f}% ", end="\r")

        time.sleep(0.6)
    
def run(bar = 45):
    while True:
        try:
            display(psutil.cpu_percent(),psutil.virtual_memory().percent,psutil.swap_memory().percent,45)
        except KeyboardInterrupt:
            break