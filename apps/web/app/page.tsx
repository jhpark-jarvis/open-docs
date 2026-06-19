export default function HomePage() {
  return (
    <main className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top,_rgba(255,219,153,0.24),_transparent_36%),linear-gradient(180deg,#f8f4ec_0%,#f2ede4_100%)] text-slate-900">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col justify-center px-6 py-16 lg:px-10">
        <section className="grid gap-10 rounded-[2rem] border border-white/60 bg-white/70 p-8 shadow-[0_30px_120px_rgba(15,23,42,0.10)] backdrop-blur md:p-12 lg:grid-cols-[1.25fr_0.75fr]">
          <div className="space-y-6">
            <p className="inline-flex rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-amber-800">
              OpenDocs scaffold
            </p>
            <div className="space-y-4">
              <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl lg:text-6xl">
                A clean foundation for MapleStory event documentation.
              </h1>
              <p className="max-w-2xl text-base leading-7 text-slate-600 sm:text-lg">
                This monorepo is ready for the Next.js App Router, TypeScript, and Tailwind CSS
                frontend while the FastAPI backend, PostgreSQL layer, and future review flow are
                assembled behind the scenes.
              </p>
            </div>
            <div className="flex flex-wrap gap-3 text-sm font-medium">
              <span className="rounded-full bg-slate-900 px-4 py-2 text-white">App Router</span>
              <span className="rounded-full bg-slate-100 px-4 py-2 text-slate-700">
                TypeScript
              </span>
              <span className="rounded-full bg-slate-100 px-4 py-2 text-slate-700">
                Tailwind CSS
              </span>
            </div>
          </div>

          <aside className="grid gap-4 rounded-[1.5rem] border border-slate-200 bg-slate-50 p-5">
            <div className="rounded-2xl bg-white p-5 shadow-sm">
              <p className="text-sm font-semibold text-slate-500">Backend</p>
              <p className="mt-2 text-lg font-medium text-slate-900">FastAPI + SQLAlchemy 2.0</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                Structured for migrations, settings, services, and future ECS deployment.
              </p>
            </div>
            <div className="rounded-2xl bg-white p-5 shadow-sm">
              <p className="text-sm font-semibold text-slate-500">Data Flow</p>
              <p className="mt-2 text-lg font-medium text-slate-900">
                Nexon notices -&gt; OCR -&gt; JSON -&gt; Markdown
              </p>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                The pipeline is scaffolded now so feature work can plug in cleanly later.
              </p>
            </div>
          </aside>
        </section>
      </div>
    </main>
  );
}
