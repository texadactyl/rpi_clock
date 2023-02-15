from RaspberryPiVcgencmd import Vcgencmd

vcgencmd = Vcgencmd()
ver = vcgencmd.get_version()
print(f"RaspberryPiVcgencmd version: {ver}\n")
cpu_temp = vcgencmd.get_cpu_temp()
print(f"CPU temperature: {cpu_temp} C")
split = vcgencmd.get_ram_split()
arm_mem = split["arm"]
gpu_mem = split["gpu"]
print(f"ARM mem: {arm_mem}, GPU mem {gpu_mem}")
core_volts = vcgencmd.measure_volts("core")
print(f"Core volts: {core_volts} V")
arm_clock = float(vcgencmd.measure_clock("arm")) / 1000000.0
print(f"ARM clock: {arm_clock:.0f} MHz")
core_clock = float(vcgencmd.measure_clock("core")) / 1000000.0
print(f"Core clock: {core_clock:.0f} MHz")
