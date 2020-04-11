# Project documentation

## Selenium

## Scrapy
Root directory for scrapy project: "web_scraping/project_scrapy/justjoinit_scraper"

### Requirements/Instalation
Run in console "pip install -r requirements" to install libraries:
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
