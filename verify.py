import filecmp
import sys

if (len(sys.argv) > 2):
 print "Error: Wrong syntax - Correct usage : (python verify.py [-ip])"
 sys.exit()
arglist = sys.argv
if (len(arglist)==2) and not(arglist[1] == '-ip'):
 print "Error: Wrong syntax - Correct usage : (python verify.py [-ip])"
 sys.exit()

if (len(arglist)==2) and (arglist[1] == '-ip'):
 f_h = open("log_g.txt",'r')
 for line in f_h:
  if line.startswith("sim_CPI"):
   CPI_G = float(line.split()[1])
 f_h.close()
 f_h = open("log.txt",'r')
 for line in f_h:
  if line.startswith("sim_CPI"):
   CPI = float(line.split()[1])
 if (CPI <= CPI_G):
  print "\nProcessor passed performance test"
 else:
  print "\nProcessor failed performance test"

if (filecmp.cmp("regl_g.txt","regl.txt")):
 print "\nProcessor passed functional test\n"
else:
 print "\nProcessor failed functional test\n"


  
