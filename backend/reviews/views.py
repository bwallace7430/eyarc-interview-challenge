from typing import Annotated

from adrf.views import APIView
from django.shortcuts import aget_object_or_404
from drf_pydantic import BaseModel
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CourseResource, Resource, ResourceReview, ResourceReviewScore, ReviewCriteria
from .permissions import IsStudent


class ResourceReviewQueryIn(BaseModel):
    drf_config = {"validate_pydantic": True}

    resource_id: int | None = None
    course_resource_id: int | None = None


ResourceReviewQuerySerializer = ResourceReviewQueryIn.drf_serializer


class ResourceReviewIn(BaseModel):
    drf_config = {"validate_pydantic": True}

    resource_id: int | None = None
    course_resource_id: int | None = None
    comments: Annotated[
        str | None, CharField(allow_blank=True, required=False, default="")
    ]
    clarity: int
    helpfulness: int
    relevance: int
    difficulty: int


ResourceReviewSerializer = ResourceReviewIn.drf_serializer


class ReviewCriteriaOut(BaseModel):
    drf_config = {"validate_pydantic": True}

    id: int
    name: str
    prompt: str


class ResourceReviewResponseOut(BaseModel):
    drf_config = {"validate_pydantic": True}

    criteria: list[ReviewCriteriaOut]
    resource_title: str


ResourceReviewGetResponseSerializer = ResourceReviewResponseOut.drf_serializer


class ResourceReviewView(APIView):
    serializer_class = None
    permission_classes = [IsAuthenticated, IsStudent]

    @extend_schema(
        parameters=[ResourceReviewQuerySerializer],
        responses={
            200: ResourceReviewGetResponseSerializer,
            204: None,
            400: None,
        },
    )
    async def get(self, request):
        student_id = request.student_id
        s = ResourceReviewQuerySerializer(data=request.query_params)
        s.is_valid(raise_exception=True)
        p = s.pydantic_instance

        resource_id = p.resource_id
        if resource_id is None:
            if p.course_resource_id is None:
                return Response(
                    {"error": "Either resource_id or course_resource_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            course_resource = await aget_object_or_404(
                CourseResource, id=p.course_resource_id
            )
            resource_id = course_resource.resource_id

        review_exists = await ResourceReview.objects.filter(
            student_id=student_id, resource_id=resource_id
        ).aexists()

        if not review_exists:
            return Response(status=status.HTTP_204_NO_CONTENT)

        criteria = [c async for c in ReviewCriteria.objects.all()]
        resource = await aget_object_or_404(Resource, id=resource_id)

        criteria_data = [
            {"id": c.pk, "name": c.name, "prompt": c.prompt}
            for c in criteria
        ]

        return Response(
            {"criteria": criteria_data, "resource_title": resource.title},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=ResourceReviewSerializer,
        responses={201: None, 400: None},
    )
    async def post(self, request):
        s = ResourceReviewSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        p = s.pydantic_instance

        resource_id = p.resource_id
        if resource_id is None:
            if p.course_resource_id is None:
                return Response(
                    {"error": "Either resource_id or course_resource_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            course_resource = await aget_object_or_404(
                CourseResource, id=p.course_resource_id
            )
            resource_id = course_resource.resource_id

        review, _ = await ResourceReview.objects.aget_or_create(
            student_id=request.student_id,
            resource_id=resource_id,
            defaults={
                "comments": p.comments or "",
            },
        )

        score_data = {
            "clarity": p.clarity,
            "helpfulness": p.helpfulness,
            "relevance": p.relevance,
            "difficulty": p.difficulty,
        }

        criteria_list = [
            c async for c in ReviewCriteria.objects.filter(name__in=score_data.keys())
        ]
        criteria_dict = {c.name: c for c in criteria_list}

        scores = [
            ResourceReviewScore(
                review=review,
                criteria=criteria_dict[name],
                score=value,
            )
            for name, value in score_data.items()
            if name in criteria_dict
        ]

        await ResourceReviewScore.objects.abulk_create(scores)

        return Response(
            {"message": "Review submitted successfully"},
            status=status.HTTP_201_CREATED,
        )
