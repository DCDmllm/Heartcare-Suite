import random

NOUNS = [
    "analysis", "evaluation", "assessment", "interpretation", "classification", 
    "finding", "result", "observation", "diagnosis", "characteristic", 
    "signal", "pattern", "data", "recording", "trace", 
    "reading", "output", "measurement", "feature", "response", 
    "sequence", "fluctuation", 
]

# INPUT_VERBS = [
#     "is", "appears as", "resembles", "has the appearance of", "is structured similarly to", 
#     "presents as", "manifests as", "exhibits as", "demonstrates as", "demonstrates a waveform consistent with", 
#     "shows as", "features", "corresponds to", "consists of", "can be described as", "can be observed as", 
#     "is like", "takes the form of", "presents a pattern similar to", "exhibits characteristics of", 
#     "contains", "looks like", "displays as", "share similar characteristics with", "exhibits a similar pattern to", 
#     "is visually similar to", "is structurally similar to", "is waveform-wise similar to", 
# ]

INSTRUCTION_VERBS_ON_ECG = [
    "analyze", "identify", "examine", "review", "assess", 
    "investigate", "inspect", "look into", "probe into", "reason through", 
    "work through", "draw conclusions from", "make sense of", "delve into", 
    "go over", "summarize", 
]

INSTRUCTION_VERBS_ON_CLASSIFICATION = [
    "come to a conclusion about", "come up with", "tell", "determine", "provide", 
    "identify", "classify", "give", "assign", "provide", 
    "output", "deduce", 
]

REPLY_VERBS = [
    "indicates", "suggests", "confirms", "supports", "highlights", 
    "implies", "points to", "aligns with", "is consistent with", "reveals", 
    "aligns with", 
]

DIAGNOSTIC_NOUNS = [
    "diagnosis", "diagnostic type", "diagnostic class", "diagnostic category", "diagnostic classification",
]

FORM_NOUNS = [
    "form", "morphology", "shape and structure", 
]

RHYTHM_NOUNS = [
    "rhythm", "rate and regularity", "pattern and timing", 
]

PATIENTS = [
    "patient", "individual", "subject", "case", "person", 
]

ADJECTIVES = [
    "clear ", "apparent ", "evident ", "significant ", "notable ", 
    "distinct ", "characteristic ", "typical ", "specific ", "indicative ", "", 
]

ADVERBS_80 = [
    "highly likely ", "strongly suggestive of ", "very probable ", "indicative of "
]

ADVERBS_50 = [
    "possibly ", "suggestive of ", "uncertain but indicative ", "likely "
]

def my_capitalize(str):
    res = str[0].upper() + str[1:]
    return res

def get_noun_phrases():
    n_1_ = random.choice(NOUNS)
    n_2_ = random.choice(NOUNS)
    n_3_ = random.choice(PATIENTS)
    n_4_ = random.choice(PATIENTS)
    n_1_mixed_with_patient = [
        f"ECG {n_1_}",
        f"the ECG {n_1_}", 
        f"this ECG {n_1_}", 
        f"the given ECG {n_1_}", 
        f"the provided ECG {n_1_}", 
        f"the ECG {n_1_} given", 
        f"the ECG {n_1_} presented", 
        f"the {n_3_}'s ECG {n_1_}", 
        f"this {n_3_}'s ECG {n_1_}", 
        f"the ECG {n_1_} of the {n_3_}", 
        f"the provided ECG {n_1_} of this {n_3_}", 
        f"the given ECG {n_1_} from the {n_3_}", 
        f"this ECG {n_1_} from the {n_3_}",
        f"the ECG {n_1_} obtained from the {n_3_}",
    ]
    n_1 = random.choice(n_1_mixed_with_patient)
    n_2_mixed_with_patient = [
        f"ECG {n_2_}",
        f"the ECG {n_2_}", 
        f"this ECG {n_2_}", 
        f"the given ECG {n_2_}", 
        f"the provided ECG {n_2_}", 
        f"the ECG {n_2_} given", 
        f"the ECG {n_2_} presented", 
        f"the {n_4_}'s ECG {n_2_}", 
        f"this {n_4_}'s ECG {n_2_}", 
        f"the ECG {n_2_} of the {n_4_}", 
        f"the provided ECG {n_2_} of this {n_4_}", 
        f"the given ECG {n_2_} from the {n_4_}", 
        f"this ECG {n_2_} from the {n_4_}",
        f"the ECG {n_2_} obtained from the {n_4_}",
    ]
    n_2 = random.choice(n_2_mixed_with_patient)
    n_1_mixed_with_patient_simple = [
        f"ECG {n_1_}",
        f"the ECG {n_1_}", 
        f"this ECG {n_1_}", 
        f"the {n_3_}'s ECG {n_1_}", 
        f"the ECG {n_1_} of the {n_3_}", 
        f"this ECG {n_1_} from the {n_3_}",
        f"the ECG {n_1_} obtained from the {n_3_}",
    ]
    n_1_simple = random.choice(n_1_mixed_with_patient_simple)
    return n_1, n_1_simple, n_2

