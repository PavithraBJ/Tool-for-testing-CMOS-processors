# Tool-for-testing-CMOS-processors
a test tool which is capable of generating random test sequence of desired length to test single-issue pipelined microprocessor using Python and Simplescalar. The tool performs functional test and performance test for a target processor comparing the result with the golden processor. 

Implementation:
Generating random sequence of instructions and detecting data hazards
isa.py - 
Machine description file which includes the set of instructions supported by the test tool. Instructions are classified based on the PISA ISA encoding.
generator.py -  input files: seqstart.txt, seqend.txt     output files: seqgen.s, seqhaz.txt
Generates random assembly sequence of desired length by randomly selecting instructions from the list of instructions in isa.py and stores the sequence in seqgen.s
Branching out of range is avoided by branching with labels. Each random instruction is given a label. Tool can randomly select a label of the random sequence. The last two instructions in the sequence cannot be Branch instruction and tool supports only forward loops in order to avoid infinite loops. This makes sure branching is within the sequence generated.
seqhaz.txt reports the data hazards of the generated random sequence. Data hazards are obtained considering no data forwarding. 
Testing microprocessor
Simulator- sim-outorder
seqgen.s- output file: reglog.txt, reglog_g.txt, log.txt, log_g.txt
Golden processor uses the default configuration (-issue:inorder false). Considered a candidate processor which uses different pipeline (-issue:inorder true) compared to golden processor.
Compiled sequence is run for golden processor and candidate processor, register contents and stats report of the simulation is collected in reglog.txt and log.txt respectively for candidate processor and in reglog_g.txt and log_g.txt for golden processor.
verify.py-
Verifies the register output and CPI of the candidate processor with the expected values of golden processor and reports the (functional and performance)test result
tester.sh-
The entire test process is automated using the script tester.sh
Usage:
./tester.sh -l <length of sequence> [-ip]
-l : required option for length
-ip : optional, To indicate the tool to include performance test for processor.
       Default – Tool only performs functional test for processor.
