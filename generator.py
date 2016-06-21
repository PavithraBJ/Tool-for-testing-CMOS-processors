import sys
from random import choice
import isa
from isa import class1
from isa import class2
from isa import class3
from isa import class4
from isa import class5
from isa import class6
from isa import class7
from isa import registers
from isa import hexadigit

if (len(sys.argv) != 3):
 print "Error: Wrong syntax - Correct usage : (python generator.py -l <length of sequence>)"
 sys.exit()
arglist = sys.argv
if not (arglist[1] == '-l') or not(arglist[2].isdigit()):
 print "Error: Wrong syntax - Correct usage : (python generator.py -l <length of sequence>)"
 sys.exit()
lo_seq = int(arglist[2])

file_handle = open('seqstart.txt','r')
f_h = open('seqgen.s','w')
f_h.write(file_handle.read())
file_handle.close()
isaclasses = class1 + class2 + class3 + class4 + class5 + class6 + class7

for i in range(lo_seq):
 oper = choice(isaclasses)
 instr = "L"+str(i)+":    "
 if oper in class1:
  sreg1 = choice(registers)
  sreg2 = choice(registers)
  dreg = choice(registers)
  instr = instr + oper+"    "+dreg+","+sreg1+","+sreg2
 elif oper in class2:
  sreg1 = choice(registers)
  imm = ''.join(choice(hexadigit) for j in range(choice(range(1,4))))
  imm = "0x"+imm
  dreg = choice(registers)
  instr = instr + oper+"    "+dreg+","+sreg1+","+imm
 elif oper in class3:
  if oper is 'LI':
   numofdig = range(choice(range(1,8)))
  elif oper is 'LUI':
   numofdig = range(choice(range(1,4)))
  imm = ''.join(choice(hexadigit) for j in numofdig)
  imm = "0x"+imm
  dreg = choice(registers)
  instr = instr + oper+"    "+dreg+","+imm
 elif oper in class4:
  sreg = choice(registers)
  dreg = choice(registers)
  instr = instr + oper+"    "+dreg+","+sreg
 elif oper in class5:
  sreg = choice(registers)
  dreg = choice(registers)
  shift = "0x"+str(choice(range(0,1)))+choice(hexadigit)
  instr = instr + oper+"    "+dreg+","+sreg+","+shift
 elif oper in class6:
  reg = choice(registers)
  instr = instr + oper+"    "+reg
 elif oper in class7:
  if (i+2)<(lo_seq-1):
   offset = "L"+str(choice(range(i+2,lo_seq-1)))
  else:
   f_h.write(instr+"NOP\n")
   continue
  if oper in ['B','BAL']:
   instr = instr + oper + "      "+offset
  elif oper in ['BEQ','BNE']:
   sreg1 = choice(registers)
   sreg2 = choice(registers)
   instr = instr + oper + "    "+sreg1+","+sreg2+","+offset
  else:
   sreg = choice(registers)
   instr = instr + oper + "    "+sreg+","+offset
 f_h.write(instr+"\n")
file_handle = open('seqend.txt','r')
f_h.write(file_handle.read())
file_handle.close()
f_h.close()

#checking for hazards
file_handle = open('seqgen.s','r')
f_h = open('seqhaz.txt','w')
listofseq = list()
for line in file_handle:
 if line.startswith("L"):
  templist = list()
  templist.append(line.split()[0])
  templist.append(line.split()[1])
  if not(line.split()[1] == "NOP"):
   templist = templist + line.split()[2].split(",")
  listofseq.append(templist)
