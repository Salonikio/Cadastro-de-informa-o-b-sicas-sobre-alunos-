# 🎓 Sistema de Cadastro e Gerenciamento de Alunos

## 📝 Descrição Rápida

Este é um sistema CRUD (Criar, Ler, Atualizar e Deletar) simples para gerenciar informações de alunos via linha de comando.

**Funções Principais:**
* **Armazenamento:** Utiliza a biblioteca Pandas para persistir todos os dados em um arquivo CSV (`dados_alunos.csv`), garantindo que os dados sejam salvos após cada alteração e carregados ao iniciar o programa.
* **Recursos:** Oferece as opções de INSERIR novo aluno (com matrícula automática), PESQUISAR por nome ou matrícula, EDITAR qualquer dado e REMOVER um aluno.

---

## 👨‍💻 Desenvolvedor

* [**Arthur Salonikio Habib**]

* ## ⚙️ Instalação e Configuração

O único requisito do sistema é a biblioteca `pandas`.

### 1. Instalar Pandas

Abra o Terminal (ou Terminal do VS Code) e execute o comando:

```bash
pip install pandas

```
Se o comando acima falhar, use este comando alternativo:

```bash
python -m pip install pandas

```

## 🚀 Uso e Comandos de Execução

### 1. Inicialização do Programa

Execute o programa no Terminal:

```bash
python cadastro_alunos.py

```

### 2. Exemplos de Interação no Menu

O programa funciona em um *loop* contínuo com base nas escolhas do usuário:

| Comando | Descrição |
| :---: | :--- |
| **1** | **INSERIR NOVO ALUNO.** O sistema pedirá Nome, Rua, Bairro, etc., e gerará a Matrícula automaticamente. |
| **2** | **PESQUISAR/GERENCIAR.** Permite que o usuário digite um termo de busca (Nome ou Matrícula). Se o aluno for encontrado, o sistema perguntará: `[E] Editar`, `[R] Remover` ou `[C] Cancelar`. |
| **3** | **SAIR.** Encerra o programa e garante que a última versão do banco de dados (`dados_alunos.csv`) seja salva. |











