# Generated by Django 4.0.5 on 2022-09-28 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_alter_videoviews_timeofview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='Mcq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('option1', models.CharField(max_length=200)),
                ('option2', models.CharField(max_length=200)),
                ('option3', models.CharField(max_length=200)),
                ('option4', models.CharField(max_length=200)),
                ('answer', models.CharField(max_length=200)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
        ),
    ]