RAW = 0
WAW = 0
WAR = 0
type1 = class1
type2 = class2 + ["MOVE"] + class5
type3 = class3 + ['MFHI','MFLO']
type4 = ['DIV','DIVU','MULT','MULTU']
type5 = ['MTHI','MTLO']
length = len(listofseq)
for i in range(length):
 if (listofseq[i][1] in class7):
  continue
 for j in range(i+1,length):
  if ((j - i) <= 4):
   if (listofseq[j][1] in class7):
    break
   if (listofseq[i][1] in type1):
    if (listofseq[j][1] in type1):  #type1 vs type1
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if ((listofseq[i][2] == listofseq[j][3]) or (listofseq[i][2] == listofseq[j][4]))  and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[j][2] == listofseq[i][3]) or (listofseq[j][2] == listofseq[i][4]):
      WAR += 1
      info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type3): #type1 vs type3
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[j][2] == listofseq[i][3]) or (listofseq[j][2] == listofseq[i][4]):
      WAR += 1
      info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type2): #type1 vs type2
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[i][2] == listofseq[j][3])  and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[j][2] == listofseq[i][3]) or (listofseq[j][2] == listofseq[i][4]):
      WAR += 1
      info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type4): #type1 vs type4
     if ((listofseq[i][2] == listofseq[j][2]) or (listofseq[i][2] == listofseq[j][3]))  and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type5): #type1 vs type5
     if (listofseq[i][2] == listofseq[j][2])  and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)

   elif (listofseq[i][1] in type2):
    if (listofseq[j][1] in type1):  #type2 vs type1
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if ((listofseq[i][2] == listofseq[j][3]) or (listofseq[i][2] == listofseq[j][4])) and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[j][2] == listofseq[i][3]):
      WAR += 1
      info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type2):  #type2 vs type2
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[i][2] == listofseq[j][3])  and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[j][2] == listofseq[i][3]):
      WAR += 1
      info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type3): #type2 vs type3
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[j][2] == listofseq[i][3]):
      WAR += 1
      info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type4):  #type2 vs type4
     if ((listofseq[i][2] == listofseq[j][2]) or (listofseq[i][2] == listofseq[j][3])) and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type5):  #type2 vs type5
     if (listofseq[i][2] == listofseq[j][2]) and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)

   elif (listofseq[i][1] in type3):
    if (listofseq[j][1] in type1):  #type3 vs type1
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if ((listofseq[i][2] == listofseq[j][3]) or (listofseq[i][2] == listofseq[j][4])) and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type2):  #type3 vs type2
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[i][2] == listofseq[j][3]) and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type3):  #type3 vs type3
     if (listofseq[i][2] == listofseq[j][2]):
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type4):  #type3 vs type4 
     if ((listofseq[i][2] == listofseq[j][2]) or (listofseq[i][2] == listofseq[j][3])) and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type5):  #type3 vs type5
     if (listofseq[i][2] == listofseq[j][2]) and ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)

   elif (listofseq[i][1] in type4):
    if (listofseq[j][1] in type1+type2+type3):  #type4 vs type1/type2/type3
     if (listofseq[j][2] == listofseq[i][2]) or (listofseq[j][2] == listofseq[i][3]):
      WAR += 1
      info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     if (listofseq[j][1] in ['MFHI','MFLO']): #wrt accumulator
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type5+type4): #wrt accumulator
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
     
   elif (listofseq[i][1] in type5):
    if (listofseq[j][1] in type1+type2+type3): #type5 vs type1/type2/type3
     if (listofseq[j][2] == listofseq[i][2]):
      WAR += 1
      info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
    elif (listofseq[j][1] in type5+type4): #wrt accumulator
      WAW += 1
      info = "WAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
   
   if (listofseq[i][1] == 'MFHI' and listofseq[j][1] == 'MTHI') or (listofseq[i][1] == 'MFLO' and listofseq[j][1] == 'MTLO'):
     WAR += 1
     info = "WAR hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
     f_h.write(info)
   elif (listofseq[j][1] == 'MFHI' and listofseq[i][1] == 'MTHI') or (listofseq[j][1] == 'MFLO' and listofseq[i][1] == 'MTLO'):
    if ((j - i) <= 3):
      RAW += 1
      info = "RAW hazard between "+listofseq[i][0]+" and "+listofseq[j][0]+"\n"
      f_h.write(info)
  else:
   break
f_h.write("\n\nRAW = "+str(RAW))
f_h.write("\nWAR = "+str(WAR))
f_h.write("\nWAW = "+str(WAW))
f_h.close()
