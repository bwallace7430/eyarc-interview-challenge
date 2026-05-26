from django.db import models

from softdelete.models import SoftDeleteObject


# --- Scaffolding models (not part of the interview challenge) ---


class Course(SoftDeleteObject):
    title = models.CharField(max_length=255)

    class Meta:
        db_table = "course"


class Student(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "student"


# --- Provided models (read-only context for the interview) ---


class Resource(SoftDeleteObject):
    """A learning resource (video, article, etc.)."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "resource"


class CourseResource(SoftDeleteObject):
    """Junction table linking a resource to a specific course offering."""

    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    class Meta:
        db_table = "course_resource"


class ReviewCriteria(models.Model):
    """A named criterion students rate (e.g. 'clarity', 'helpfulness')."""

    name = models.CharField(max_length=64, unique=True)
    prompt = models.CharField(max_length=255)

    class Meta:
        db_table = "review_criteria"


class ResourceReview(SoftDeleteObject):
    """A student's overall review of a resource."""

    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "resource_review"


class ResourceReviewScore(models.Model):
    """Per-criterion score attached to a ResourceReview."""

    review = models.ForeignKey(
        ResourceReview, on_delete=models.CASCADE, related_name="scores"
    )
    criteria = models.ForeignKey(ReviewCriteria, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "resource_review_score"
