from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)


class Employee(models.Model):
    name = models.CharField(max_length=20)
    nt_account = models.CharField(max_length=20)
    team = models.ForeignKey('Team')


class Server(models.Model):
    host_name = models.CharField(max_length=20)
    ip_addr = models.CharField(max_length=15)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    owner = models.ForeignKey('Employee')
    team = models.ForeignKey('Team')
    os = models.CharField(max_length=20, default=None)


class Switch(models.Model):
    name = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    ip_addr = models.CharField(max_length=15)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    model = models.CharField(max_length=20)


class SwitchPort(models.Model):
    switch = models.ForeignKey('Switch')
    port_index = models.IntegerField()
    vf_vsan = models.IntegerField()


class HBA(models.Model):
    vendor = models.CharField(max_length=20)
    wwn = models.CharField(max_length=23)
    model = models.CharField(max_length=20)


class HbaPort(models.Model):
    updated = models.DateTimeField(auto_now=True)
    wwn = models.CharField(max_length=23)
    hba_card = models.ForeignKey('HBA')
    link_down = models.BooleanField()
    connection = models.ForeignKey('SwitchPort')
