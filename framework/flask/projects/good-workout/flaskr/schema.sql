

DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS treinos;
DROP TABLE IF EXISTS usuario;

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



create table posts (
    id int auto_increment primary key,
    author_id int not null,
    image_url varchar(255) not null,
    title Text not null,
    created_at datetime not null default current_timestamp,
    descricao text,
    foreign key (author_id) references usuario(id) on delete cascade
);