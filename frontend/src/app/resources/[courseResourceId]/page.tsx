import ResourceReview from "@/components/ResourceReview";

export default function ResourcePage() {
    return (
        <main className="mx-auto max-w-2xl px-4 py-12">
            <div className="mb-2 text-xs font-medium uppercase tracking-widest text-indigo-500">
                Course Material
            </div>
            <h1 className="mb-1 text-2xl font-semibold text-gray-900">Introduction to Machine Learning</h1>
            <p className="mb-8 text-sm text-gray-500">
                A comprehensive introduction to ML concepts, algorithms, and practical applications.
            </p>
            <ResourceReview />
        </main>
    );
}
