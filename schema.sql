-- PATENTS TABLE
CREATE TABLE patents (
    patent_id TEXT,
    patent_title TEXT,
    patent_date TEXT,
    year INTEGER
);

-- ABSTRACTS TABLE
CREATE TABLE abstracts (
    patent_id TEXT,
    abstract TEXT
);

-- INVENTORS TABLE
CREATE TABLE inventors (
    patent_id TEXT,
    inventor_id TEXT,
    name TEXT,
    location_id TEXT
);

-- COMPANIES TABLE
CREATE TABLE companies (
    patent_id TEXT,
    company_id TEXT,
    company_name TEXT
);

-- LOCATIONS TABLE
CREATE TABLE locations (
    location_id TEXT,
    country TEXT
);

-- RELATIONSHIPS TABLE
CREATE TABLE relationships (
    patent_id TEXT,
    inventor_id TEXT,
    name TEXT,
    location_id TEXT,
    company_id TEXT,
    company_name TEXT
);