-- Create the slabvpn_data database
CREATE DATABASE slabvpn_data;

-- Connect to the slabvpn_data database
\c slabvpn_data;

-- Drop and create tables
DROP TABLE IF EXISTS countries CASCADE;
CREATE TABLE countries (
    id UUID PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

CREATE TABLE cities (
    id UUID PRIMARY KEY,
    name TEXT,
    country_id UUID,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    CONSTRAINT fk_countries_cities FOREIGN KEY (country_id) REFERENCES countries (id)
);

DROP TABLE IF EXISTS providers CASCADE;
CREATE TABLE providers (
    id UUID PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

DROP TABLE IF EXISTS servers CASCADE;
CREATE TABLE servers (
    id UUID PRIMARY KEY,
    name TEXT,
    provider_id UUID,
    location_id UUID,
    location_type TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    CONSTRAINT fk_providers_servers FOREIGN KEY (provider_id) REFERENCES providers (id)
);

DROP TABLE IF EXISTS in_ips CASCADE;
CREATE TABLE in_ips (
    id UUID PRIMARY KEY,
    ip TEXT,
    server_id UUID,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    CONSTRAINT fk_servers_in_ip FOREIGN KEY (server_id) REFERENCES servers (id)
);

DROP TABLE IF EXISTS out_ips CASCADE;
CREATE TABLE out_ips (
    id UUID PRIMARY KEY,
    ip TEXT,
    server_id UUID,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    CONSTRAINT fk_servers_out_ip FOREIGN KEY (server_id) REFERENCES servers (id)
);

-- Create user slabvpn with read permissions
CREATE USER slabvpn WITH PASSWORD '';
GRANT CONNECT ON DATABASE slabvpn_data TO slabvpn;
GRANT USAGE ON SCHEMA public TO slabvpn;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO slabvpn;

-- Ensure future tables grant SELECT to slabvpn
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO slabvpn;
