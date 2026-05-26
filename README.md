# Full-Stack Developer Interview Challenge

## Context

This is a simplified excerpt from a real production codebase. The stack is:

- **Backend**: Django (Python) with async views via `adrf`, Pydantic-based serializers via `drf-pydantic`, and PostgreSQL
- **Frontend**: Next.js (React/TypeScript) using a type-safe auto-generated SDK

## The Feature

Students can submit a review for a learning resource. The flow is:

1. When a student navigates to a resource page, the frontend sends a `GET` request to `/api/resources/review` with the resource's ID as a query parameter.
2. The backend checks if the student has already reviewed this resource.
   - If yes, returns `204 No Content` — the frontend shows nothing.
   - If no, returns `200 OK` with the review criteria (categories to rate) and the resource title.
3. The frontend renders a form where the student rates each criterion (1–5) and optionally leaves a comment.
4. On submit, the frontend sends a `POST` to `/api/resources/review` with the ratings.
5. On success, a confirmation message is shown.

## Provided Files

| File | Description |
|---|---|
| `backend/reviews/models.py` | Model definitions (read-only context) |
| `backend/reviews/views.py` | The Django API endpoint |
| `frontend/src/components/ResourceReview.tsx` | Top-level React component — fetches review criteria on mount |
| `frontend/src/components/ReviewForm.tsx` | Form component — collects and submits ratings |

## Your Task

The feature has been implemented but **is not working correctly**. Investigate the provided files, identify the bug(s), and fix them.

Be prepared to:

1. Explain what each file does and how they connect
2. Describe the bug(s) you found, why they cause the failure, and what the correct behaviour should be
3. Show the fixed code
4. Walk through how you used any tools (including AI) to investigate

## Notes

- The auto-generated SDK functions (`apiResourcesReviewRetrieve`, `apiResourcesReviewCreate`) match the backend's URL and serializer shape exactly.
- `useSDK` is a `useSWR`-based hook. Its second argument is the params object, which may include `query`, `path`, and `body` keys.
- `request.student_id` on the backend is populated by authentication middleware — treat it as always available.

---

## Setup

**Requirements:** Python 3.11+, Node.js 18+

### Backend

```bash
cd backend
python -m venv venv

# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
```

### Frontend (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000** — it redirects to the resource page automatically.

API docs are available at **http://localhost:8000/api/docs**.

### Resetting the database

To wipe all submitted reviews and start fresh:

```bash
python manage.py flush --no-input && python manage.py seed
```
