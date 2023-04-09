# Generated by Django 4.1.7 on 2023-03-28 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_bookinstance_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'), ('is_staff', 'Is it a staff member?'))},
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'Maintenance'), ('a', 'Available'), ('o', 'On loan'), ('r', 'Reserverd')], default='m', help_text='Book availability', max_length=1),
        ),
    ]
