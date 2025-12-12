import pandas as pd
import os
import uuid 

# --- CONFIGURAÇÃO INICIAL (Constantes) ---
DATA_FILE = 'dados_alunos.csv'

# Estrutura do DataFrame
COLUNAS_DB = [
    'Matricula', 'Nome', 'Rua', 'Numero', 'Bairro', 
    'Cidade', 'UF', 'Telefone', 'e-mail'
]

# Variável global para manter o DataFrame em memória.
global db_alunos 
db_alunos = None

# --- FUNÇÕES DE UTILIDADE DE ARQUIVO ---

def load_db_or_create_new():
    """Tenta carregar o DataFrame do CSV. Se não existir, cria um vazio."""
    global db_alunos
    
    try:
        db_alunos = pd.read_csv(DATA_FILE)
        print(f"Dados carregados do arquivo '{DATA_FILE}'.")
    except FileNotFoundError:
        db_alunos = pd.DataFrame(columns=COLUNAS_DB)
        print(f"Arquivo '{DATA_FILE}' não encontrado. Criando novo banco de dados.")

def save_current_db():
    """Grava o estado atual do DataFrame de volta no disco."""
    global db_alunos
    try:
        db_alunos.to_csv(DATA_FILE, index=False)
        print("Dados salvos com sucesso no disco.")
    except Exception as err:
        print(f"Erro ao salvar dados: {err}")

# --- FUNÇÕES DO CRUD ---

def display_main_menu():
    """Exibe o menu principal e coleta a escolha do usuário."""
    print("\n" + "~"*35)
    print("Gerenciador de Alunos Simples")
    print("~"*35)
    print("1 -> INSERIR novo aluno")
    print("2 -> PESQUISAR/EDITAR/REMOVER")
    print("3 -> SAIR do programa")
    print("~"*35)
    
    choice = input("Sua opção: ").strip()
    return choice

def insert_new_student():
    """Coleta os dados do novo aluno, gera a matrícula e anexa ao DataFrame."""
    global db_alunos
    print("\n--- INSERÇÃO ---")

    temp_data = {}
    
    # Gera uma Matrícula única de 8 caracteres.
    matricula_gerada = str(uuid.uuid4())[:8].upper()
    temp_data['Matricula'] = matricula_gerada
    print(f"Matrícula gerada automaticamente: {matricula_gerada}")
    
    fields_to_ask = COLUNAS_DB[1:]
    
    for field in fields_to_ask:
        user_input = input(f"Informe {field.capitalize()}: ")
        temp_data[field] = user_input.strip()
        
    record_df = pd.DataFrame([temp_data], columns=COLUNAS_DB)
    db_alunos = pd.concat([db_alunos, record_df], ignore_index=True)
    
    print(f"\nAluno '{temp_data['Nome']}' inserido.")
    save_current_db()

def search_student(search_term):
    """Busca um aluno por Matrícula ou Nome (case-insensitive)."""
    term_lower = search_term.lower().strip()
    
    if db_alunos.empty:
        return db_alunos

    # 1. Busca por Matrícula exata
    mask_matricula = db_alunos['Matricula'].astype(str).str.lower() == term_lower
    
    # 2. Busca por Nome (contenção de texto)
    mask_nome = db_alunos['Nome'].astype(str).str.lower().str.contains(term_lower, na=False)

    # Combina as máscaras (OR lógico)
    results = db_alunos[mask_matricula | mask_nome]
    
    return results

def edit_student_data(matricula):
    """Permite ao usuário editar um único campo específico do aluno."""
    global db_alunos
    
    try:
        # Obtendo o índice da linha a ser modificada.
        idx_to_edit = db_alunos[db_alunos['Matricula'] == matricula].index[0]
    except IndexError:
        print("Erro interno: Matrícula não encontrada.")
        return

    while True:
        print("\n--- EDIÇÃO DE CAMPO ESPECÍFICO ---")
        editable_fields = COLUNAS_DB[1:]
        
        for i, field in enumerate(editable_fields):
            current_value = db_alunos.loc[idx_to_edit, field]
            print(f"[{i + 1}] {field}: {current_value}")
            
        print("[0] CONCLUIR EDIÇÃO")
        
        choice = input("Selecione o número do campo para alterar (0 para sair): ").strip()
        
        if choice == '0':
            print("Edição finalizada.")
            save_current_db()
            break
            
        try:
            field_index = int(choice) - 1
            if 0 <= field_index < len(editable_fields):
                selected_field = editable_fields[field_index]
                new_value = input(f"Novo valor para '{selected_field}': ").strip()
                db_alunos.loc[idx_to_edit, selected_field] = new_value
                print(f"'{selected_field}' atualizado.")
            else:
                print("Opção fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")


def delete_student(matricula):
    """Remove um registro do banco de dados após a confirmação."""
    global db_alunos
    
    confirm = input(
        f"CONFIRMA REMOÇÃO PERMANENTE do aluno {matricula}? Digite 'SIM' para prosseguir: "
    ).upper().strip()
    
    if confirm == 'SIM':
        # Filtra o DataFrame, excluindo a linha da matrícula alvo e resetando o índice.
        db_alunos = db_alunos[db_alunos['Matricula'] != matricula].reset_index(drop=True)
        print(f"Registro {matricula} REMOVIDO.")
        save_current_db()
    else:
        print("Ação de REMOÇÃO CANCELADA pelo usuário.")


def search_and_manage_flow():
    """Gerencia as sub-opções (Pesquisar, Editar, Remover)."""
    global db_alunos
    
    if db_alunos.empty:
        print("DB vazio. Insira um aluno primeiro.")
        return

    search_term = input("Pesquisar por Matrícula ou Nome: ").strip()
    results = search_student(search_term)
    
    if results.empty:
        print(f"Nenhum aluno encontrado com o termo '{search_term}'.")
        return
    
    print("\n--- RESULTADOS ---")
    print(results.to_string(index=False))

    # Só permite edição/remoção se houver um único resultado.
    if len(results) == 1:
        target_matricula = results['Matricula'].iloc[0]
        target_name = results['Nome'].iloc[0]
        
        print(f"\nAluno selecionado: {target_name} ({target_matricula})")
        print("[E] Editar")
        print("[R] Remover")
        print("[C] Cancelar")
        
        action = input("Escolha a ação: ").lower().strip()
        
        if action == 'e':
            edit_student_data(target_matricula)
        elif action == 'r':
            delete_student(target_matricula)
        elif action == 'c':
            print("Ação cancelada.")
        else:
            print("Opção inválida, voltando ao menu principal.")
            
    elif len(results) > 1:
        print("Múltiplos resultados encontrados. Use a Matrícula para garantir a edição/remoção correta.")


# --- FUNÇÃO PRINCIPAL DE EXECUÇÃO ---

def main_program():
    """Inicia o banco de dados e gerencia o loop principal do programa."""
    
    load_db_or_create_new()

    keep_running = True 
    
    while keep_running:
        choice = display_main_menu()
        
        if choice == '1':
            insert_new_student()
        elif choice == '2':
            search_and_manage_flow()
        elif choice == '3':
            keep_running = False
            print("\nFechando o sistema.")
            save_current_db() 
        else:
            print(f"'{choice}' não é uma opção válida. Tente novamente.")

# Execução do script.
if __name__ == '__main__':
    main_program()
