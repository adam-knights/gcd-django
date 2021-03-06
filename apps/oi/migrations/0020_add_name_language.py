# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-03 16:31


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stddata', '0003_script'),
        ('oi', '0019_creator_story_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatornamedetailrevision',
            name='is_official_name',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='creatornamedetailrevision',
            name='in_script',
            field=models.ForeignKey(default=37, on_delete=django.db.models.deletion.CASCADE, to='stddata.Script'),
        ),
        migrations.AlterField(
            model_name='creatornamedetailrevision',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='revision_name_details', to='gcd.NameType'),
        ),
    ]
