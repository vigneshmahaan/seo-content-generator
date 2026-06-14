-- Supabase schema for SEO Content Generator

-- seo_requests
create table if not exists public.seo_requests (
  id serial primary key,
  input_one text not null,
  input_two text not null,
  input_three text,
  status text not null default 'Pending',
  provider_used text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- seo_contents
create table if not exists public.seo_contents (
  id serial primary key,
  request_id integer references public.seo_requests(id) on delete cascade,
  generated_content text not null,
  generated_at timestamptz default now()
);

-- system_logs
create table if not exists public.system_logs (
  id serial primary key,
  request_id integer references public.seo_requests(id),
  log_type text not null,
  message text not null,
  provider text,
  created_at timestamptz default now()
);

create index if not exists idx_seo_contents_generated_at on public.seo_contents (generated_at);
