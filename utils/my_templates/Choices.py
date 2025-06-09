import random
import json
from utils.my_templates import Sentences

with open('data/class.json', 'r', encoding='utf-8') as f:
    OPTION = json.load(f)

def get_options(key, symptom_dic, idx, num_choices=4):
    cols = ['diagnostic', 'form', 'rhythm']
    option_list = OPTION[cols[idx]] + ["normal"]
    option_list = list(set(option_list) - set(symptom_dic.keys()))
    options = random.sample(option_list, k=num_choices-1)
    options.append(key)
    random.shuffle(options)
    idx = options.index(key)
    reply = f"{chr(ord('A') + idx)}. {Sentences.my_capitalize(key)}."

    question = []
    for i, op in enumerate(options):
        question.append(f"{chr(ord('A') + i)}. {Sentences.my_capitalize(op)}")
    question = "; ".join(question)
    return question, reply

def get_input(age, sex, ecg_input):
    return Sentences.get_input(age, sex, ecg_input)

def get_func(age, sex, ecg_input, symptom_dict_list, idx):
    result = []
    func = [Sentences.get_diagnostic, Sentences.get_form, Sentences.get_rhythm]
    symptom_dic = symptom_dict_list[idx]
    if not symptom_dic:
        symptom_dic = {'normal': 100}
    for key in symptom_dic.keys():
        question, reply = get_options(key, symptom_dic, idx)
        instruction = func[idx](age, sex, ecg_input) + " " + question +"."
        result.append([get_input(age, sex, ecg_input), instruction, reply])

    return result

def get_template(age, sex, ecg_input, symptom_dict_list):
    result = []
    for idx in range(3):
        result = result + get_func(age, sex, ecg_input, symptom_dict_list, idx)

    return result