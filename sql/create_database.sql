use role sysadmin;
create database volfase;
use database volfase;

create schema waredax;

create schema twilighttube;

use role securityadmin;
create role beheerder;
grant usage on database volfase to role beheerder;
grant usage on schema volfase.waredax to role beheerder;
grant usage on schema volfase.twilighttube to role beheerder;
GRANT USAGE ON WAREHOUSE compute_wh TO ROLE beheerder;
grant create table on schema volfase.waredax to role beheerder;
grant all privileges on future tables in schema volfase.waredax to role beheerder;
grant create table in schema volfase.waredax to role beheerder;
grant all privileges on future tables in schema volfase.twilighttube to role beheerder;
GRANT CREATE MASKING POLICY on SCHEMA volfase.waredax to ROLE beheerder;

use role accountadmin;
GRANT APPLY MASKING POLICY on ACCOUNT to ROLE beheerder;

use role securityadmin;

grant role beheerder to user maarten;

use role beheerder;
use database volfase;
use schema waredax;

create table hattam (
    id integer primary key autoincrement,
    first_name text,
    last_name text,
    email text,
    random_value text
);

select *
from hattam
limit 100;

alter table hattam modify column email unset masking policy;
CREATE OR REPLACE MASKING POLICY email_mask AS (val string) RETURNS string ->
  CASE
    WHEN CURRENT_ROLE() = 'BEHEERDER' THEN val
    ELSE regexp_replace(val,'.+\@','*****@')
  END;

alter table hattam modify column first_name unset masking policy;
create or replace masking policy first_name_mask as (val string) returns string -> 
    case 
        when current_role() in ('BEHEERDER') then val
        else '********'
    end;

alter table hattam modify column email set masking policy email_mask;
alter table hattam modify column first_name set masking policy first_name_mask;

use role securityadmin;
create role analist;
grant usage on database volfase to role analist;
grant usage on schema volfase.waredax to role analist;
grant usage on schema volfase.twilighttube to role analist;
GRANT USAGE ON WAREHOUSE compute_wh TO ROLE analist;
grant select on table volfase.waredax.hattam to role analist;
grant select on future tables in schema volfase.waredax to role analist;
grant role analist to user maarten;

/*
Volfase
waredax
Twilighttube
Hattam
Vortextales
Doubleing
Dantax
Hogcoms
Forestwell
Mathfix
*/
