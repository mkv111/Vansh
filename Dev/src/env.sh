#!/bin/bash

# Environment Setup.
export ANCSTRY_APP_BASE=/mnt/Ancestry
export ANCSTRY_APP_HOME=$ANCSTRY_APP_BASE/Dev
export ANCSTRY_APP_BIN=$ANCSTRY_APP_HOME/src
export ANCSTRY_APP_DATA=$ANCSTRY_APP_HOME/data
export ANCSTRY_APP_LOG=$ANCSTRY_APP_HOME/log

export PATH=$PATH:$ANCSTRY_APP_BIN

# Alias Commands.
alias cdAB='cd $ANCSTRY_APP_BIN'
alias cdAD='cd $ANCSTRY_APP_DATA'
alias cdAL='cd $ANCSTRY_APP_LOG'
alias edreg='vi $ANCSTRY_APP_BIN/registration.py'
alias edenv='vi $ANCSTRY_APP_BIN/env.py'
#alias exreg='$ANCSTRY_APP_BIN/registration.sh'
alias exreg='cdAB;python3 registration.py'

# Program Initialization.

ParmInit() {
root="N"
markroot="N"
self="Y"
}

FamilyReg() {
read -p "Name your Family: " family
if [ -f $ANCSTRY_APP_DATA/${family}.csv ]
then
	echo "$family Family data already present.. Look for your family."
fi
}

PushData(){
DataFile=$ANCSTRY_APP_DATA/${family}.csv
if [ "$name" = "" -o "$age" = "" ];then echo "Data Error: Name/Age is not correct..\nEntry Discarded. Please re-enter the details..";return 1; fi
echo "$name, $age, $root, $relation" >> $DataFile
}

ProfileReg() {

if [ "$self" = "N" ]
then
	read -p "Name of the Family Member:" name
        read -p "Relation with Family Member:" relation
else
	read -p "Your Name:" name
        relation="SELF"
        self="N"
fi

read -p "Age:" age

if [ "$markroot" = "N" ]
then
        read -p "Ancestry Root? (Y/N):" root
        case $root in
                [yY])markroot=Y;;
                *)root="N";makeroot=N;;
        esac

        PushData $name $age $root $relation
	if [ $? -gt 0 ];then ParamInit; return;fi
else
        PushData $name $age "N" $relation
	if [ $? -gt 0 ];then ParamInit; return;fi
fi

read -p "Register more family members? (Y/N)" more
case $more in
        [yY]) echo ;;
        *) exit;;
esac
}
