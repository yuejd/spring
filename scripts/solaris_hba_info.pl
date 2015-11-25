my $info = `fcinfo hba-port`;
my @info_list = split /\n(?=HBA)/, $info;
print "[\n";
for (@info_list) {
	print "{\n";

	print "\"WWPN\": ";
	$_ =~ /(?<=Port WWN: )(\w+)/;
	my $wwpn = $1;
	$wwpn =~ s/..\K\B/:/g;
	print "\"$wwpn\"";
	print ",\n";

	print "\"Model\": ";
	$_ =~ /(?<=Model: )([-_a-zA-Z0-9]+)/;
	print "\"$1\"";
	print ",\n";

	print "\"Active\": ";
	$_ =~ /(?<=State: )(\w+)/;
	if( $1 eq "online" ) {
		print "true";
	} else {
		print "false";
	}
	print ",\n";
		
	print "\"SerialNumber\": ";
	$_ =~ /(?<=Serial Number: )(.+)/;
	print "\"$1\"";
	print ",\n";

	print "\"ModelDescription\": ";
	$_ =~ /(?<=Manufacturer: )(.+)/;
	print "\"$1\"";
	print ",\n";

	print "\"FirmwareVersion\": ";
	$_ =~ /(?<=Firmware Version: )(.+)/;
	print "\"$1\"";
	print "\n";

	if( \$_ == \$info_list[-1] ) {
		print "}\n";
	} else {
		print "},\n";
	}
}
print "]\n";
