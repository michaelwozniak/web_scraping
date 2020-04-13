# Project documentation

## Selenium
Root directory for selenium project: "web_scraping/project_selenium"

### Requirements/Instalation
Run in the console "pip install -r requirements" to install libraries:
  * selenium~=3.141.0

Proper Selenium webdriver is needed. In this part of project geckodriver (Firefox) is used.
In the directory "justjoinit_scraper/geckodriver" there is provided geckodriver 71.0.0.7222.

If you decide to use other drivers, please swap driver file in the directory "justjoinit_scraper/project_selenium".
Please also change code in "justjoinit_scraper.py" file (lines: 36, 38 and 43).

### User manual
0. Go to the directory: "web_scraping/project_selenium/"
1. Default option for driver is headless mode. You can change it in __init__.
2. Run in the console "python justjoinit.py" to save scraping results in filename.csv. 
3. Configure your scraper by answering on 3 questions about: 100_pages condition, salary range and location. The answer method is described in detail in the program.
4. Wait for the scraping to finish.
5. Analyze filename.csv :) 
6. Analyze logs from scraping in an adequate file from the "logs" folder.

### Example
Let's scrape job offers from Łódź in the salary range [10000, 14000].

0. Go to the directory: "web_scraping/project_scrapy/justjoinit_scraper/justjoinit_scraper/"
1. Run in the console "scrapy crawl justjoinit -o example_limit100_lodz_10000_140000.csv"
2. Do you want to set the page limit to 100? [T/F]: **T**
3. Do you want to scrap offers from all over Poland [T]? If not, press [F].: **F**
4. Please type, Which city are you interested in: 'Berlin', 'Białystok', 'Bielsko-Biała', 'Billund', 'Bremen', 'Burbank', 'Bydgoszcz', 'Chicago', 'Chorzów', 'Culver City', 'Częstochowa', 'Dublin', 'Düsseldorf', 'Dąbrowa Górnicza', 'Gdańsk', 'Gdynia', 'Gliwice', 'Helsinki', 'Irvine', 'Katowice', 'Kielce', 'Kraków', 'Kroměříž', 'Kwidzyn', 'København', 'London', 'Londyn', 'Los Angeles', 'Los Gatos', 'Lublin', 'Lund/Stockholm', 'Luxembourgh', 'Malmo', 'Marki', 'Mediolan', 'Miami Beach', 'München', 'New York', 'Norymberga', 'Nowy Jork', 'Olsztyn', 'Opole', 'Ostrów Wielkopolski', 'Palo Alto', 'Paris', 'Pasadena', 'Portland', 'Poznań', 'Road Town', 'Rybnik', 'Rzeszów', 'Sadowa', 'San Francisco', 'Seattle', 'Singapore', 'Sopot', 'Swarzędz', 'Szczecin', 'Tczew', 'Toruń', 'Tychy', 'Unterföhring', 'Ustroń', 'Valetta', 'Warsaw', 'Warszawa', 'Wałbrzych', 'Wrocław', 'Zabierzów', 'Zielona Góra', 'Łódź', 'Świdnica', 'Краків': **Łódź**
5. Do you want to provide boundaries of salary (logical alternative) [T/F]: **T**
6. Please provide lower boundaries:: **10000**
7. Please provide upper boundaries: **14000**
8. Wait for the scraping to finish.
9. Analyze "justjoinit_scraper/example_limit100_lodz_10000_140000.csv".
5. Analyze logs from scraping in an adequate file from the "justjoinit_scraper/logs" folder.

Obtained file is available in the directory: "web_scraping/project_selenium/example_limit100_lodz_10000_140000.csv". 

### Project tree
```bash
└───project_selenium
    ├───logs
    │       log_2020_04_11_20_52_48.526360.txt
    │   geckodriver.exe
    │   geckodriver.txt
    └───justjoinit_scraper.py

```


## Scrapy
Root directory for scrapy project: "web_scraping/project_scrapy/justjoinit_scraper"

### Requirements/Instalation
Run in the console "pip install -r requirements" to install libraries:
  * scrapy~=1.6.0
  * scrapy_selenium~=0.0.7
  * selenium~=3.141.0

Proper Selenium webdriver is needed. In this project chromedriver is used.
In the directory "justjoinit_scraper/selenium/driver" there is provided chromedriver v.81.0.4044.92 (so you need Google Chrome v.81.0.4044.92)

