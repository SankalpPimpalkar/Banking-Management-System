# Generated by Django 5.1.4 on 2025-01-05 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0003_alter_account_account_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.IntegerField()),
                ('transaction_type', models.CharField(choices=[('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal'), ('Transfer', 'Transfer')], max_length=20)),
                ('recipient_account', models.IntegerField(blank=True, null=True)),
                ('amount', models.FloatField()),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