def get_input(age, sex, ecg_input):
    inputs = [
        f"This is a {age}-year-old {sex} patient.",
        f"The patient is {age} years old and {sex}.",
        f"Now we have a {sex} patient aged {age}.",
        f"Here is a {sex} patient, {age} years old.",
        f"Patient details: {age} years old, {sex}.",
        f"The ECG belongs to a {age}-year-old {sex} patient.",
        f"This ECG is from a {sex} patient who is {age} years old.",
        f"The ECG is from a {age}-year-old {sex} patient.",
        f"The ECG is for a {sex} patient aged {age}.",
        f"This ECG was recorded from a {age}-year-old {sex}.",
        f"The ECG report belongs to a {age}-year-old {sex} patient.",
        f"The ECG examination results is seen in a {age}-year-old {sex} during routine medical check-ups.",
        f"The acquired ECG corresponds to a {sex} patient who is {age} years old and undergoing clinical evaluation.",
        f"The detected ECG is observed in a {sex} patient undergoing evaluation at {age} years of age.",
        f"ECG testing is observed in a {sex} patient who is {age} years old.",
        f"The ECG originates from a {sex} patient aged {age}.",
        f"The ECG corresponds to a {age}-year-old {sex} who underwent heart monitoring.",
    ]

    return f"ECG (2 seconds, 250 Hz): {ecg_input}. {random.choice(inputs)}"

