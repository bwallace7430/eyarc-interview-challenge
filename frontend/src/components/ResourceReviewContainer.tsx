"use client";

import { useState } from "react";

import ReviewForm from "./ReviewForm";

type ReviewCriterion = {
    id: number;
    name: string;
    prompt: string;
};

type Props = {
    criteria: ReviewCriterion[];
    courseResourceId: number;
    resourceTitle: string;
};

export default function ResourceReviewContainer({ criteria, courseResourceId, resourceTitle }: Props) {
    const [dismissed, setDismissed] = useState(false);
    const [submitted, setSubmitted] = useState(false);

    if (dismissed) return null;

    if (submitted) {
        return (
            <div className="rounded-xl border border-green-200 bg-green-50 px-6 py-5">
                <p className="font-medium text-green-700">Review submitted — thanks for the feedback!</p>
            </div>
        );
    }

    return (
        <div className="rounded-xl border border-gray-200 bg-white px-6 py-6 shadow-sm">
            <ReviewForm
                criteria={criteria}
                courseResourceId={courseResourceId}
                resourceTitle={resourceTitle}
                handleClose={() => setDismissed(true)}
                onSuccess={() => setSubmitted(true)}
            />
        </div>
    );
}
