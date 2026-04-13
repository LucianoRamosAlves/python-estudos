create database if not exists bom_treino;


drop table if exists checkins;
drop table if exists fotos;
drop table if exists evolucao;
drop table if exists treinos;
drop table if exists  usuario;

create table usuario (
    id int auto_increment primary key,
    nome_usuario varchar(100) unique not null,
    senha_usuario varchar(255) not null
);

create table treinos (
    id int auto_increment primary key,
    nome_treino varchar(100) not null,
    descricao text,
    usuario_id int not null,
    foreign key (usuario_id) references usuario(id) on delete cascade
);

create table checkins (
    id int auto_increment primary key,
    data_checkins date not null,
    treino_id int not null,
    usuario_id int not null,
    completado boolean default false,
    foreign key (treino_id) references treinos(id) on delete cascade
);

create table evolucao (
    id int auto_increment primary key,
    checkin_id int not null,
    exercicio varchar(100) not null,
    peso decimal(5,2),
    repeticoes int,
    observacoes text,
    foreign key (checkin_id) references checkins(id) on delete cascade
);

create table fotos (
    id int auto_increment primary key,
    checkin_id int not null,
    url varchar(255) not null,
    data_foto date not null,
    descricao text,
    foreign key (checkin_id) references checkins(id) on delete cascade
);