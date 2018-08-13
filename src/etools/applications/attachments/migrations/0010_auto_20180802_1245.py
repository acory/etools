# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-02 12:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_file_types(apps, schema_editor):
    FileTypeOld = apps.get_model("attachments", "filetype")
    FileType = apps.get_model("unicef_attachments", "filetype")
    for f in FileTypeOld.objects.all():
        FileType.objects.create(
            id=f.pk,
            name=f.name,
            label=f.label,
            code=f.code,
            order=f.order,
        )


def migrate_attachments(apps, schema_editor):
    AttachmentOld = apps.get_model("attachments", "attachment")
    Attachment = apps.get_model("unicef_attachments", "attachment")
    FileType = apps.get_model("unicef_attachments", "filetype")
    for a in AttachmentOld.objects.all():
        ft = FileType.objects.get(pk=a.file_type.pk)
        Attachment.objects.create(
            id=a.pk,
            file_type=ft,
            file=a.file,
            hyperlink=a.hyperlink,
            content_type=a.content_type,
            object_id=a.object_id,
            code=a.code,
            uploaded_by=a.uploaded_by,
            created=a.created,
            modified=a.modified,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0009_attachmentflat_agreement_link'),
        ('unicef_attachments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments_old', to='contenttypes.ContentType', verbose_name='Content Type'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='file_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments_old', to='attachments.FileType', verbose_name='Document Type'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments_old', to=settings.AUTH_USER_MODEL, verbose_name='Uploaded By'),
        ),
        migrations.RunPython(
            migrate_file_types,
            migrations.RunPython.noop
        ),
        migrations.RunPython(
            migrate_attachments,
            migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='attachmentflat',
            name='attachment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denormalized', to='unicef_attachments.Attachment'),
        ),
    ]
