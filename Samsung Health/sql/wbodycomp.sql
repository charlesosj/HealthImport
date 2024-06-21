-- Table: stress

-- DROP TABLE IF EXISTS stress;

CREATE TABLE IF NOT EXISTS stress
(
    create_sh_ver integer,
    start_time timestamp without time zone,
    custom text COLLATE pg_catalog."default",
    binning_data text COLLATE pg_catalog."default",
    tag_id integer,
    modify_sh_ver integer,
    update_time timestamp without time zone,
    create_time timestamp without time zone,
    max numeric,
    min numeric,
    score numeric,
    algorithm integer,
    time_offset text COLLATE pg_catalog."default",
    deviceuuid text COLLATE pg_catalog."default",
    comment text COLLATE pg_catalog."default",
    pkg_name text COLLATE pg_catalog."default",
    end_time timestamp without time zone,
    hash character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT stress_hash_unique UNIQUE (hash)
)

TABLESPACE pg_default;


-- Index: idx_stress_covering

-- DROP INDEX IF EXISTS idx_stress_covering;

CREATE INDEX IF NOT EXISTS idx_stress_covering
    ON stress USING btree
    (start_time ASC NULLS LAST, max ASC NULLS LAST, min ASC NULLS LAST, score ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_stress_start_time

-- DROP INDEX IF EXISTS idx_stress_start_time;

CREATE INDEX IF NOT EXISTS idx_stress_start_time
    ON stress USING btree
    (start_time ASC NULLS LAST)
    TABLESPACE pg_default;