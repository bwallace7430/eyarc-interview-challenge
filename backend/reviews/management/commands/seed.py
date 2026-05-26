from django.core.management.base import BaseCommand

from reviews.models import Course, CourseResource, Resource, ReviewCriteria, Student


class Command(BaseCommand):
    help = "Seed sample data for the interview environment"

    def handle(self, *args, **options):
        Student.objects.get_or_create(id=1, defaults={"name": "Test Student"})

        criteria = [
            ("clarity", "How clearly was the content presented?"),
            ("helpfulness", "How helpful was this resource for your learning?"),
            ("relevance", "How relevant was this to the course material?"),
            ("difficulty", "How appropriate was the difficulty level?"),
        ]
        for name, prompt in criteria:
            ReviewCriteria.objects.get_or_create(name=name, defaults={"prompt": prompt})

        resource, _ = Resource.objects.get_or_create(
            id=1,
            defaults={
                "title": "Introduction to Machine Learning",
                "description": "A comprehensive introduction to ML concepts.",
            },
        )

        course, _ = Course.objects.get_or_create(id=1, defaults={"title": "CS 101"})

        CourseResource.objects.get_or_create(
            id=1,
            defaults={"course": course, "resource": resource},
        )

        self.stdout.write(self.style.SUCCESS("Done. Visit http://localhost:3000/resources/1"))