def get_diagnostic(age, sex, ecg_input, symptom_dict_list=None):
    v_1 = random.choice(INSTRUCTION_VERBS_ON_CLASSIFICATION)
    v_2 = random.choice(INSTRUCTION_VERBS_ON_ECG)
    v_3 = random.choice(REPLY_VERBS)
    adj = random.choice(ADJECTIVES)
    diagnostic = random.choice(DIAGNOSTIC_NOUNS)
    n_1, n_1_simple, n_2 = get_noun_phrases()

    instructions = [
        f"What is the {diagnostic} of {n_1}",
        f"What {diagnostic} can be concluded based on the observation in {n_1}?",
        f"What {diagnostic} can be inferred from {n_1}?",
        f"Which specific {diagnostic} is most indicative of the observed characteristics in {n_1}?",
        f"Given {n_1_simple}, what {diagnostic} would be most suitable?",
        f"Based on the data from {n_1}, what {diagnostic} can be identified?",
        f"Which defining {diagnostic} can be attributed to {n_1}?",
        f"After carefully examining {n_1}, proceed to {v_1} the {diagnostic} that aligns most accurately with its features.",
        f"Based on {n_1}, {v_1} what {diagnostic} it belongs to.",
        f"By examining {n_1}, can you please {v_1} the correct {diagnostic}?",
        f"Considering {n_1}, can you {v_1} the {diagnostic}?",
        f"From the features of {n_1}, please {v_1} the corresponding {diagnostic}.",
        f"Given {n_1_simple}, please {v_1} the {diagnostic} beneath its features.",
        f"Through meticulous examination of {n_1}, please accurately {v_1} the {diagnostic} that best defines it.",
        f"Using {n_1} as a reference, please{v_1} the {diagnostic} accordingly.",
        f"Please {v_1} the {diagnostic} based on {n_1}.",
        f"{my_capitalize(v_1)} the {diagnostic} that aligns with the clinical presentation of {n_1}.",
        f"Please {v_1} the most relevant {diagnostic} for {n_1} according to waveform analysis.",
        f"How would you {v_1} the {diagnostic} based on {n_1}?",
        f"With careful observation, please {v_1} the {diagnostic} that best suits {n_1}.",
        f"{my_capitalize(v_2)} {n_1} and {v_1} its appropriate {diagnostic}.",
        f"Please {v_2} {n_1} in a systematic manner, ensuring that all pertinent aspects are considered before determining its {diagnostic}.",
        f"By applying medical expertise, {v_2} {n_1} and {v_1} which {diagnostic} it best fits into.",
        f"Please carefully {v_2} {n_1} by considering its waveform patterns and irregularities, then {v_1} the most appropriate {diagnostic}.",
        f"Based on {n_1}, {v_2} its structure and {v_1} the expected {diagnostic}.",
        f"From the {n_1}, {v_2} its key patterns and {v_1} the best matching {diagnostic}."
        f"Given {n_1_simple}, please accurately {v_2} its waveform structure and {v_1} the {diagnostic} that corresponds to it.",
        f"Using {n_1}, {v_2} its waveform and {v_1} the corresponding {diagnostic}.",
        f"{my_capitalize(v_2)} {n_1} and diagnose its classification based on its features.",
        f"{my_capitalize(v_2)} {n_1} thoroughly, taking into account all relevant diagnostic criteria, and {v_1} which class it falls under.",
        f"Examine {n_1} in depth, {v_2} its fundamental properties, and {v_1} it accordingly based on recognized diagnostic standards.",
        f"After reviewing {n_1}, {v_2} its relevant characteristics and {v_1} it according to established diagnostic criteria.",
        f"By assessing {n_1} in relation to standard diagnostic frameworks, {v_2} its defining characteristics and {v_1} it accordingly.",
        f"Given {n_1_simple}, thoroughly {v_2} its structural components, including rhythm, morphology, and amplitude, to {v_1} its {diagnostic}.",
    ]
    
    if symptom_dict_list is None:
        return random.choice(instructions)
    
    if not symptom_dict_list[0]:
        replies = [
            f"After comprehensive evaluation, the {diagnostic} {v_3} no evidence of pathological abnormalities in {n_2}.",
            f"The {diagnostic} reveals a physiologically normal ECG, with all waveforms within expected parameters in {n_2}.",
            f"No clinically significant abnormalities are detected; {n_2} {v_3} standard healthy cardiac activity.",
            f"The ECG tracing in {n_2} is unremarkable, showing no signs of arrhythmia, ischemia, or conduction disturbances.",
            f"The {diagnostic} confirms a normal ECG pattern in {n_2}, consistent with a healthy cardiovascular system.",
            f"No pathological findings are observed; {n_2} exhibits typical features of normal cardiac function.",
            f"All leads in {n_2} demonstrate physiological waveforms, and the overall conclusion is a normal ECG.",
            f"The recorded {n_2} is within normal bounds, showing no deviations suggestive of disease.",
            f"Upon detailed assessment, {n_2} {v_3} a completely normal cardiac electrical activity.",
            f"Standard diagnostic criteria confirm that {n_2} is entirely normal, with no pathological findings.",
            f"Comprehensive review of {n_2} reveals a normal ECG, with no abnormalities in any lead.",
            f"The {diagnostic} of {n_2} is reassuringly normal, with no evidence of cardiac disease.",
            f"After systematic analysis, {n_2} is classified as a normal ECG without any concerning features.",
            f"The ECG recording from {n_2} meets all criteria for normal cardiac electrical activity.",
            f"No diagnostic red flags are present in {n_2}; the ECG is entirely normal.",
            f"The {diagnostic} of {n_2} aligns perfectly with expected physiological norms.",
            f"Normal ECG.",
            f"No abnormalities.",
            f"Healthy cardiac activity.",
            f"ECG is within normal limits, no signs of pathology.",
            f"All parameters are within expected ranges.",
            f"The ECG meets all criteria for a normal study.",
            f"Findings are consistent with a healthy cardiovascular system.",
            f"No clinically significant abnormalities detected.",
            f"Normal ECG, no acute changes.",
        ]
        return [get_input(age, sex, ecg_input), random.choice(instructions), random.choice(replies)]

    res_list = []
    for key, value in symptom_dict_list[0].items():
        if value == 100:
            res_list.append(key)
        elif value >= 80:
            res_list.append(f"{random.choice(ADVERBS_80)}{key}")
        else:
            res_list.append(f"{random.choice(ADVERBS_50)}{key}")
            
    symptom = ", ".join(res_list)

    replies = [
        f"After analysis, the {diagnostic} {v_3} {adj}symptoms consistent with {symptom} from {n_2}.",
        f"After evaluating {n_2}, the {diagnostic} {v_3} a {adj}{symptom}.",
        f"After examining {n_2}, it belongs to the {adj}category of {symptom}.",
        f"After thorough analysis, {n_2} {v_3} {adj}results indicating {symptom} as the {diagnostic}.",
        f"As per the diagnostic criteria, {n_2} strongly {v_3} {symptom} as the probable {diagnostic}.",
        f"Based on the interpretation of {n_2}, the {diagnostic} falls under the category of {symptom}.",
        f"Based on {n_2}, the {diagnostic} {v_3} a {adj}suggestion of {symptom}.",
        f"By evaluating {n_2}, it becomes {adj}that the {diagnostic} is suggestive of {symptom}.",
        f"Considering the observed traits in {n_2}, the {diagnostic} corresponds to {symptom}."
        f"Findings from {n_2} are indicative of {adj}symptoms consistent with {symptom}.",
        f"Following {n_2} assessment, the {diagnostic} {v_3} an {adj}finding of {symptom}.",
        f"From {n_2}, it can be concluded that the {diagnostic} is {adj}for {symptom}."
        f"From {n_2}, it is clear that the {diagnostic} {v_3} an {adj}manifestation of {symptom}.",
        f"Observations from {n_2} demonstrate a {adj}manifestation of {symptom}.",
        f"The {diagnostic} for {n_2} is {symptom}.",
        f"The {diagnostic} observed in {n_2} suggests a {adj}link to {symptom}.",
        f"The {diagnostic} {v_3} {symptom}.",
        f"Upon detailed assessment, the ECG {diagnostic} is classified as indicative of {symptom}.",
        f"Upon reviewing {n_2}, the {diagnostic} is classified as {symptom}.",
        f"The ECG {diagnostic} can be classified as a case of {symptom}.",
        f"{my_capitalize(n_2)} suggests a {adj}{diagnostic} of {symptom}.",
        f"{my_capitalize(n_2)} {v_3} a {adj}{diagnostic}, with prominent signs of {symptom}.",
        f"{my_capitalize(n_2)} {v_3} an {adj}{diagnostic}, pointing to {symptom}.",
        f"Key characteristics found in {n_2} strongly support a diagnosis of {symptom}.",
        f"Upon review, it is diagnosed that {n_2} corresponds to {symptom}.",
        f"From the findings in {n_2}, the diagnostic category is {symptom}.",
        f"Extensive review of {n_2} {v_3} {symptom} as a prominent diagnostic possibility.",
        f"{my_capitalize(symptom)}.",
    ]

    return [get_input(age, sex, ecg_input), random.choice(instructions), random.choice(replies)]

