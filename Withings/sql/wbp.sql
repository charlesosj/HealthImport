-- Table: data.wbp

-- DROP TABLE IF EXISTS data.wbp;

CREATE TABLE IF NOT EXISTS data.wbp
(
    date timestamp without time zone,
    heartrate integer,
    systolic integer,
    diastolic integer,
    hash character varying(100) COLLATE pg_catalog."default",
    comments text COLLATE pg_catalog."default",
    CONSTRAINT wbp_hash_unique UNIQUE (hash)
)

TABLESPACE pg_default;

-- Index: idx_wbp_covering

-- DROP INDEX IF EXISTS data.idx_wbp_covering;

CREATE INDEX IF NOT EXISTS idx_wbp_covering
    ON data.wbp USING btree
    (date ASC NULLS LAST, heartrate ASC NULLS LAST, systolic ASC NULLS LAST, diastolic ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_wbp_date

-- DROP INDEX IF EXISTS data.idx_wbp_date;

CREATE INDEX IF NOT EXISTS idx_wbp_date
    ON data.wbp USING btree
    (date ASC NULLS LAST)
    TABLESPACE pg_default;