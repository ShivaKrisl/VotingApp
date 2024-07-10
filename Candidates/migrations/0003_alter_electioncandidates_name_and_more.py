# Generated by Django 5.0 on 2024-03-31 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Candidates", "0002_electioncandidates"),
    ]

    operations = [
        migrations.AlterField(
            model_name="electioncandidates",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="electioncandidates",
            name="party_name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
