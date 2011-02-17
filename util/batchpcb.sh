#!/bin/bash
# batchpcb.sh - batch up files for batchpcb

if [ $# -ne 1 ]
then
    echo "Please supply the base filename as the only arg"
    exit
fi

rm $1.tgz
echo "tar czvf $1.tgz $1.gbl $1.gbo $1.gbs $1.gtl $1.gto $1.gtp $1.gts $1.oln $1.txt"
tar czvf $1.tgz $1.gbl $1.gbo $1.gbs $1.gtl $1.gto $1.gtp $1.gts $1.oln $1.txt
