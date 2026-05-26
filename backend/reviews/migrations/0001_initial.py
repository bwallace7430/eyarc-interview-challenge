import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
            ],
            options={"db_table": "course"},
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
            ],
            options={"db_table": "student"},
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
            ],
            options={"db_table": "resource"},
        ),
        migrations.CreateModel(
            name="ReviewCriteria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, unique=True)),
                ("prompt", models.CharField(max_length=255)),
            ],
            options={"db_table": "review_criteria"},
        ),
        migrations.CreateModel(
            name="CourseResource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reviews.course")),
                ("resource", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reviews.resource")),
            ],
            options={"db_table": "course_resource"},
        ),
        migrations.CreateModel(
            name="ResourceReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("comments", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reviews.student")),
                ("resource", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reviews.resource")),
            ],
            options={"db_table": "resource_review"},
        ),
        migrations.CreateModel(
            name="ResourceReviewScore",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveSmallIntegerField()),
                (
                    "review",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scores",
                        to="reviews.resourcereview",
                    ),
                ),
                ("criteria", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reviews.reviewcriteria")),
            ],
            options={"db_table": "resource_review_score"},
        ),
    ]
