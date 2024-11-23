from .question_assistant import Question

def get_index_from_id(question_list:list[Question], id:int):
    return (tuple(index 
                  for index, question in enumerate(question_list)
                  if question['id'] == id))[0]