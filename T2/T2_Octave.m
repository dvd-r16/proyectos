pkg load database;
conn = pq_connect (setdbopts ("dbname", "postgres", "host", "localhost", "port", "5432", "user", "postgres", "password", "202010039"));


% ----AGREGAR UN DATO A LA TABLA T202010039----
% pq_exec_params(conn, "INSERT INTO T202010039 (nombre, carnet) VALUES ($1, $2);", {"Juan Perez Octave", 202010043});

% ----ELIMINAR UN DATO DE LA TABLA T202010039----
% pq_exec_params(conn, "DELETE FROM T202010039 WHERE carnet = $1;", {202010040});

% ----ACTUALIZACIÓN DE UN DATO EXISTENTE EN LA TABLA T202010039----
% pq_exec_params(conn, "UPDATE T202010039 SET nombre = $1 WHERE carnet = $2;", {"Luis Angel", 202010037});

N = pq_exec_params (conn, "select * from T202010039;")