def get_form(age, sex, ecg_input, symptom_dict_list=None):
    v_1 = random.choice(INSTRUCTION_VERBS_ON_CLASSIFICATION)
    v_2 = random.choice(INSTRUCTION_VERBS_ON_ECG)
    v_3 = random.choice(REPLY_VERBS)
    adj = random.choice(ADJECTIVES)
    form = random.choice(FORM_NOUNS)
    n_1, n_1_simple, n_2 = get_noun_phrases()

    instructions = [
        f"What {form} does {n_1} fall into?",
        f"What is the most appropriate {form} that can be derived from {n_1}?",
        f"What kind of {form} does {n_1} suggest?",
        f"Which {form} classification best describes the characteristics of {n_1}?",
        f"From a detailed analysis of {n_1}, what {form} emerges as the most fitting?",
        f"In the context of {n_1}, which {form} stands out as the most accurate?",
        f"Upon analyzing the amplitudes, durations or deflections within {n_1}, what {form} can be confidently assigned?",
        f"After reviewing {n_1}, please {v_1} its {form}.",
        f"Based on {n_1}, please{v_1} the {form}.",
        f"Based on your analysis of {n_1}, please {v_1} the most suitable {form}.",
        f"By carefully assessing the provided {n_1}, please {v_1} the most probable {form}.",
        f"Following a thorough analysis of {n_1}, please {v_1} the most fitting {form} that characterizes its attributes.",
        f"From {n_1}, {v_1} what {form} it most accurately corresponds to.",
        f"Given the specific characteristics observed in {n_1_simple}, {v_1} the most suitable {form} it represents.",
        f"Upon careful inspection of {n_1}, please {v_1} its {form}.",
        f"With careful review of {n_1}, please {v_1} the corresponding {form}.",
        f"Please {v_1} the {form} of {n_1}.",
        f"{my_capitalize(v_1)} the {form} according to {n_1}.",
        f"{my_capitalize(v_1)} the optimal {form} for {n_1}.",
        f"Please {v_1} the most suitable {form} classification with a detailed examination of {n_1}.",
        f"Using a systematic approach, {v_1} the appropriate {form} associated with {n_1}.",
        f"By analyzing key markers, {v_1} the most fitting {form} for {n_1}.",
        f"Please {v_2} {n_1} and {v_1} its {form}.",
        f"Please {v_2} {n_1}, {v_1} the {form} it belongs to.",
        f"{my_capitalize(v_2)} {n_1} and {v_1} which {form} best matches its characteristics.",
        f"By carefully considering all available information, {v_2} {n_1} and {v_1} the most suitable {form}.",
        f"Taking into account any potential anomalies, {v_2} {n_1} and {v_1} which {form} it should be assigned to.",
        f"Please examine {n_1}, {v_2} its signals and {v_1} the best {form}.",
        f"Based on the ECG {n_1}, {v_2} its characteristics carefully and {v_1} the most appropriate {form} it belongs to.",
        f"Given {n_1_simple}, please {v_2} its features and {v_1} the right {form}.",
        f"In light of {n_1}, {v_2} present data and {v_1} the most suitable {form}.",
        f"With {n_1}, {v_2} its abnormalities and {v_1} the appropriate {form}.",
    ]
    
    if symptom_dict_list is None:
        return random.choice(instructions)
    
    if not symptom_dict_list[1]:
        replies = [
            f"The {form} of {n_2} is entirely norma.",
            f"All waveforms in {n_2} exhibit standard {form}.",
            f"{my_capitalize(n_2)} demonstrates {adj}physiological waveform shapes.",
            f"No morphological abnormalities are observed; {n_2} aligns with standard ECG criteria for healthy individuals.",
            f"The ECG in {n_2} exhibits normal {form}.",
            f"Each lead in {n_2} shows expected waveform characteristics, and no axis deviation is present.",
            f"Detailed morphological assessment of {n_2} confirms normal P wave axis, QRS duration, and T wave polarity.",
            f"The {form} in {n_2} is consistent with healthy cardiac conduction.",
            f"ECG analysis confirms that {n_2} has no abnormal waveforms or conduction abnormalities.",
            f"The overall morphology of {n_2} is consistent with a healthy, non-pathological ECG.",
            f"Normal waveform morphology.",
            f"Standard P-QRS-T configuration.",
            f"No morphological abnormalities.",
            f"Healthy ECG waveform shapes.",
            f"P waves, QRS complexes, and T waves are within normal limits.",
            f"No evidence of ST-segment elevation, depression, or T-wave inversions.",
            f"All leads demonstrate normal wave progression and axis.",
            f"Waveform amplitudes and durations are physiological.",
            f"ECG meets all criteria for normal morphology in all 12 leads.",
            f"Interpretation: Normal ECG morphology, no ischemic changes.",
        ]

        return [get_input(age, sex, ecg_input), random.choice(instructions), random.choice(replies)]

    res_list = []
    for key, value in symptom_dict_list[1].items():
        if value == 100:
            res_list.append(key)
        elif value >= 80:
            res_list.append(f"{random.choice(ADVERBS_80)}{key}")
        else:
            res_list.append(f"{random.choice(ADVERBS_50)}{key}")
            
    symptom = ", ".join(res_list)

    replies = [
        f"After careful analysis, {n_2} shows signs of {symptom}.",
        f"After evaluating {n_2}, the {form} {v_3} {symptom}.",
        f"After reviewing {n_2}, the {form} {v_3} an {adj}indication of {symptom}.",
        f"An in-depth analysis of {n_2} {v_3} a {adj}correlation with {symptom}.",
        f"Based on the collected data, {n_2} {v_3} {adj}characteristics of {symptom}.",
        f"Based on {n_2}, after thorough examination, the {form} is classified as {symptom}.",
        f"Based on {n_2}, the {form} {v_3} {adj}evidence supporting {symptom}.",
        f"Clinical findings from {n_2} reinforce the presence of {symptom} as a {adj}outcome.",
        f"Data gathered from {n_2} points toward {symptom} as the most probable {form}.",
        f"Following the analysis of {n_2}, the {form} {v_3} {adj}indicators of {symptom}.",
        f"From the analysis of {n_2}, the most appropriate {form} is {symptom}.",
        f"From {n_2}, it can be concluded that the {form} is {symptom}.",
        f"From {n_2}, it is evident that the {form} {v_3} {adj}symptoms of {symptom}.",
        f"Results from {n_2} testing show {symptom} as the most likely {form}.",
        f"The {form} in {n_2} {v_3} {adj}features of {symptom}.",
        f"The {form} of {n_2} is {symptom}.",
        f"Upon analyzing {n_2}, the {form} {v_3} {adj}evidence of {symptom} being present.",
        f"Upon evaluating {n_2}, the {form} {v_3} {adj}clues indicating {symptom}.",
        f"Upon reviewing {n_2}, the {form} {v_3} {adj}characteristics related to {symptom}.",
        f"The ECG {form} falls under the category of {symptom}.",
        f"{my_capitalize(n_2)} {v_3} a {adj}pattern, suggesting {symptom} as the primary {form}.",
        f"{my_capitalize(n_2)} {v_3} a {form} result, with {adj}symptoms of {symptom}.",
        f"{my_capitalize(n_2)} {v_3} {adj}evidence of {symptom} with a {form}.",
        f"{my_capitalize(symptom)}.",
    ]

    return [get_input(age, sex, ecg_input), random.choice(instructions), random.choice(replies)]

