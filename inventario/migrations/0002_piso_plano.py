from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="piso",
            name="plano",
            field=models.ImageField(
                blank=True,
                help_text="Imagen del plano del piso (PNG, JPG o WEBP).",
                null=True,
                upload_to="planos/",
            ),
        ),
    ]
