SMS Analysis: Natural Language Processing
=========================================

[![pip](https://img.shields.io/badge/pip-v9.0.1-blue.svg)](https://pypi.python.org/pypi/pip) [![Python 3](https://img.shields.io/badge/Python-3.5%2C%203.6-blue.svg)](https://docs.python.org/3/) [![MIT Licence](https://img.shields.io/github/license/ouassimBenMosbah/sms_analysis.svg)](https://github.com/ouassimBenMosbah/sms_analysis/blob/master/LICENSE) [![Build Status](https://travis-ci.org/ouassimBenMosbah/sms_analysis.svg?branch=master)](https://travis-ci.org/ouassimBenMosbah/sms_analysis)

# Detection of suspicious messages.

This program aim to help judicial experts to detect suspicious messages. It takes as a parameter an xml file containing all the messages and output a new xml file containing many messages sorted from the most suspicious message to the less suspicious one. Those suspicious messages are detected by using french natural language processing.

## Installation

```python
> pip3 install -r requirements.txt
```

## Usage

```python
> python3 main/main.py
```
A folder named `results` containing the results files will be created. It is recommended to open those xml files in your browser for a better visualization.

## Customization

- In order to improve the antispam filter, you can add spams in `french_antispam/list_spams.txt` or add normal messages in `french_antispam/list_hams.txt`. Once it is done, you have to execute `python french_antispam/model_init.py` to save the new model.

- In order to improve the sms -> frnech translator, you can add new words. The wrongly spelled words will be added to `sms_dico/sms.py` while the correctly spelled word will be added in `sms_dico/sms_traduction.py` (Each word should be added at the same line in both files).

- In order to improve the sms rate, you can modify the rate of a word or add a new word to the file `custom_textblob/textblob_fr/fr-sentiment.xml` (You should be aware that  all the words contained in this file have been stemmed and you should do so before adding new words !).

## Authors

- Ouassim BEN MOSBAH
- Clément BOULY

