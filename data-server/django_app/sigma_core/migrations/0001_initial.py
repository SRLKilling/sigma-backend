# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-14 22:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('lastname', models.CharField(max_length=255)),
                ('firstname', models.CharField(max_length=128)),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Acknowledgment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AcknowledgmentInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_by_invitee', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField(blank=True)),
                ('is_protected', models.BooleanField(default=False)),
                ('can_anyone_ask', models.BooleanField(default=False)),
                ('need_validation_to_join', models.BooleanField(default=False)),
                ('members_visibility', models.PositiveSmallIntegerField(choices=[(0, 'Public'), (1, 'Normal'), (2, 'Secret')], default=0)),
                ('group_visibility', models.PositiveSmallIntegerField(choices=[(0, 'Public'), (1, 'Normal'), (2, 'Secret')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GroupField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Number'), (1, 'String'), (2, 'Choice'), (3, 'Email')], default=0)),
                ('accept', models.TextField(blank=True, default='')),
                ('protected', models.BooleanField(default=False)),
                ('multiple_values_allowed', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='sigma_core.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupFieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='sigma_core.GroupField')),
            ],
        ),
        migrations.CreateModel(
            name='GroupInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_by_invitee', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='sigma_core.Group')),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hidden', models.BooleanField(default=False)),
                ('is_administrator', models.BooleanField(default=False)),
                ('is_super_administrator', models.BooleanField(default=False)),
                ('has_invite_right', models.BooleanField(default=False)),
                ('has_contact_right', models.BooleanField(default=False)),
                ('has_publish_right', models.BooleanField(default=False)),
                ('has_kick_right', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='sigma_core.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupfieldvalue',
            name='membership',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_values', to='sigma_core.GroupMember'),
        ),
        migrations.AddField(
            model_name='acknowledgmentinvitation',
            name='acknowledged',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_to_be_acknowledged', to='sigma_core.Group'),
        ),
        migrations.AddField(
            model_name='acknowledgmentinvitation',
            name='acknowledged_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_to_acknowledge', to='sigma_core.Group'),
        ),
        migrations.AddField(
            model_name='acknowledgment',
            name='acknowledged',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acknowledged_by', to='sigma_core.Group'),
        ),
        migrations.AddField(
            model_name='acknowledgment',
            name='acknowledged_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acknowledged', to='sigma_core.Group'),
        ),
        migrations.AlterUniqueTogether(
            name='userconnection',
            unique_together=set([('user1', 'user2')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupmember',
            unique_together=set([('user', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupinvitation',
            unique_together=set([('invitee', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupfieldvalue',
            unique_together=set([('membership', 'field')]),
        ),
        migrations.AlterUniqueTogether(
            name='acknowledgmentinvitation',
            unique_together=set([('acknowledged', 'acknowledged_by')]),
        ),
        migrations.AlterUniqueTogether(
            name='acknowledgment',
            unique_together=set([('acknowledged', 'acknowledged_by')]),
        ),
    ]
