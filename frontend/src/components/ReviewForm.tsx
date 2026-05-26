"use client";

import { useForm } from "react-hook-form";
import toast from "react-hot-toast";

import { apiResourcesReviewCreate } from "@/client";
import type { ResourceReviewInRequest } from "@/client";

type ReviewCriterion = {
    id: number;
    name: string;
    prompt: string;
};

type ReviewFormProps = {
    criteria: ReviewCriterion[];
    courseResourceId: number;
    resourceTitle: string;
    handleClose: () => void;
    onSuccess: () => void;
};

export default function ReviewForm({
    criteria,
    courseResourceId,
    resourceTitle,
    handleClose,
    onSuccess,
}: ReviewFormProps) {
    const { register, control, formState, handleSubmit, watch } =
        useForm<ResourceReviewInRequest>();

    const numCommentChar = watch("comments")?.length ?? 0;

    const onSubmit = async (formData: ResourceReviewInRequest) => {
        const { error } = await apiResourcesReviewCreate({
            body: {
                ...formData,
                resource_id: null,
                course_resource_id: courseResourceId,
            },
        });

        if (error) {
            toast.error(JSON.stringify(error));
            return;
        }

        onSuccess();
    };

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex w-full flex-col gap-5"
        >
            <div>
                <p className="text-xs font-medium uppercase tracking-widest text-indigo-500">
                    Rate this resource
                </p>
                <h2 className="mt-0.5 text-base font-semibold text-gray-800">
                    {resourceTitle}
                </h2>
            </div>

            <div className="flex flex-col gap-4">
                {criteria.map((criterion) => (
                    <div key={criterion.name} className="flex items-center justify-between gap-4">
                        <label className="text-sm text-gray-700">{criterion.prompt}</label>
                        <input
                            type="number"
                            min={1}
                            max={5}
                            placeholder="1–5"
                            {...register(criterion.name as keyof ResourceReviewInRequest, {
                                required: true,
                                min: 1,
                                max: 5,
                                valueAsNumber: true,
                            })}
                            className="w-16 rounded-lg border border-gray-300 px-2 py-1.5 text-center text-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100"
                        />
                    </div>
                ))}
            </div>

            <div className="flex flex-col gap-1.5">
                <div className="flex items-center justify-between">
                    <label className="text-sm text-gray-700">
                        Comments <span className="text-gray-400">(optional)</span>
                    </label>
                    <span className={`text-xs ${numCommentChar > 500 ? "text-red-500" : "text-gray-400"}`}>
                        {numCommentChar}/500
                    </span>
                </div>
                <textarea
                    {...register("comments", {
                        maxLength: {
                            value: 500,
                            message: "Comments must be 500 characters or fewer",
                        },
                    })}
                    placeholder="Anything else you'd like to share…"
                    rows={3}
                    className="w-full resize-none rounded-lg border border-gray-300 p-2.5 text-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100"
                />
            </div>

            {formState.isSubmitted && !formState.isValid && (
                <p className="text-sm italic text-red-500">
                    {formState.errors.comments?.message ?? "Please complete all rating fields."}
                </p>
            )}

            <div className="flex items-center justify-end gap-2 border-t border-gray-100 pt-4">
                <button
                    type="button"
                    onClick={handleClose}
                    className="rounded-lg px-4 py-2 text-sm text-gray-500 hover:bg-gray-100"
                >
                    No thanks
                </button>
                <button
                    type="submit"
                    disabled={formState.isSubmitting}
                    className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
                >
                    {formState.isSubmitting ? "Submitting…" : "Submit Review"}
                </button>
            </div>
        </form>
    );
}
