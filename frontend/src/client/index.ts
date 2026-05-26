export type ResourceReviewInRequest = {
  resource_id: number | null;
  course_resource_id: number | null;
  comments?: string | null;
  clarity: number;
  helpfulness: number;
  relevance: number;
  difficulty: number;
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type ApiResult<T> = { data: T; error?: never } | { data?: never; error: any };

export async function apiResourcesReviewRetrieve(params: {
  query?: { resource_id?: number; course_resource_id?: number };
}): Promise<ApiResult<unknown>> {
  const qs = new URLSearchParams();
  if (params.query?.resource_id != null)
    qs.set("resource_id", String(params.query.resource_id));
  if (params.query?.course_resource_id != null)
    qs.set("course_resource_id", String(params.query.course_resource_id));

  const queryStr = qs.toString();
  const url = `/api/resources/review${queryStr ? `?${queryStr}` : ""}`;
  const res = await fetch(url, { headers: { "Content-Type": "application/json" } });

  if (res.status === 204) return { data: null };
  const json = await res.json();
  return res.ok ? { data: json } : { error: json };
}

export async function apiResourcesReviewCreate(params: {
  body: ResourceReviewInRequest;
}): Promise<ApiResult<unknown>> {
  const res = await fetch("/api/resources/review", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params.body),
  });

  const json = await res.json();
  return res.ok ? { data: json } : { error: json };
}
