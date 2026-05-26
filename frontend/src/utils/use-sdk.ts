import useSWR from "swr";

type SDKResult<T> = { data?: T; error?: unknown };
type SDKFn<TParams, TData> = (params: TParams) => Promise<SDKResult<TData>>;

export function useSDK<TParams, TData>(fn: SDKFn<TParams, TData>, params: TParams) {
  const key = [fn.name, JSON.stringify(params)];
  const { data: result, error: swrError } = useSWR<SDKResult<TData>>(key, () =>
    fn(params)
  );

  return {
    data: result?.data,
    error: result?.error ?? swrError,
    isLoading: !result && !swrError,
  };
}
