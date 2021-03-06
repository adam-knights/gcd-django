# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-23 15:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('uses_tokens', models.BooleanField(default=False)),
                ('allows_abstentions', models.BooleanField(default=False)),
                ('quorum', models.IntegerField(blank=True, default=1, help_text='Quorum must always be at least 1')),
                ('secret_ballot', models.BooleanField(default=False)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Permission')),
                ('subscribers', models.ManyToManyField(editable=False, related_name='subscribed_agendas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AgendaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('notes', models.TextField(blank=True, null=True)),
                ('state', models.NullBooleanField(choices=[(None, 'Pending'), (True, 'Open'), (False, 'Closed')])),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('agenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='voting.Agenda')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agenda_items', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(editable=False, related_name='subscribed_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'voting_agenda_item',
            },
        ),
        migrations.CreateModel(
            name='AgendaMailingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_agenda_item_add', models.BooleanField(default=False)),
                ('on_agenda_item_open', models.BooleanField(default=False)),
                ('on_vote_open', models.BooleanField(default=False)),
                ('on_vote_close', models.BooleanField(default=False)),
                ('is_primary', models.BooleanField(default=False)),
                ('reminder', models.BooleanField(default=False)),
                ('display_token', models.BooleanField(default=False)),
                ('agenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agenda_mailing_lists', to='voting.Agenda')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'db_table': 'voting_agenda_mailing_list',
            },
        ),
        migrations.CreateModel(
            name='ExpectedVoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenure_began', models.DateTimeField()),
                ('tenure_ended', models.DateTimeField(blank=True, null=True)),
                ('agenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expected_voters', to='voting.Agenda')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voting_expectations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('tenure_began', 'tenure_ended', 'voter__last_name', 'voter__first_name'),
                'db_table': 'voting_expected_voter',
            },
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.EmailField(max_length=75)),
            ],
            options={
                'db_table': 'voting_mailing_list',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField(blank=True, null=True)),
                ('ballot_position', models.IntegerField(blank=True, help_text='Optional whole number used to arrange the options in an order other than alphabetical by name.', null=True)),
                ('result', models.NullBooleanField()),
            ],
            options={
                'ordering': ('ballot_position', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_key', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField(blank=True, null=True)),
                ('open', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('deadline', models.DateTimeField(db_index=True)),
                ('token', models.CharField(editable=False, max_length=255, null=True)),
                ('result_calculated', models.BooleanField(db_index=True, default=False, editable=False)),
                ('invalid', models.BooleanField(default=False, editable=False)),
                ('agenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='voting.Agenda')),
                ('agenda_items', models.ManyToManyField(related_name='topics', to='voting.AgendaItem')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to=settings.AUTH_USER_MODEL)),
                ('second', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seconded_topics', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(editable=False, related_name='subscribed_topics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='voting.Option')),
                ('voter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VoteType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('max_votes', models.IntegerField(blank=True, default=1, help_text='Having more votes than winners sets up ranked choice voting.  Leave max votes blank to allow as many ranks as options.', null=True)),
                ('max_winners', models.IntegerField(default=1, help_text='Having more than one winner allows votes to be cast for up to that many options.')),
            ],
            options={
                'db_table': 'voting_vote_type',
            },
        ),
        migrations.AddField(
            model_name='topic',
            name='vote_type',
            field=models.ForeignKey(help_text='Pass / Fail types will automatically create their own Options if none are specified directly.  For other types, add Options below.', on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='voting.VoteType'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='voting.Topic'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='option',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='voting.Topic'),
        ),
        migrations.AddField(
            model_name='option',
            name='voters',
            field=models.ManyToManyField(related_name='voted_options', through='voting.Vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agendamailinglist',
            name='mailing_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agenda_mailing_lists', to='voting.MailingList'),
        ),
    ]
