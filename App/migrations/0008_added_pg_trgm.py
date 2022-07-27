from django.db import migrations, models
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):
    dependencies = [
        ('App', '0007_user_verificationcode'),
    ]

    operations = [
        TrigramExtension(),
    ]