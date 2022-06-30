SELECT * FROM pg_create_logical_replication_slot('strim_slot','wal2json');

SELECT slot_name,plugin,slot_type,database,active,restart_lan,confirmed_flush_lsn
FROM pg_replication_slots;
