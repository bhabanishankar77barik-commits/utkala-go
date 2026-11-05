
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile


media_root = Path(settings.MEDIA_ROOT)

uploaded = 0
missing = 0
failed = 0

for model in apps.get_models():

    image_fields = [
        field
        for field in model._meta.fields
        if field.get_internal_type() == "FileField"
    ]

    if not image_fields:
        continue

    for obj in model.objects.all():

        for field in image_fields:

            image = getattr(obj, field.name)

            if not image or not image.name:
                continue

            old_name = image.name

            # Skip files already stored on Cloudinary
            if old_name.startswith("media/"):
                print("SKIPPED:", model.__name__, old_name)
                continue

            local_path = media_root / old_name

            if not local_path.exists():
                print("MISSING:", model.__name__, old_name)
                missing += 1
                continue

            try:
                with open(local_path, "rb") as file:
                    content = ContentFile(
                        file.read(),
                        name=Path(old_name).name
                    )

                new_name = image.storage.save(
                    old_name,
                    content
                )

                setattr(obj, field.name, new_name)
                obj.save(update_fields=[field.name])

                print("UPLOADED:", model.__name__, old_name, "->", new_name)

                uploaded += 1

            except Exception as error:
                print("ERROR:", model.__name__, old_name, error)
                failed += 1

print("\nIMAGE MIGRATION FINISHED")
print("Uploaded:", uploaded)
print("Missing:", missing)
print("Failed:", failed)
