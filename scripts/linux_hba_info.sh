#!/bin/bash
if [ -d "/sys/class/fc_host/" ]; then
	echo -e "["
	for i in `ls /sys/class/fc_host/`
	do
		echo -e "{"
		echo -e "\"Model\":\"`cd /sys/class/scsi_host/$i/device/scsi_host/$i/; cat modelname || cat model_name`\","
		echo -e "\"WWPN\":\"`cat /sys/class/fc_host/$i/node_name |cut -d 'x' -f2 | sed 's/../&:/g;s/:$//' `\","
	    if [ "`cat /sys/class/fc_host/$i/port_state`" == "Online" ]; then
		echo -e "\"Active\":true,"
	    else
		echo -e "\"Active\":false,"
	    fi
		echo -e "\"SerialNumber\":\"`cd /sys/class/scsi_host/$i/device/scsi_host/$i/; cat serialnum || cat serial_num`\","
		echo -e "\"ModelDescription\":\"`cd /sys/class/scsi_host/$i/device/scsi_host/$i/; cat modeldesc || cat model_desc`\","
		echo -e "\"FirmwareVersion\":\"`cd /sys/class/scsi_host/$i/device/scsi_host/$i/; cat fwrev || cat fw_version`\""
		if [ ! $processedLast ]
		then
			echo -e "},"
		else
			echo -e "}"
		fi
	done
	echo -e "]"
fi
