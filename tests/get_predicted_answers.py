import os
import sys
import json
import argparse

# IMPORTANT:
# Before running this script, make sure to follow the instructions in the README file.
# You need to execute load_data.py to load the necessary data and api.py to start the server.

# Add the backend directory to the system path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Verify the backend path and import the invoke function
try:
    from chat import invoke
except ImportError as e:
    print(f"Failed to import 'invoke' from 'chat.py' in {backend_path}. Make sure the path is correct.")
    raise e

def read_questions_answers(file_path):
    """
    Reads questions and answers from a file.
    
    Parameters:
    - file_path (str): The path to the input file.
    
    Returns:
    - list of tuple: A list of (question, answer) tuples.
    """
    questions_answers = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            question, answer = line.strip().split('\t')
            questions_answers.append((question, answer))
    
    return questions_answers

def get_model_answers(questions):
    """
    Gets answers from the RAG model for a list of questions.
    
    Parameters:
    - questions (list of str): The questions to ask the model.
    
    Returns:
    - list of str: The answers from the model.
    """
    answers = []
    
    for question in questions:
        response = invoke(question)
        answers.append(response.get('answer', ''))
    
    return answers

def save_answers(file_path, model_answers, true_answers):
    """
    Saves the model answers and true answers to a file.
    
    Parameters:
    - file_path (str): The path to the output file.
    - model_answers (list of str): The answers from the model.
    - true_answers (list of str): The true answers from the input file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for model_answer, true_answer in zip(model_answers, true_answers):
            file.write(f"{model_answer}\t{true_answer}\n")

def main():
    parser = argparse.ArgumentParser(description="Process some questions and answers.")
    parser.add_argument('--input', type=str, default='ja_nein2.txt',
                        help='the path to the input file (default: questions_and_answers.txt)')
    parser.add_argument('--output', type=str, default='answers.txt',
                        help='the path to the output file (default: answers.txt)')
    
    args = parser.parse_args()
    
    input_file = args.input
    output_file = args.output
    
    # Step 1: Read the input file
    questions_answers = read_questions_answers(input_file)
    questions = [qa[0] for qa in questions_answers]
    true_answers = [qa[1] for qa in questions_answers]
    
    # Step 2: Get answers from the model
    model_answers = get_model_answers(questions)
    
    # Step 3: Save the results to an output file
    save_answers(output_file, model_answers, true_answers)
    
    print(f"Answers have been saved to {output_file}")

if __name__ == "__main__":
    main()
