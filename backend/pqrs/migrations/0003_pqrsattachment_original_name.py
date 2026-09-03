from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pqrs", "0002_ticketsequence_attachment_ticketlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="pqrsattachment",
            name="original_name",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]