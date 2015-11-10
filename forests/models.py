from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)


class Employee(models.Model):
    name = models.CharField(max_length=20)
    nt_account = models.CharField(max_length=20)
    team = models.ForeignKey('Team')


class Server(models.Model):
    host_name = models.CharField(max_length=20, null=True)
    ip_addr = models.CharField(max_length=15)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    owner = models.ForeignKey('Employee', null=True)
    team = models.ForeignKey('Team', null=True)
    os = models.CharField(max_length=20, default=None, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Switch(models.Model):
    name = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    ip_addr = models.CharField(max_length=15)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class SwitchPort(models.Model):
    switch = models.ForeignKey('Switch')
    port_index = models.IntegerField()
    vf_vsan = models.IntegerField()


class HBA(models.Model):
    model = models.CharField(max_length=20)
    description = models.CharField(max_length=200, null=True)
    driver_name = models.CharField(max_length=20, null=True)
    driver_version = models.CharField(max_length=20, null=True)
    firmware_version = models.CharField(max_length=20, null=True)
    serial_number = models.CharField(max_length=50)
    server = models.ForeignKey('Server', default=None)


class HbaPort(models.Model):
    wwpn = models.CharField(max_length=23)
    hba_card = models.ForeignKey('HBA')
    link_down = models.NullBooleanField()
    connection = models.ForeignKey('SwitchPort', null=True)