def get_rhythm(age, sex, ecg_input, symptom_dict_list=None):
    v_1 = random.choice(INSTRUCTION_VERBS_ON_CLASSIFICATION)
    v_2 = random.choice(INSTRUCTION_VERBS_ON_ECG)
    v_3 = random.choice(REPLY_VERBS)
    adj = random.choice(ADJECTIVES)
    rhythm = random.choice(RHYTHM_NOUNS)
    n_1, n_1_simple, n_2 = get_noun_phrases()

    instructions = [
        f"What {rhythm} does {n_1} exhibit?",
        f"What {rhythm} is most relevant to the features exhibited by {n_1}?",
        f"What category of {rhythm} does {n_1} belong to?",
        f"Which {rhythm} aligns best with the properties of {n_1}?",
        f"How does {n_1} relate to {rhythm}?",
        f"Considering {n_1}, what {rhythm} would be the best match?",
        f"Considering the amplitudes, durations and deflections observed in {n_1}, what {rhythm} should it be categorized under?",
        f"After thoroughly inspecting {n_1}, {v_1} its {rhythm}.",
        f"Based on {n_1} presented, please {v_1} the relevant {rhythm}.",
        f"Based on the distinct attributes of {n_1}, please {v_1} its appropriate {rhythm}.",
        f"By conducting a detailed evaluation of {n_1}, {v_1} the correct {rhythm} it should be classified under.",
        f"From {n_1}, please {v_1} the appropriate {rhythm}.",
        f"Given {n_1_simple}, {v_1} the corresponding {rhythm}.",
        f"Taking into account {n_1}, {v_1} the precise {rhythm} that best corresponds to it.",
        f"Upon your examination of {n_1}, {v_1} the appropriate {rhythm}.",
        f"With reference to {n_1}, {v_1} the correct {rhythm} it aligns with.",
        f"{my_capitalize(v_1)} the {rhythm} associated with {n_1}.",
        f"Please {v_1} the {rhythm} reflecting the key abnormalities in {n_1}.",
        f"{my_capitalize(v_1)} the most relevant {rhythm} from {n_1} based on its distinctive features.",
        f"What would you {v_1} the {rhythm} of {n_1} to be?",
        f"Through precise analysis, please {v_1} the {rhythm} appropriately represents {n_1}.",
        f"Taking into account all features, {v_1} the {rhythm} that represents {n_1} accurately.",
        f"{my_capitalize(v_2)} {n_1} and {v_1} the most accurate {rhythm}.",
        f"Please {v_2} {n_1} by examining its key features in detail, and {v_1} a precise {rhythm} based on the observed patterns.",
        f"Please {v_2} the features of {n_1}, {v_1} the {rhythm} it belongs to.",
        f"Systematically {v_2} {n_1}, taking into account any abnormalities or deviations from normal patterns, and {v_1} the correct {rhythm}.",
        f"With precision and attention to detail, {v_2} {n_1} and {v_1} the most appropriate {rhythm} based on its characteristics.",
        f"After thoroughly examining the {n_1}, please {v_2} its relevant features and {v_1} the corresponding {rhythm} with justification.",
        f"By closely analyzing the {n_1}, please {v_2} any anomalies present and {v_1} the most likely {rhythm} it corresponds to.",
        f"Given the information contained within {n_1_simple}, please carefully {v_2} its waveform and irregularities to {v_1} the appropriate {rhythm}.",
        f"Probing into {n_1}, {v_2} its details and {v_1} the correct {rhythm}.",
        f"With reference to {n_1}, please meticulously {v_2} its various parameters and {v_1} the most relevant {rhythm}.",
    ]
    
    if symptom_dict_list is None:
        return random.choice(instructions)
    
    if not symptom_dict_list[2]:
        replies = [
            f"The ECG in {n_2} shows a regular {rhythm} with consistent P-P and R-R intervals.",
            f"Normal {rhythm} is confirmed in {n_2}.",
            f"No arrhythmias are detected; {n_2} demonstrates a steady, sinus-originating {rhythm}.",
            f"The heart rate in {n_2} is within normal range, and the {rhythm} is regular without variability.",
            f"All beats in {n_2} are conducted normally.",
            f"The ECG tracing of {n_2} reveals a perfectly regular {rhythm}.",
            f"No conduction abnormalities are present.",
            f"The recorded {n_2} meets all criteria for normal {rhythm}.",
            f"The {rhythm} in {n_2} is entirely regular.",
            f"The heart rate variability in {n_2} is within normal physiological limits, suggesting healthy autonomic tone.",
            f"The {n_2} indicates healthy conduction.",
            f"ECG analysis confirms that {n_2} has no arrhythmias or conduction system disorders.",
            f"The overall rhythm assessment of {n_2} is entirely normal, with no concerning features.",
            f"Normal rhythm.",
            f"Regular rhythm.",
            f"No arrhythmias.",
            f"Physiological rhythm.",
            f"Heart rate is regular, with consistent P-P and R-R intervals.",
            f"Interpretation: Normal rhythm, no conduction abnormalities.",
            f"Conclusion: Normal cardiac rhythm, no actionable findings.",
        ]
        return [get_input(age, sex, ecg_input), random.choice(instructions), random.choice(replies)]

    res_list = []
    for key, value in symptom_dict_list[2].items():
        if value == 100:
            res_list.append(key)
        elif value >= 80:
            res_list.append(f"{random.choice(ADVERBS_80)}{key}")
        else:
            res_list.append(f"{random.choice(ADVERBS_50)}{key}")

    symptom = ", ".join(res_list)

    replies = [
        f"After closely inspecting {n_2}, the {rhythm} {v_3} {adj}traits that align with {symptom}.",
        f"After examining {n_2}, it belongs to the category of {symptom}.",
        f"After studying {n_2}, the {rhythm} {v_3} {adj}symptoms of {symptom}.",
        f"Analysis of {n_2} uncovers {adj}patterns commonly associated with {symptom}.",
        f"Based on the findings in {n_2}, the {rhythm} {v_3} {symptom}.",
        f"Based on {n_2}, the {rhythm} is {adj}and {v_3} {symptom}.",
        f"Based on {n_2}, the {rhythm} {v_3} {adj}signs of {symptom}.",
        f"Comparing {n_2} to similar cases, it appears to be a {adj}match for {symptom}.",
        f"Examination of {n_2} {v_3} a {adj}consistency with the symptoms of {symptom}.",
        f"Following the interpretation of {n_2}, the {rhythm} {v_3} {adj}symptoms that suggest {symptom}.",
        f"From the examination of {n_2}, the {rhythm} {v_3} {adj}indications of {symptom}.",
        f"From {n_2}, it can be inferred that the {rhythm} {v_3} {adj}signs of {symptom}.",
        f"Further analysis of {n_2} {v_3} a {adj}correlation with {symptom}.",
        f"Results of tests on {n_2} {v_3} a {adj}likelihood of {symptom}.",
        f"The {rhythm} is {adj}for {symptom}.",
        f"The {rhythm} of {n_2} {v_3} {symptom}.",
        f"Upon close inspection of the {n_2}, it is determined that the {rhythm} is {symptom}.",
        f"Upon examining the {n_2}, it is found that the {rhythm} {v_3} {adj}symptoms of {symptom}.",
        f"Upon reviewing {n_2}, the {rhythm} {v_3} {adj}hints at {symptom}.",
        f"{my_capitalize(n_2)} reveals a {adj}{rhythm}, which {v_3} signs of {symptom}.",
        f"{my_capitalize(n_2)} {v_3} a {adj}{rhythm}, which points to {symptom} as the likely condition.",
        f"{my_capitalize(n_2)} {v_3} an {adj}{rhythm} of {symptom}.",
        f"{my_capitalize(n_2)} {v_3} {adj}markers of {symptom}, consistent with the {rhythm} findings.",
        f"{my_capitalize(symptom)}.",
    ]

    return [get_input(age, sex, ecg_input), random.choice(instructions), random.choice(replies)]

def get_func(age, sex, ecg_input, symptom_dict_list, idx):
    func = [get_diagnostic, get_form, get_rhythm]
    return [func[idx](age, sex, ecg_input, symptom_dict_list)]

def get_template(age, sex, ecg_input, symptom_dict_list):
    result = []
    for idx in range(3):
        result = result + get_func(age, sex, ecg_input, symptom_dict_list, idx)
    return result