pkg load database;
conn = pq_connect (setdbopts ("dbname", "postgres", "host", "localhost", "port", "5432", "user", "postgres", "password", "Lobodefuego01"));
N = pq_exec_params (conn, "select * from T202010039;")
