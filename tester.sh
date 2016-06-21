rm -rf seqgen.s seqhaz.txt log_g.txt log.txt reglog_g.txt reglog.txt seqgen
python generator.py $1 $2
#compiling
$HOME/simplescalar/bin/sslittle-na-sstrix-gcc -o seqgen seqgen.s
#running golden processor
$HOME/simplescalar/simplesim-3.0/sim-outorder -redir:sim log_g.txt seqgen
mv reglog.txt reglog_g.txt
#running candidate processor
#$HOME/simplescalar/simplesim-3.0/sim-outorder -redir:sim log.txt -bpred taken seqgen
$HOME/simplescalar/simplesim-3.0/sim-outorder -redir:sim log.txt -issue:inorder true seqgen
python verify.py ${3}
