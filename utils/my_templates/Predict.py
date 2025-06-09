import random
from utils.my_templates import Sentences

PREDICTION_VERBS = [
    "predict", "forecast", "estimate", "project", "anticipate", 
    "extrapolate", "model", "simulate", "calculate", "determine"
]

TIME_WINDOWS = [
    "a short period", "a little while", 
    "a few moments", "a brief interval",
    "a small timeframe", "a little bit",
    "a short duration", "a little span",
    "a short stretch", "a little interval",
    "the near future", "the short term",
    "the next little bit", "the next short while",
]

PRON = [
    "for", "in", "during", "over"
]

TIME_ADJ = [
    "next", "follwing", "coming", "immediate"
]

ECG_COMPONENTS = [
    "ECG waveform", "cardiac rhythm", "heart rate", 
    "QRS complex", "ST segment", "T wave", 
    "P wave", "QT interval", "PR interval",
    "electrical activity", "heart signals"
]

PREDICTION_TYPES = [
    "continuous prediction", "time-series forecast", 
    "sequential estimation", "temporal projection",
    "dynamic modeling", "real-time simulation"
]

def get_input(age, sex, ecg_input):
    return Sentences.get_input(age, sex, ecg_input)

def get_template(age, sex, ecg_input):
    v = random.choice(PREDICTION_VERBS)
    c = random.choice(ECG_COMPONENTS)
    p = random.choice(PREDICTION_TYPES)
    pron = random.choice(PRON)
    form = random.randint(0, 1)
    if form:
        adj = random.choice(TIME_ADJ)
        sec = random.randint(1, 10) * 0.1
        t = f"{random.choice(TIME_WINDOWS)} {sec:.2f} second"
        time = f"the {adj} {t}"
    else:
        sec = 1
        time = random.choice(TIME_WINDOWS)
    time = f"{pron} {time}"
    
    instructions = [
        f"Please {v} the {c} {time}.",
        f"{Sentences.my_capitalize(v)} how the {c} will evolve {time}.",
        f"Generate a {p} of the {c} {time}.",
        f"What would be your {v}ion of the {c} {time}?",
        f"Perform {v}ive modeling of the {c} {time}.",
        f"Create a forecast of the {c} dynamics {time}.",
        f"Based on current patterns, {v} the {c} {time}.",
        f"Project the expected changes {c} {time}.",
        f"Estimate the most probable {c} trajectory {time}.",
        f"Simulate the anticipated {c} behavior {time}.",
        f"Provide a {v}ive analysis of the {c} evolution {time}.",
        f"Calculate the likely progression of the {c} {time}.",
        f"Determine the projected {c} characteristics {time}.",
        f"Model the expected {c} variations {time}.",
        f"Anticipate how the {c} might change {time}.",
        f"Extrapolate the {c} pattern {time} timeframe.",
        f"Predict the cardiac electrical activity {time}.",
        f"Forecast the heart's electrical signals {time}.",
        f"Generate a real-time projection of {c} {time}.",
        f"Compute the probable {c} development {time}."
    ]

    predict = [
        f"ECG signal prediction results {time}:",
        f"Based on the input pattern, {time}, the predicted ECG continuation is:",
        f"The algorithm predicts this continuation {time}:",
        f"Based on the rhythm, here's the forecast {time}:",
        f"Sure! This is how the signal should progress {time}:",
        f"Predicted ECG segment {time}:",
        f"I think the ECG will continue like this {time}:",
    ]

    reply = f"{random.choice(predict)}\n<|pred_start|> {sec:.2f} <|pred_end|>"
    return [[get_input(age, sex, ecg_input), random.choice(instructions), reply]]