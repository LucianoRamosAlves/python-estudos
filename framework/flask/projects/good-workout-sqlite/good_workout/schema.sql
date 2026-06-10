DROP TABLE IF EXISTS progresso;
DROP TABLE IF EXISTS exercicios;
DROP TABLE IF EXISTS contato_mensagens;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS treinos;
DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT UNIQUE NOT NULL,
    senha_usuario TEXT NOT NULL
);

CREATE TABLE treinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_treino TEXT NOT NULL,
    descricao TEXT,
    categoria TEXT DEFAULT 'geral',
    usuario_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario (id) ON DELETE CASCADE
);

CREATE TABLE exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    treino_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    series INTEGER DEFAULT 3,
    repeticoes TEXT DEFAULT '12',
    carga TEXT DEFAULT '',
    observacao TEXT DEFAULT '',
    ordem INTEGER DEFAULT 0,
    FOREIGN KEY (treino_id) REFERENCES treinos (id) ON DELETE CASCADE
);

CREATE TABLE progresso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    data_registro DATE NOT NULL DEFAULT (date('now')),
    peso DECIMAL(5,2) DEFAULT NULL,
    altura DECIMAL(5,2) DEFAULT NULL,
    braco_esquerdo DECIMAL(5,2) DEFAULT NULL,
    braco_direito DECIMAL(5,2) DEFAULT NULL,
    peito DECIMAL(5,2) DEFAULT NULL,
    cintura DECIMAL(5,2) DEFAULT NULL,
    quadril DECIMAL(5,2) DEFAULT NULL,
    coxa_esquerda DECIMAL(5,2) DEFAULT NULL,
    coxa_direita DECIMAL(5,2) DEFAULT NULL,
    observacao TEXT DEFAULT '',
    FOREIGN KEY (usuario_id) REFERENCES usuario (id) ON DELETE CASCADE
);

CREATE TABLE contato_mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    assunto TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    resposta TEXT DEFAULT NULL,
    lida INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario (id) ON DELETE CASCADE
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    title TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descricao TEXT,
    FOREIGN KEY (author_id) REFERENCES usuario (id) ON DELETE CASCADE
);

