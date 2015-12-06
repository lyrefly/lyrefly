drop table if exists users;
drop table if exists user_sessions;

create table users (
  id bigint auto_increment,
  username varchar(100) not null unique,
  email varchar(255) not null unique,
  password tinytext not null,
  salt tinytext not null,
  primary key(id)
);

create table user_sessions (
  user_id bigint,
  session_id varchar(255) not null,
  primary key(user_id, session_id)
);
