CREATE DATABASE slabvpn_data;
CREATE DATABASE slabvpn_django;

\c slabvpn_data;

DROP TABLE IF EXISTS countries CASCADE;
CREATE TABLE countries (
    id UUID PRIMARY KEY,
    name TEXT,
    created_at BIGINT,
    updated_at BIGINT
);

CREATE TABLE cities (
    id UUID PRIMARY KEY,
    name TEXT,
    country_id UUID,
    created_at BIGINT,
    updated_at BIGINT,
    CONSTRAINT fk_countries_cities FOREIGN KEY (country_id) REFERENCES countries (id)
);

DROP TABLE IF EXISTS providers CASCADE;
CREATE TABLE providers (
    id UUID PRIMARY KEY,
    name TEXT,
    created_at BIGINT,
    updated_at BIGINT
);

DROP TABLE IF EXISTS servers CASCADE;
CREATE TABLE servers (
    id UUID PRIMARY KEY,
    name TEXT,
    provider_id UUID,
    location_id UUID,
    location_type TEXT,
    is_active BOOLEAN,
    created_at BIGINT,
    updated_at BIGINT,
    CONSTRAINT fk_providers_servers FOREIGN KEY (provider_id) REFERENCES providers (id)
);

DROP TABLE IF EXISTS in_ips CASCADE;
CREATE TABLE in_ips (
    id UUID PRIMARY KEY,
    ip TEXT,
    server_id UUID,
    created_at BIGINT,
    updated_at BIGINT,
    CONSTRAINT fk_servers_in_ip FOREIGN KEY (server_id) REFERENCES servers (id)
);

DROP TABLE IF EXISTS ip_reflectors CASCADE;
CREATE TABLE ip_reflectors (
    id UUID PRIMARY KEY,
    reflector_type TEXT,
    name TEXT,
    created_at BIGINT,
    updated_at BIGINT
);

DROP TABLE IF EXISTS out_ips CASCADE;
CREATE TABLE out_ips (
    id UUID PRIMARY KEY,
    ip TEXT,
    server_id UUID,
    ip_reflector_id UUID,
    created_at BIGINT,
    updated_at BIGINT,
    CONSTRAINT fk_servers_out_ip FOREIGN KEY (server_id) REFERENCES servers (id),
    CONSTRAINT fk_ip_reflectors_out_ip FOREIGN KEY (ip_reflector_id) REFERENCES ip_reflectors (id)
);


CREATE USER slabber_django WITH PASSWORD '';
ALTER DATABASE slabvpn_django OWNER TO slabber_django;
REVOKE CONNECT ON DATABASE slabvpn_data FROM slabber_django;
GRANT ALL PRIVILEGES ON DATABASE slabvpn_django TO slabber_django;

GRANT ALL ON SCHEMA public TO slabber_django;
GRANT CREATE ON SCHEMA public TO slabber_django;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO slabber_django;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO slabber_django;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO slabber_django;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO slabber_django;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO slabber_django;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO slabber_django;

CREATE USER slabber_data WITH PASSWORD '';
GRANT CONNECT ON DATABASE slabvpn_data TO slabber_data;
REVOKE CONNECT ON DATABASE slabvpn_django FROM slabber_data;
GRANT USAGE ON SCHEMA public TO slabber_data;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO slabber_data;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO slabber_data;
