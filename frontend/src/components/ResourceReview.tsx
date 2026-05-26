"use client";

import { useParams } from "next/navigation";

import { useSDK } from "@/utils/use-sdk";
import { apiResourcesReviewRetrieve } from "@/client";

import ResourceReviewContainer from "./ResourceReviewContainer";

type ReviewCriterion = {
    id: number;
    name: string;
    prompt: string;
};

type ReviewResponse = {
    criteria: ReviewCriterion[];
    resource_title: string;
};

const isReviewResponse = (data: unknown): data is ReviewResponse => {
    return !!(
        data &&
        typeof data === "object" &&
        "criteria" in data &&
        "resource_title" in data
    );
};

export default function ResourceReview() {
    const { courseResourceId } = useParams();

    const { data, error, isLoading } = useSDK(apiResourcesReviewRetrieve, {});

    if (isLoading) return <p className="text-sm text-gray-400">Loading…</p>;

    if (error) return (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4">
            <p className="text-sm font-medium text-red-700">Error loading review form</p>
            <pre className="mt-2 overflow-auto whitespace-pre-wrap text-xs text-red-600">
                {JSON.stringify(error, null, 2)}
            </pre>
        </div>
    );

    if (isReviewResponse(data)) {
        return (
            <ResourceReviewContainer
                criteria={data.criteria}
                courseResourceId={Number(courseResourceId)}
                resourceTitle={data.resource_title}
            />
        );
    }

    return <p>No content to review.</p>;
}
