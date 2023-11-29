# Парсер таблиц и логов автотестов prog-intro

**По этому парсеру был создан более удобный [сайт](http://prog-intro.ddns.net). [Github](https://github.com/Vaniog/prog-intro-tests-parser/tree/flask)**

На оригинальный парсер было потрачено ровно столько сил и времени, сколько было на паре английского

Поэтому прошу не осуждать за очень некачественный код и/или реализацию

## New features
- concurrency
- update checker
- automatical group filling

## Installation

Python3 must be installed (tested using 3.11.6)

```
pip3 install -r requirements.txt
```

## Usage

Configurate `config.py` with desired credentials

Then:

```
python3 main.py
```

Script will parse pages, generate html file and open it in your favorite browser

## Feel free to fork 

Идеи для ваших форков или проектов с нуля

- Сделать глобальную удобную табличку для всех OS с возможностью быстрого поиска

- Сделать страничку, на которой по имени можно будет узнать результаты тестирования(пропадает необходимость config.py)

- <s>Провести конкурс на самый красивый парсер</s>
