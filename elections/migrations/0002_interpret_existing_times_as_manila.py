from datetime import timedelta

from django.db import migrations


def move_existing_election_times_to_manila(apps, schema_editor):
    Election = apps.get_model('elections', 'Election')

    for election in Election.objects.all():
        election.start_time = election.start_time - timedelta(hours=8)
        election.end_time = election.end_time - timedelta(hours=8)
        election.save(
            update_fields=[
                'start_time',
                'end_time',
            ]
        )


def restore_existing_election_times_to_utc(apps, schema_editor):
    Election = apps.get_model('elections', 'Election')

    for election in Election.objects.all():
        election.start_time = election.start_time + timedelta(hours=8)
        election.end_time = election.end_time + timedelta(hours=8)
        election.save(
            update_fields=[
                'start_time',
                'end_time',
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            move_existing_election_times_to_manila,
            restore_existing_election_times_to_utc
        ),
    ]
