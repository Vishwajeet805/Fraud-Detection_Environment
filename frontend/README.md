# Fraud Decision Intelligence UI

Production-style multi-page SaaS frontend built with React + Vite, Tailwind CSS, Framer Motion, and Recharts.

## Run

```bash
cd frontend
npm install
npm run dev
```

The UI is structured for backend integration against:

- `POST /reset`
- `POST /step`

via `src/lib/api.ts`.
