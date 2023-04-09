# Generated by Django 4.1.7 on 2023-03-14 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_book_author_alter_bookinstance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(help_text='13 Character', max_length=13, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Available'), ('r', 'Reserverd'), ('o', 'On loan'), ('m', 'Maintenance')], default='m', help_text='Book availability', max_length=1),
        ),
    ]