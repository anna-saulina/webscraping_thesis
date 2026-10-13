# Clinical Trial Safety Data NLP Pipeline

A Python-based NLP and web-scraping project for automated collection, processing, and preliminary analysis of adverse event data from ClinicalTrials.gov.

The project was developed as part of my university thesis in Mathematical Support and Administration of Information Systems and combines my background in clinical research and drug safety with hands-on programming and medical data analysis.

## Project objective

ClinicalTrials.gov contains a large amount of publicly available clinical trial safety data. Reviewing adverse events across multiple studies manually requires substantial data collection, cleaning, and structuring.

The objective of this project was to explore how automated data extraction and natural language processing techniques could be used to collect and preprocess adverse event information and prepare it for preliminary safety analysis.

## What the pipeline does

The pipeline:

1. Automatically identifies clinical trials with available results.
2. Navigates individual study records on ClinicalTrials.gov.
3. Extracts study-level information, including:
   - sponsor
   - condition
   - intervention
   - enrollment
4. Extracts reported Serious Adverse Events (SAEs).
5. Processes and cleans textual adverse event data.
6. Structures the extracted information for further analysis.
7. Aggregates adverse event data across clinical trials.
8. Performs preliminary analysis of SAE frequency.
9. Generates visualizations of the resulting safety data.
10. Saves structured results in JSON format.

## Technologies

- Python
- Natural Language Processing (NLP)
- Selenium
- pandas
- Matplotlib
- JSON

## Repository structure

- `scraper_clinical_trials_selenium.py` — automated collection and extraction of clinical trial and adverse event data
- `data_analysis.py` — preprocessing, aggregation, and exploratory analysis
- `constants.py` — constants used by the scraper
- `services.py` — utility functions
- `trial_data.json` — example structured output
- `trial-data-plot.pdf` — example visualization
- `requirements.txt` — project dependencies

## Clinical relevance

The project was designed at the intersection of clinical research, drug safety, and data science.

Its purpose was not to replace medical review or validated pharmacovigilance processes, but to explore how automation and NLP could support the collection and preliminary analysis of large volumes of publicly available clinical safety data.

This work reflects my broader interest in translating clinical questions into structured, computationally tractable problems and using technical tools to support medical evidence evaluation.

## Limitations

This is an academic exploratory project rather than a production pharmacovigilance system. ClinicalTrials.gov data have their own reporting limitations, and the outputs require medical interpretation before any conclusions about product safety can be made.

## Author

**Anna Saulina, MD**

Physician and clinical research professional with experience in clinical development, drug safety, medical monitoring, clinical evidence evaluation, and clinical data standards.
