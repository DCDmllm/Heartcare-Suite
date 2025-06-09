<h1 align = "center">
<img src="images/logo.png" alt="icon" style="width:40px; vertical-align:middle;" />
Heartcare Suite: Multi-dimensional Understanding of ECG with Raw Multi-lead Signal Modeling
</h1>

<div align="center">
Yihan Xie<sup>1*</sup>, Sijing Li<sup>1*</sup>, Tianwei Lin<sup>1*</sup>, Zhuonan Wang<sup>1</sup>, Chenglin Yang<sup>1</sup>, Yu Zhong<sup>1</sup>, Wenqiao Zhang<sup>1</sup>, Haoyuan Li<sup>2</sup>, Hao Jiang<sup>2</sup>, Fengda Zhang<sup>1</sup>, Qishan Chen<sup>3</sup>, Jun Xiao<sup>1</sup>, Yueting Zhuang<sup>1</sup>, Beng Chin Ooi<sup>4</sup>
<br><br>

<sup>1</sup>Zhejiang University,
<sup>2</sup>Alibaba,
<sup>3</sup>Xinhua Hospital of Shanghai Jiaotong University School,
<sup>4</sup>National University of Singapore
</div>

<a href='https://arxiv.org/abs/2506.05831'><img src='https://img.shields.io/badge/Paper-Arxiv-red'></a>

<img src="images/HeartcareGPT.jpg" style="vertical-align:middle;" />

We present Heartcare Suite, a multimodal comprehensive framework for fine-grained electrocardiogram (ECG) understanding. It comprises three key components: **(i) Heartcare-220K**, a high-quality, structured, and comprehensive multimodal ECG dataset covering essential tasks such as disease diagnosis, waveform morphology analysis, and rhythm interpretation. **(ii) Heartcare-Bench**, a systematic and multi-dimensional benchmark designed to evaluate diagnostic intelligence and guide the optimization of Medical Multimodal Large Language Models (Med-MLLMs) in ECG scenarios. **(iii) HeartcareGPT** with a tailored tokenizer Bidirectional ECG Abstract Tokenization (**Beat**), which compresses raw multi-lead signals into semantically rich discrete tokens via dual-level vector quantization and query-guided bidirectional diffusion mechanism.

## Dataset: Heartcare-220K

We construct **Heartcare-220K**, a comprehensive, fine-grained multimodal ECG instruction dataset that supports unified modeling across key tasks such as disease diagnosis, waveform morphology analysis, rhythm interpretation, report generation. It combines two sources: the public [PTB-XL dataset](https://physionet.org/content/ptb-xl/1.0.3/) with 21,799 12-lead ECG signals annotated with 179 SCP-ECG classes, and 12,170 ECG images with structured reports from top hospitals, including scanned traces, clinical conclusions, and de-identified metadata—substantially enriching modality and label diversity.

<p align="center">
<img src="images/donut_charts.jpg" style="width:80%;vertical-align:middle;" />
</p>

To transform heterogeneous ECG data into structured supervision, we develop **HeartAgent**, a modular multi-agent engine with a bottom-up pipeline that ensures annotation consistency and generates high-quality instruction-style QA pairs, significantly boosting both scalability and data quality.

<img src="images/engine.jpg" style="vertical-align:middle;" />

## Benchmark: Heartcare-Bench

We introduce **Heartcare-Bench**, a framework for systematically evaluating diagnostic intelligence in ECG scenarios. It covers tasks including closed-ended and open-ended QA, report generation, signal reconstruction, and trend prediction, grouped into three clinically grounded categories: Diagnostic, Form, and Rhythm.

## Model: HeartcareGPT

We propose **Bidirectional ECG Abstract Tokenization (Beat)**, a hierarchical, structure-aware discrete encoding framework tailored for ECG time-series data. Beat compresses raw ECG signals into token sequences based on vector quantization that can be directly consumed by MLLMs. These discrete representations are directly embedded into the vocabulary of MLLMs, enabling our proposed Med-MLLMs, **HeartcareGPT**, to perform end-to-end reasoning across signals, text, and images.

<img src="images/method.jpg" style="vertical-align:middle;" />
