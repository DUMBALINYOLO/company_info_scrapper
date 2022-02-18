# company_info_scrapper
A scrapper written in python to scrape https://find-and-update.company-information.service.gov.uk/register-of-disqualifications site 




1. Download Chrome Driver and add it to your path

2. python -m venv venvname

3. venvname\scripts\activate if windows

4. python -m pip install --upgrade pip

5. pip install -r requirements.txt

6. python main.py

It shall create a compnanies.xlsx file and scrape all the records including in paginated pages
and store it in the file. The file shall be divided in worksheets from A-Z as per the scrapped website