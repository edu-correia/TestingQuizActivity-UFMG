import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# Teste 1: Validação de pontos inválidos na criação da questão.
def test_create_question_with_invalid_points_raises_exception():
    """Verifica se a criação de uma questão com pontos fora do intervalo (1-100) levanta uma exceção."""
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='Valid title', points=0)
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='Valid title', points=101)

# Teste 2: Adicionar múltiplas alternativas e verificar se os IDs são sequenciais.
def test_add_multiple_choices_generates_sequential_ids():
    """Testa se a adição de múltiplas alternativas gera IDs incrementais e corretos."""
    question = Question(title='Question with multiple choices')
    choice1 = question.add_choice('First choice')
    choice2 = question.add_choice('Second choice')
    choice3 = question.add_choice('Third choice')

    assert len(question.choices) == 3
    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3

# Teste 3: Remover uma alternativa existente pelo seu ID.
def test_remove_existing_choice_by_id():
    """Verifica se uma alternativa específica é corretamente removida da lista de alternativas."""
    question = Question(title='Question about removing choices')
    question.add_choice('Choice A')
    choice_to_remove = question.add_choice('Choice B')
    question.add_choice('Choice C')
    
    assert len(question.choices) == 3
    
    question.remove_choice_by_id(choice_to_remove.id)
    
    assert len(question.choices) == 2
    # Garante que a alternativa removida não está mais na lista.
    assert choice_to_remove not in question.choices
    # Garante que o ID removido não está mais presente.
    assert choice_to_remove.id not in [c.id for c in question.choices]

# Teste 4: Tentar remover uma alternativa com um ID que não existe.
def test_remove_non_existent_choice_raises_exception():
    """Testa se tentar remover uma alternativa com um ID inválido levanta uma exceção."""
    question = Question(title='Question with one choice')
    question.add_choice('Only choice')

    with pytest.raises(Exception, match='Invalid choice id 99'):
        question.remove_choice_by_id(99)

# Teste 5: Remover todas as alternativas de uma vez.
def test_remove_all_choices():
    """Verifica se todas as alternativas são removidas quando o método `remove_all_choices` é chamado."""
    question = Question(title='Question to clear')
    question.add_choice('Choice 1')
    question.add_choice('Choice 2')
    
    assert len(question.choices) == 2
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

# Teste 6: Definir a alternativa correta e verificar se seu status foi atualizado.
def test_set_correct_choices_updates_status():
    """Testa se o status 'is_correct' de uma alternativa é atualizado corretamente."""
    question = Question(title='Which is correct?')
    choice1 = question.add_choice('A')
    choice2 = question.add_choice('B')

    assert not choice1.is_correct
    assert not choice2.is_correct
    
    question.set_correct_choices([choice2.id])
    
    assert not choice1.is_correct
    assert choice2.is_correct

# Teste 7: "Corrigir" uma questão selecionando a alternativa correta.
def test_correct_selected_choices_with_correct_answer():
    """Verifica se a correção retorna o ID da alternativa correta quando a seleção está certa."""
    question = Question(title='Simple correct question')
    question.add_choice('Wrong')
    correct_choice = question.add_choice('Correct', is_correct=True)
    
    result = question.correct_selected_choices([correct_choice.id])
    
    assert result == [correct_choice.id]

# Teste 8: "Corrigir" uma questão selecionando a alternativa incorreta.
def test_correct_selected_choices_with_incorrect_answer():
    """Verifica se a correção retorna uma lista vazia quando a seleção está errada."""
    question = Question(title='Simple incorrect question')
    wrong_choice = question.add_choice('Wrong')
    question.add_choice('Correct', is_correct=True)
    
    result = question.correct_selected_choices([wrong_choice.id])
    
    assert result == []

# Teste 9: Tentar "corrigir" uma questão selecionando mais alternativas do que o permitido.
def test_selecting_more_than_max_selections_raises_exception():
    """Testa se uma exceção é levantada ao selecionar mais alternativas do que `max_selections` permite."""
    question = Question(title='Multi-choice question', max_selections=1)
    choice1 = question.add_choice('A')
    choice2 = question.add_choice('B')
    
    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.correct_selected_choices([choice1.id, choice2.id])

# Teste 10: Validação de texto inválido ao adicionar uma alternativa.
def test_add_choice_with_invalid_text_raises_exception():
    """Verifica se tentar adicionar uma alternativa com texto vazio ou muito longo levanta uma exceção."""
    question = Question(title='Question for choice validation')
    
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')
        
    long_text = 'a' * 101
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice(long_text)
