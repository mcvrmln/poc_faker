/*
The purpose of this script is to setup a database in Snowflake with masking policies. 

This script is not intended to run completely top-to-bottom. Some statements undo the statement next above it.

The python script src/main.py fills the table waredax.hattam with some random pii data.

 */
-- Creation of the database
use role sysadmin;
create database volfase;
use database volfase;
create schema waredax;
create schema twilighttube;

-- Creation of the roles and grants
use role securityadmin;
create role beheerder;
grant usage on database volfase to role beheerder;
grant usage on schema volfase.waredax to role beheerder;
grant usage on schema volfase.twilighttube to role beheerder;
GRANT USAGE ON WAREHOUSE compute_wh TO ROLE beheerder;
grant create table on schema volfase.waredax to role beheerder;
grant create table on schema volfase.twilighttube to role beheerder;
grant all privileges on future tables in schema volfase.twilighttube to role beheerder;
grant all privileges on future tables in schema volfase.waredax to role beheerder;
grant all privileges on future tables in schema volfase.twilighttube to role beheerder;
GRANT CREATE MASKING POLICY on SCHEMA volfase.waredax to ROLE beheerder;

-- Apply masking policy is on account level (needs accountadmin)
use role accountadmin;
GRANT APPLY MASKING POLICY on ACCOUNT to ROLE beheerder;

-- Assign role beheerder to an user
use role securityadmin;
grant role beheerder to user maarten;

-- Creation of database objects (tables + masking policy)
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

-- To change a masking policy, you must first unset this
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

-- Apply the policies to the hattam table ()
alter table hattam modify column email set masking policy email_mask;
alter table hattam modify column first_name set masking policy first_name_mask;

-- Creation of the role analist (readonly from tables)
use role securityadmin;
create role analist;
grant usage on database volfase to role analist;
grant usage on schema volfase.waredax to role analist;
revoke usage on schema volfase.waredax to role analist;
grant select on table volfase.waredax.hattam to role analist;
revoke select on all tables in schema volfase.waredax from role analist;
grant select on future tables in schema volfase.waredax to role analist;
revoke select on future tables in schema volfase.waredax from role analist;

grant usage on schema volfase.twilighttube to role analist;
grant select on future tables in schema volfase.twilighttube to role analist;
GRANT USAGE ON WAREHOUSE compute_wh TO ROLE analist;
grant role analist to user maarten;

-- With role beheerder, ctas of the hattam table in twilighttube schema.
use role beheerder;
drop table volfase.twilighttube.hattam;
create table volfase.twilighttube.hattam as
select * 
from volfase.waredax.hattam
;
-- Apply the masking policies in the table twilighttube.hattam with the masking policy in waredax schema.
alter table volfase.twilighttube.hattam modify column email set masking policy volfase.waredax.email_mask;
alter table volfase.twilighttube.hattam modify column first_name set masking policy volfase.waredax.first_name_mask;

-- Just a random word list.
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
