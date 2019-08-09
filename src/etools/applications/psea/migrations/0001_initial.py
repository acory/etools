# Generated by Django 2.2.3 on 2019-08-09 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_fsm
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchase_order', '0007_auto_20190625_1437'),
        ('partners', '0038_auto_20190620_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('reference_number', models.CharField(max_length=100, unique=True, verbose_name='Reference Number')),
                ('overall_rating', models.IntegerField(blank=True, null=True)),
                ('assessment_date', models.DateField(blank=True, null=True, verbose_name='Assessment Date')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='psea_assessment', to='partners.PartnerOrganization', verbose_name='Partner')),
            ],
            options={
                'verbose_name': 'Assessment',
                'verbose_name_plural': 'Assessments',
                'ordering': ('-assessment_date',),
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('label', models.CharField(max_length=50, verbose_name='Label')),
                ('weight', models.IntegerField(verbose_name='Weight')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Ratings',
            },
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('subject', models.TextField(verbose_name='Subject')),
                ('content', models.TextField(verbose_name='Content')),
                ('active', models.BooleanField(default=True)),
                ('ratings', models.ManyToManyField(to='psea.Rating', verbose_name='Rating')),
            ],
            options={
                'verbose_name': 'Indicator',
                'verbose_name_plural': 'Indicators',
            },
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('label', models.TextField(verbose_name='Label')),
                ('requires_description', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('indicators', models.ManyToManyField(to='psea.Indicator', verbose_name='Indicators')),
            ],
            options={
                'verbose_name': 'Evidence',
                'verbose_name_plural': 'Evidence',
            },
        ),
        migrations.CreateModel(
            name='Assessor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('assessor_type', models.CharField(choices=[('external', 'External Individual'), ('unicef', 'UNICEF Staff'), ('vendor', 'Assessing Firm')], max_length=30, verbose_name='Type')),
                ('order_number', models.CharField(blank=True, max_length=30, verbose_name='Order Number')),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psea.Assessment', verbose_name='Assessment')),
                ('auditor_firm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='purchase_order.AuditorFirm', verbose_name='Auditor')),
                ('auditor_firm_staff', models.ManyToManyField(blank=True, to='purchase_order.AuditorStaffMember', verbose_name='Auditor Staff')),
                ('focal_points', models.ManyToManyField(blank=True, related_name='assessor_focal_point', to=settings.AUTH_USER_MODEL, verbose_name='UNICEF Focal Points')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Assessor',
                'verbose_name_plural': 'Assessors',
            },
        ),
        migrations.CreateModel(
            name='AssessmentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', django_fsm.FSMField(choices=[('draft', 'Draft'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('submitted', 'Submitted'), ('final', 'Final'), ('cancelled', 'Cancelled')], default='draft', max_length=30, verbose_name='Status')),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psea.Assessment', verbose_name='Assessment')),
            ],
            options={
                'verbose_name': 'Assessment Status',
                'verbose_name_plural': 'Assessment Statuses',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='AnswerEvidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psea.Answer', verbose_name='Answer')),
                ('evidence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psea.Evidence', verbose_name='Evidence')),
            ],
            options={
                'verbose_name': 'Answer Evidence',
                'verbose_name_plural': 'Answer Evidences',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psea.Assessment', verbose_name='Assessment'),
        ),
        migrations.AddField(
            model_name='answer',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psea.Indicator', verbose_name='Indicator'),
        ),
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psea.Rating', verbose_name='Rating'),
        ),
    ]
