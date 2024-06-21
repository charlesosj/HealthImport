-- Table: data.wbodycomp

-- DROP TABLE IF EXISTS data.wbodycomp;

CREATE TABLE IF NOT EXISTS wbodycomp
(
    date timestamp without time zone,
    weight numeric(5,2),
    fatmass numeric(5,2),
    bonemass numeric(5,2),
    musclemass numeric(5,2),
    hydration numeric(5,2),
    hash character varying(100) COLLATE pg_catalog."default",
    comments text COLLATE pg_catalog."default",
    CONSTRAINT wbodycomp_hash_unique UNIQUE (hash)
)

TABLESPACE pg_default;

-- Index: idx_wbodycomp_covering

-- DROP INDEX IF EXISTS data.idx_wbodycomp_covering;

CREATE INDEX IF NOT EXISTS idx_wbodycomp_covering
    ON wbodycomp USING btree
    (date ASC NULLS LAST, weight ASC NULLS LAST, fatmass ASC NULLS LAST, bonemass ASC NULLS LAST, musclemass ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_wbodycomp_date

-- DROP INDEX IF EXISTS data.idx_wbodycomp_date;

CREATE INDEX IF NOT EXISTS idx_wbodycomp_date
    ON wbodycomp USING btree
    (date ASC NULLS LAST)
    TABLESPACE pg_default;