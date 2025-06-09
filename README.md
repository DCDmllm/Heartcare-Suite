# Heartcare Suite: Multi-dimensional Understanding of ECG with Raw Multi-lead Signal Modeling

We present Heartcare Suite, a multimodal comprehensive framework for fine-grained electrocardiogram (ECG) understanding. It comprises three key components: **(i) Heartcare-220K**, a high-quality, structured, and comprehensive multimodal ECG dataset covering essential tasks such as disease diagnosis, waveform morphology analysis, and rhythm interpretation. **(ii) Heartcare-Bench**, a systematic and multi-dimensional benchmark designed to evaluate diagnostic intelligence and guide the optimization of Medical Multimodal Large Language Models (Med-MLLMs) in ECG scenarios. **(iii) HeartcareGPT** with a tailored tokenizer Bidirectional ECG Abstract Tokenization (Beat), which compresses raw multi-lead signals into semantically rich discrete tokens via dual-level vector quantization and query-guided bidirectional diffusion mechanism. Built upon Heartcare-220K, HeartcareGPT achieves strong generalization and SoTA performance across multiple clinically meaningful tasks. Extensive experiments demonstrate that Heartcare Suite is highly effective in advancing ECG-specific multimodal understanding and evaluation.

<img src="images/HeartcareGPT.jpg" style="vertical-align:middle;" />

## Dataset: Heartcare-220K

We construct **Heartcare-220K**, a comprehensive, fine-grained multimodal ECG instruction dataset that supports unified modeling across key tasks such as disease diagnosis, waveform morphology analysis, rhythm interpretation, report generation. It combines two sources: the public [PTB-XL dataset](https://physionet.org/content/ptb-xl/1.0.3/) with 21,799 12-lead ECG signals annotated with 179 SCP-ECG classes, and 12,170 ECG images with structured reports from top hospitals, including scanned traces, clinical conclusions, and de-identified metadata—substantially enriching modality and label diversity.

<img src="images/donut_charts.jpg" style="vertical-align:middle;" />

To transform heterogeneous ECG data into structured supervision, we develop **HeartAgent**, a modular multi-agent engine with a bottom-up pipeline that ensures annotation consistency and generates high-quality instruction-style QA pairs, significantly boosting both scalability and data quality.

<img src="images/engine.jpg" style="vertical-align:middle;" />

## Benchmark: Heartcare-Bench

We introduce **Heartcare-Bench**, a framework for systematically evaluating diagnostic intelligence in ECG scenarios. It covers tasks including closed-ended and open-ended QA, report generation, signal reconstruction, and trend prediction, grouped into three clinically grounded categories: Diagnostic, Form, and Rhythm.

## Model: HeartcareGPT

We propose **Bidirectional ECG Abstract Tokenization (Beat)**, a hierarchical, structure-aware discrete encoding framework tailored for ECG time-series data. Beat compresses raw ECG signals into token sequences based on vector quantization that can be directly consumed by MLLMs. These discrete representations are directly embedded into the vocabulary of MLLMs, enabling our proposed Med-MLLMs, **HeartcareGPT**, to perform end-to-end reasoning across signals, text, and images.

<img src="images/method.jpg" style="vertical-align:middle;" />
