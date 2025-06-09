import random
from utils.my_templates import Sentences

NOUNS = [
    "analysis", "evaluation", "assessment", "interpretation", "classification", 
    "finding", "result", "observation", "diagnosis", "characteristic", 
    "signal", "pattern", "data", "recording", "trace", "reading", "output", 
    "measurement", "feature", "response", "sequence", "fluctuation"
]

ADJECTIVES = [
    "detailed ", "preliminary ", "comprehensive ", "initial ", "final ", 
    "thorough ", "brief ", "critical ", "systematic ", "technical ", 
    "statistical ", "quantitative", "qualitative ", "professional ", "clear ", 
    "concise ", "", 
]

VERBS_ON_REPORT = [
    "provide", "give me", "write", "compile", "generate", 
    "construct", "deliver", "formulate", "summarize", "derive", 
]

VERBS_ON_ECG = [
    "analyze", "evaluate", "assess", "summarize", "review", 
]

PATIENTS = [
    "patient", "individual", "subject", "case", "person", 
]

RECORDS = [
    "diagnostic report", "clinical report", "diagnostic summary", "medical documentation", "medical record", 
]

ADVERBS_80 = [
    "highly likely ", "strongly suggestive of ", "very probable ", "indicative of "
]

ADVERBS_50 = [
    "possibly ", "suggestive of ", "uncertain but indicative ", "likely "
]

def get_input(age, sex, ecg_input):
    return Sentences.get_input(age, sex, ecg_input)

def get_template(age, sex, ecg_input, symptom_dict_list):
    n_1 = random.choice(NOUNS)
    n_2 = random.choice(RECORDS)
    n_3 = random.choice(PATIENTS)
    adj = random.choice(ADJECTIVES)
    v_1 = random.choice(VERBS_ON_REPORT)
    v_2 = random.choice(VERBS_ON_ECG)

    instructions = [
        f"From the ECG {n_1}, {v_1} me a {adj}{n_2}.",
        f"{Sentences.my_capitalize(v_1)} a {adj}{n_2} of the ECG {n_1}.",
        f"Based on the ECG {n_1} of the {n_3}, {v_1} a {adj}{n_2}.",
        f"{Sentences.my_capitalize(v_2)} the ECG {n_1} of this {n_3} and {v_1} a {adj}{n_2}.",
        f"{Sentences.my_capitalize(v_2)} the findings associated with this ECG {n_1} into a {adj}{n_2}.",
        f"Given the {n_3}'s ECG {n_1}, {v_1} a {adj}{n_2} that encapsulates its findings.",
        f"With reference to the {n_3}'s ECG {n_1}, {v_1} a {adj}{n_2} that highlights the significant findings.",
        f"{Sentences.my_capitalize(v_1)} a {adj}{n_2} based on the comprehensive evaluation of the ECG {n_1}.",
        f"Taking the ECG {n_1} of the {n_3} into account, {v_1} a {adj}{n_2} on its clinical implications.",
        f"{Sentences.my_capitalize(v_1)} the primary observations from the ECG {n_1} into a {adj}{n_2} .",
        f"{Sentences.my_capitalize(v_1)} a {adj}{n_2} reflecting the key takeaways from the findings of the ECG {n_1}",
        f"{Sentences.my_capitalize(v_2)} the data from the ECG {n_1} and {v_1} a {adj}{n_2} that accurately represents your conclusions.",
        f"{v_1.capitalize} a {adj}{n_2} that conveys its diagnostic insights using the details extracted from the ECG {n_1}.",
        f"{Sentences.my_capitalize(v_2)} the ECG {n_1} of this {n_3} and {v_1} a {adj}{n_2} presenting its major implications.",
        f"From the ECG {n_1}, {v_1} a {adj}{n_2} to summarize its findings effectively.",
        f"{Sentences.my_capitalize(v_2)} the parameters of ECG {n_1} and {v_1} a {adj}{n_2} that encapsulates its clinical relevance.",
        f"Taking the {n_3}'s ECG {n_1} into account, {v_1} a {adj}{n_2} that distills its most critical insights.",
        f"Extract meaningful conclusions from the {n_3}'s ECG {n_1} and {v_1} a {adj}{n_2} summarizing them.",
        f"{Sentences.my_capitalize(v_2)} the {n_3}'s ECG {n_1} in detail and {v_1} a {adj}{n_2} that presents its core findings.",
    ]

    l = []
    for i in range(3):
        res_list = []
        if not symptom_dict_list[i]:
            if i == 0:
                result = "- Normal ECG."
            elif i == 1:
                result = "- No abnormal waveforms."
            else:
                result = "- Regular rhythm."
        else:
            for key, value in symptom_dict_list[i].items():
                if value == 100:
                    res_list.append(f"- {Sentences.my_capitalize(key)}.")
                elif value >= 80:
                    res_list.append(f"- {Sentences.my_capitalize(random.choice(ADVERBS_80))}{key}.")
                else:
                    res_list.append(f"- {Sentences.my_capitalize(random.choice(ADVERBS_50))}{key}.")
            result = "\n".join(res_list)
        l.append(result)

        replies = [
            f"Sure! Here is the {n_2}:",
            f"The {n_2} is as follows:",
            f"Please see the generated {n_2} below:",
            f"As requested, here is the detailed {n_2}:",
            f"The analysis results are summarized in the following {n_2}:",
            f"The complete {n_2} is provided below:",
            f"Full {n_2} generated as per your request:",
            f"Processing complete. The {n_2} is ready:",
            f"Sure! The detailed {n_2} is as follows:",
            f"Here's the {n_2} you requested:",
        ]

    reply = f'''{random.choice(replies)}
<|report_start|>
# Diagnostic Report
## Information
- Age: {age}
- Sex: {Sentences.my_capitalize(sex)}
## Form Description
{l[1]}
## Rhythm Description
{l[2]}
<|report_end|>
## Diagnostic Recommendation
{l[0]}
'''
    return [[get_input(age, sex, ecg_input), random.choice(instructions), reply]]