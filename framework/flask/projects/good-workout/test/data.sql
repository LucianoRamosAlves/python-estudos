INSERT INTO usuario (nome_usuario, senha_usuario)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, descricao, author_id, created_at, image_url)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00', https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStyE_OeQb5PWvivVMqLOwbkuFobmbtVOKa0ibQ7s8nfO1UUgXu8IQU1ZM7CvurJUrQYf6H2VMkoOnqak_yerbBW5qcVKXIkw6m00svKb6L&s=10);