If you decide to use other drivers, please swap driver file in the directory "justjoinit_scraper/selenium".
Please also change code in "justjoinit_scraper/settings.py" file (lines: 99-100).

```python
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = 'selenium_driver/chromedriver'
```

### User manual
0. Go to the directory: "web_scraping/project_scrapy/justjoinit_scraper/justjoinit_scraper/"
1. Run in the console "scrapy crawl justjoinit -o filename.csv" to save scraping results in filename.csv (optionally use json). 
2. Configure your scraper by answering on 3 questions about: 100_pages condition, localization and salary range. The answer method is described in detail in the program.
3. Wait for the scraping to finish.
4. Analyze filename.csv :) 
5. Analyze logs from scraping in an adequate file from the "justjoinit_scraper/logs" folder.

### Example
Let's scrape job offers from Łódź in the salary range [10000, 14000].

0. Go to the directory: "web_scraping/project_scrapy/justjoinit_scraper/justjoinit_scraper/"
1. Run in the console "scrapy crawl justjoinit -o example_limit100_lodz_10000_140000.csv"
2. Do you want to set the page limit to 100? [T/F]: **T**
3. Do you want to scrap offers from all over Poland [T]? If not, press [F].: **F**
4. Please type, Which city are you interested in: 'Berlin', 'Białystok', 'Bielsko-Biała', 'Billund', 'Bremen', 'Burbank', 'Bydgoszcz', 'Chicago', 'Chorzów', 'Culver City', 'Częstochowa', 'Dublin', 'Düsseldorf', 'Dąbrowa Górnicza', 'Gdańsk', 'Gdynia', 'Gliwice', 'Helsinki', 'Irvine', 'Katowice', 'Kielce', 'Kraków', 'Kroměříž', 'Kwidzyn', 'København', 'London', 'Londyn', 'Los Angeles', 'Los Gatos', 'Lublin', 'Lund/Stockholm', 'Luxembourgh', 'Malmo', 'Marki', 'Mediolan', 'Miami Beach', 'München', 'New York', 'Norymberga', 'Nowy Jork', 'Olsztyn', 'Opole', 'Ostrów Wielkopolski', 'Palo Alto', 'Paris', 'Pasadena', 'Portland', 'Poznań', 'Road Town', 'Rybnik', 'Rzeszów', 'Sadowa', 'San Francisco', 'Seattle', 'Singapore', 'Sopot', 'Swarzędz', 'Szczecin', 'Tczew', 'Toruń', 'Tychy', 'Unterföhring', 'Ustroń', 'Valetta', 'Warsaw', 'Warszawa', 'Wałbrzych', 'Wrocław', 'Zabierzów', 'Zielona Góra', 'Łódź', 'Świdnica', 'Краків': **Łódź**
5. Do you want to provide boundaries of salary (logical alternative) [T/F]: **T**
6. Please provide lower boundaries:: **10000**
7. Please provide upper boundaries: **14000**
8. Wait for the scraping to finish.
9. Analyze "justjoinit_scraper/example_limit100_lodz_10000_140000.csv".
5. Analyze logs from scraping in an adequate file from the "justjoinit_scraper/logs" folder.

Obtained file is available in the directory: "web_scraping/project_scrapy/justjoinit_scraper/justjoinit_scraper/example_limit100_lodz_10000_140000.csv". 

### Project tree
```bash
└───justjoinit_scraper
    │   requirements.txt
    │   scrapy.cfg
    │
    └───justjoinit_scraper
        │   debug.log
        │   example_limit100_lodz_10000_140000.csv
        │   items.py
        │   middlewares.py
        │   pipelines.py
        │   settings.py
        │   __init__.py
        │
        ├───logs
        │       log_2020_04_11_20_52_48.526360.txt
        │
        ├───selenium_driver
        │       chromedriver.exe
        │
        └──────spiders
            │   justjointit.py
            └───   __init__.py 
```
Differences in the project compared to the default Scrapy configuration:
* added requirements.txt file (mentioned in the Requirements/Instalation)
* added middlewares: scrapy-selenium (added selenium_driver/chromedriver.exe and changed settings.py - mentioned in the Requirements/Instalation) 
* added logs (mentioned in the User manual)
