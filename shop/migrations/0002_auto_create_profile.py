from django.db import migrations
from django.contrib.auth import get_user_model


def create_profiles(apps, schema_editor):
    User = get_user_model()
    Profile = apps.get_model("shop", "Profile")
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_profiles),
    ]
