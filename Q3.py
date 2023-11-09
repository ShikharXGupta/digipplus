import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_categories():
    URL = 'https://www.upwork.com/ab/search-results/freelancer-jobs/all?sort=recency'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    categories = soup.find_all('option', {'data-testid': 'job-category-select-option'})
    category_names = [category.get('value') for category in categories]
    return category_names

def scrape_projects(category):
    URL = f'https://www.upwork.com/ab/search-results/freelancer-jobs/{category}?sort=recency'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    projects = soup.find_all('div', {'data-testid': 'job-card'})
    project_details = []
    for project in projects:
        title = project.find('h2', {'data-testid': 'job-title'}).text.strip()
        budget = project.find('div', {'data-testid': 'budget'}).text.strip()
        post_date = project.find('span', {'data-testid': 'post-date'}).text.strip()
        details = [title, budget, post_date]
        project_details.append(details)
    return project_details

def upload_to_sheet(sheet, project_details):
    sheet.clear()
    sheet.append_row(['Title', 'Budget', 'Post Date'])
    for project in project_details:
        sheet.append_row(project)

if __name__ == "__main__":
    # Replace with your own categories and sheet details
    categories = get_categories()
    # Filter out specific categories here
    #categories = ['web-development', 'graphic-design']
    all_projects = []
    for category in categories:
        all_projects.extend(scrape_projects(category))

    # Upload to google sheet
    # Replace 'your_creds.json' and 'your_sheet_name' with your own details
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('your_creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('your_sheet_name').sheet1
    upload_to_sheet(sheet, all_projects)