# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-06 17:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('user_count', models.IntegerField()),
                ('view_count', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Access Record',
                'verbose_name_plural': 'Access Record',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('nagios_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Nagios Host ID')),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('internal_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=128)),
                ('ssh_port', models.IntegerField(blank=True, null=True)),
                ('status', models.SmallIntegerField(choices=[(0, 'Normal'), (1, 'Down'), (2, 'No Connect'), (3, 'Error')])),
                ('brand', models.CharField(choices=[('DELL', 'DELL'), ('HP', 'HP'), ('Other', 'Other')], max_length=64)),
                ('model', models.CharField(max_length=64)),
                ('cpu', models.CharField(max_length=64)),
                ('core_num', models.SmallIntegerField(choices=[(2, b'2 Cores'), (4, b'4 Cores'), (6, b'6 Cores'), (8, b'8 Cores'), (10, b'10 Cores'), (12, b'12 Cores'), (14, b'14 Cores'), (16, b'16 Cores'), (18, b'18 Cores'), (20, b'20 Cores'), (22, b'22 Cores'), (24, b'24 Cores'), (26, b'26 Cores'), (28, b'28 Cores')])),
                ('hard_disk', models.IntegerField()),
                ('memory', models.IntegerField()),
                ('system', models.CharField(choices=[('CentOS', 'CentOS'), ('FreeBSD', 'FreeBSD'), ('Ubuntu', 'Ubuntu')], max_length=32, verbose_name='System OS')),
                ('system_version', models.CharField(max_length=32)),
                ('system_arch', models.CharField(choices=[('x86_64', 'x86_64'), ('i386', 'i386')], max_length=32)),
                ('create_time', models.DateField()),
                ('guarantee_date', models.DateField()),
                ('service_type', models.CharField(choices=[(b'moniter', 'Moniter'), (b'lvs', 'LVS'), (b'db', 'Database'), (b'analysis', 'Analysis'), (b'admin', 'Admin'), (b'storge', 'Storge'), (b'web', 'WEB'), (b'email', 'Email'), (b'mix', 'Mix')], max_length=32)),
                ('description', models.TextField()),
                ('administrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'Admin')),
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'Host',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('hosts', models.ManyToManyField(blank=True, related_name='groups', to='app.Host', verbose_name='Hosts')),
            ],
            options={
                'verbose_name': 'Host Group',
                'verbose_name_plural': 'Host Group',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('contact', models.CharField(max_length=32)),
                ('telphone', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=128)),
                ('customer_id', models.CharField(max_length=128)),
                ('create_time', models.DateField(auto_now=True)),
                ('groups', models.ManyToManyField(to='auth.Group')),
            ],
            options={
                'verbose_name': 'IDC',
                'verbose_name_plural': 'IDC',
            },
        ),
        migrations.CreateModel(
            name='MaintainLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintain_type', models.CharField(max_length=32)),
                ('hard_type', models.CharField(max_length=16)),
                ('time', models.DateTimeField()),
                ('operator', models.CharField(max_length=16)),
                ('note', models.TextField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Host')),
            ],
            options={
                'verbose_name': 'Maintain Log',
                'verbose_name_plural': 'Maintain Log',
            },
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.IDC'),
        ),
    ]
