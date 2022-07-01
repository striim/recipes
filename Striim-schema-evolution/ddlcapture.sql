 CREATE TABLE IF NOT EXISTS striim.ddlcapturetable 
  ( 
     event           TEXT, 
     tag             TEXT, 
     classid         OID, 
     objid           OID, 
     objsubid        INT, 
     object_type     TEXT, 
     schema_name     TEXT, 
     object_identity TEXT, 
     is_extension    BOOL, 
     query           TEXT, 
     username        TEXT DEFAULT CURRENT_USER, 
     db_name TEXT DEFAULT Current_database(), 
     client_addr     INET DEFAULT Inet_client_addr(), 
     creation_time   TIMESTAMP DEFAULT now() 
  ); 
GRANT USAGE ON SCHEMA striim TO PUBLIC;
GRANT SELECT, INSERT ON TABLE striim.ddlcapturetable TO PUBLIC;

create or replace function striim.ddl_capture_command() returns event_trigger as $$
declare v1 text;
r record;
begin

    select query into v1 from pg_stat_activity where pid=pg_backend_pid();
    if TG_EVENT='ddl_command_end' then
        SELECT * into r FROM pg_event_trigger_ddl_commands();
        if r.classid > 0 then
            insert into striim.ddlcapturetable(event, tag, classid, objid, objsubid, object_type, schema_name, object_identity, is_extension, query)
            values(TG_EVENT, TG_TAG, r.classid, r.objid, r.objsubid, r.object_type, r.schema_name, r.object_identity, r.in_extension, v1);
         end if;
    end if;
    if TG_EVENT='sql_drop' then
            SELECT * into r FROM pg_event_trigger_dropped_objects();
            insert into striim.ddlcapturetable(event, tag, classid, objid, objsubid, object_type, schema_name, object_identity, is_extension, query)
            values(TG_EVENT, TG_TAG, r.classid, r.objid, r.objsubid, r.object_type, r.schema_name, r.object_identity, 'f', v1);
    end if;
end;
$$ language plpgsql strict;


CREATE EVENT TRIGGER pg_get_ddl_command on ddl_command_end EXECUTE PROCEDURE striim.ddl_capture_command();
CREATE EVENT TRIGGER pg_get_ddl_drop on sql_drop EXECUTE PROCEDURE striim.ddl_capture_command();
