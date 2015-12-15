#!/bin/bash - 
#===============================================================================
#
#          FILE: hp_hba_info.sh
# 
#         USAGE: ./hp_hba_info.sh 
# 
#        AUTHOR: Jiadi Yue (Brady), jdyue19@gmail.com
#  ORGANIZATION: 
#       CREATED: 12/14/2015 15:09
#      REVISION:  ---
#===============================================================================
i=0; while ((i<15));
  do
    /opt/fcms/bin/fcmsutil /dev/fcd$i 2>/dev/null | grep -E "rt Port World|Driver state" | cut -d = -f 2; 
    /opt/fcms/bin/fcmsutil /dev/fcd$i vpd 2>/dev/null | grep -E "Description|Serial|Firmware " |cut -d : -f 2; 
    i=$(($i+1)); 
  done; 

i=0; while ((i<15));
  do 
    /opt/fcms/bin/fcmsutil /dev/fclp$i 2>/dev/null | grep -E "rt Port World|Driver state" | cut -d = -f 2; 
    /opt/fcms/bin/fcmsutil /dev/fclp$i vpd 2>/dev/null | grep -E "Description|Serial|Firmware " |cut -d : -f 2; 
    i=$(($i+1)); 
  done; 

i=0; while ((i<15));
  do 
    /opt/fcms/bin/fcmsutil /dev/fcoc$i 2>/dev/null | grep -E "rt Port World|Driver state" | cut -d = -f 2; 
    /opt/fcms/bin/fcmsutil /dev/fcoc$i vpd 2>/dev/null | grep -E "Description|Serial|Firmware " |cut -d : -f 2; 
    i=$(($i+1)); 
  done;
