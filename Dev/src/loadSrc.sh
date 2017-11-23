#!/bin/bash

FamilyReg() {
read -p "Name your Family: " family
}

PushData(){
DataFile=$ANCSTRY_APP_DATA/${family}.csv
echo "$name, $age, $root, $relation" >> $DataFile
}

ProfileReg() {
read -p "Name:" name
read -p "Age:" age

if [ "$self" = "N" ]
then
	read -p "Relation with Member:" relation
else
	relation="SELF"
	self="N"
fi

if [ "$markroot" = "N" ]
then
	read -p "Ancestry Root? (Y/N):" root
	case $root in
		[yY])markroot=Y;;
		*)root="N";makeroot=N;;
	esac

	PushData $name $age $root $relation
else
	PushData $name $age "N" $relation
fi

read -p "Register more family members? (Y/N)" more
case $more in
	[yY]) echo ;;
	*) exit;;
esac
}
