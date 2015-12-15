for i in `lsdev -Cc adapter -S a | grep fcs | grep Available | cut -d " " -f 1`; do echo $(lscfg -vpl $i | grep "Network" | awk -F. '{print $NF}'); echo $(lscfg -vpl $i | grep $i); done
