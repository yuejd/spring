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
