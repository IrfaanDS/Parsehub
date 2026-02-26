-- ParseHub Production Database Schema (PostgreSQL)

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    token TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    owner_email TEXT,
    main_site TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Metadata table
CREATE TABLE IF NOT EXISTS metadata (
    id SERIAL PRIMARY KEY,
    personal_project_id TEXT UNIQUE NOT NULL,
    project_id INTEGER REFERENCES projects(id),
    project_token TEXT UNIQUE,
    project_name TEXT NOT NULL,
    last_run_date TIMESTAMP,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    region TEXT,
    country TEXT,
    brand TEXT,
    website_url TEXT,
    total_pages INTEGER,
    total_products INTEGER,
    current_page_scraped INTEGER DEFAULT 0,
    current_product_scraped INTEGER DEFAULT 0,
    last_known_url TEXT,
    import_batch_id INTEGER,
    status TEXT DEFAULT 'pending'
);

-- Runs table
CREATE TABLE IF NOT EXISTS runs (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    run_token TEXT UNIQUE NOT NULL,
    status TEXT,
    pages_scraped INTEGER DEFAULT 0,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds INTEGER,
    records_count INTEGER DEFAULT 0,
    data_file TEXT,
    is_empty BOOLEAN DEFAULT false,
    is_continuation BOOLEAN DEFAULT false,
    completion_percentage REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scraped records
CREATE TABLE IF NOT EXISTS scraped_records (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    run_token TEXT NOT NULL,
    page_number INTEGER,
    data_hash TEXT,
    data_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(run_token, page_number, data_hash)
);

-- Analytics cache
CREATE TABLE IF NOT EXISTS analytics_cache (
    id SERIAL PRIMARY KEY,
    project_token TEXT UNIQUE NOT NULL,
    run_token TEXT,
    total_records INTEGER DEFAULT 0,
    total_fields INTEGER DEFAULT 0,
    total_runs INTEGER DEFAULT 0,
    completed_runs INTEGER DEFAULT 0,
    progress_percentage REAL DEFAULT 0,
    status TEXT,
    analytics_json TEXT,
    stored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_metadata_region ON metadata(region);
CREATE INDEX IF NOT EXISTS idx_metadata_country ON metadata(country);
CREATE INDEX IF NOT EXISTS idx_metadata_brand ON metadata(brand);
CREATE INDEX IF NOT EXISTS idx_runs_project_id ON runs(project_id);
CREATE INDEX IF NOT EXISTS idx_scraped_records_run_token ON scraped_records(run_token);
