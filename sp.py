import subprocess as sp
import time 


out1 = sp.check_output(["vcgencmd", "measure_temp"])
print(out1)

out2 = sp.check_output(["vcgencmd", "measure_temp"]).decode()
print(out2)

out3 = sp.check_output(["vcgencmd", "measure_temp"]).decode().split("=")[1]
print(out3)

out4 = sp.check_output(["vcgencmd", "measure_temp"]).decode().split("=")[1].split("'")[0]
print(out4)
