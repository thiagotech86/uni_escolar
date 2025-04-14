-- Tabela base para Usuario
CREATE TABLE tb_usuario (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(20)
);

-- Responsável herda de Usuario
CREATE TABLE tb_responsavel (
    cpf VARCHAR(11) PRIMARY KEY,
    profissao VARCHAR(100),
    FOREIGN KEY (cpf) REFERENCES tb_usuario(cpf)
);

-- Professor herda de Usuario
CREATE TABLE tb_professor (
    cpf VARCHAR(11) PRIMARY KEY,
    materia VARCHAR(100),
    FOREIGN KEY (cpf) REFERENCES tb_usuario(cpf)
);

-- Aluno
CREATE TABLE tb_aluno (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100),
    sexo VARCHAR(10),
    dataNascimento DATE,
    cpf_responsavel VARCHAR(11),
    FOREIGN KEY (cpf_responsavel) REFERENCES tb_responsavel(cpf)
);

-- PacoteHora
CREATE TABLE tb_pacotehora (
    id INTEGER PRIMARY KEY,
    horasContratadas INTEGER,
    valorHora INTEGER,
    saldo INTEGER,
    cpf_responsavel VARCHAR(11),
    FOREIGN KEY (cpf_responsavel) REFERENCES tb_responsavel(cpf)
);

-- Aula
CREATE TABLE tb_aula (
    id INTEGER PRIMARY KEY,
    numero INTEGER,
    local VARCHAR(100),
    disciplina VARCHAR(100),
    dataInicio DATE,
    horaInicio TIME,
    horaFim TIME,
    id_aluno INTEGER,
    cpf_professor VARCHAR(11),
    FOREIGN KEY (id_aluno) REFERENCES tb_aluno(id),
    FOREIGN KEY (cpf_professor) REFERENCES tb_professor(cpf)
);


-- Insere informações no Banco

-- Inserindo usuários (responsáveis)
INSERT INTO tb_usuario (cpf, nome, email, telefone) VALUES
(11111111111, 'Maria Silva', 'maria@email.com', '11999999999'),
(22222222222, 'João Costa', 'joao@email.com', '11888888888');

-- Inserindo responsáveis (herdam de Usuario)
INSERT INTO tb_responsavel (cpf, profissao) VALUES
(11111111111, 'Advogada'),
(22222222222, 'Engenheiro');

-- Inserindo alunos (1 do responsável 1, 2 do responsável 2)
INSERT INTO tb_aluno (id, nome, sexo, dataNascimento, cpf_responsavel) VALUES
(1, 'Lucas Silva', 'M', '2012-04-15', 11111111111),
(2, 'Ana Costa', 'F', '2013-06-10', 22222222222),
(3, 'Pedro Costa', 'M', '2011-09-22', 22222222222);

-- Inserindo pacotes de hora (um para cada responsável)
INSERT INTO tb_pacoteHora (id, horasContratadas, valorHora, saldo, cpf_responsavel) VALUES
(1, 10, 50, 5, 11111111111),
(2, 20, 45, 12, 22222222222);

-- Inserindo usuários (professores)
INSERT INTO tb_usuario (cpf, nome, email, telefone) VALUES
(33333333333, 'Carlos Lima', 'carlos@email.com', '11777777777'),
(44444444444, 'Fernanda Dias', 'fernanda@email.com', '11666666666'),
(55555555555, 'Ricardo Alves', 'ricardo@email.com', '11555555555');

-- Inserindo professores
INSERT INTO tb_professor (cpf, materia) VALUES
(33333333333, 'Matemática'),
(44444444444, 'Português'),
(55555555555, 'Inglês');

-- Inserindo aulas
INSERT INTO tb_aula (id, numero, local, disciplina, dataInicio, horaInicio, horaFim, id_aluno, cpf_professor) VALUES
(1, 101, 'A distancia', 'Matemática', '2024-04-10', '14:00', '15:00', 1, 33333333333),
(2, 102, 'Presencial', 'Português',  '2024-04-11', '10:00', '11:00', 2, 44444444444),
(3, 103, 'Presencial', 'Inglês',     '2024-04-12', '16:00', '17:00', 3, 55555555555);
