from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time

def find_results(source, tag = None, css_class = None):
	final = []
	result = source(tag, class_=css_class)
	
	for item in result:
		for strings in item.stripped_strings:
			final.append(strings)
	
	return final


def clean(lst):
	junk = ['Open Today', 'Today', 'Open']
	final = []
	for item in lst:
		if not item in junk:
			final.append(item)
			
	return final


def fetch_race(page):
	driver = webdriver.Chrome('C:\\Users\\User\Desktop/chromedriver')
	driver.get(page)
	flucs = driver.find_element_by_xpath("//race-runners[@class='ng-isolate-scope']/div[@class='race-runners-wrapper']/div[@class='race-runners-menu-wrapper clearfix ng-scope']/menu[@class='form-filters-menu']/div[@class='different-button-grouped compact ng-scope']/button[@class='toggle-flucs-button different-button ng-scope button-inactive']/span[@class='long-title ng-binding']")
	flucs.click()
	html = driver.page_source
	driver.close()
	return html
	
def fetch_results(page):
	driver = webdriver.Chrome('C:\\Users\\User\Desktop/chromedriver')
	driver.get(page)
	html = driver.page_source
	driver.close()
	return html
	
	
def race_name(html):
	soup = BeautifulSoup(html, 'html.parser')
		
	race_header = soup.find('header', class_='race-header')
		
	race_name_time = []
		
	for child in race_header.children:
		if type(child) == type(race_header):
			time = find_results(child, 'div', 'race-heading')
			name = find_results(child, 'div', 'race-name')
				
			if time and name:
				race_name_time.append(time)
				race_name_time.append(name)
		
	return race_name_time
	
	
def flux_cleaner(flux):
	result = []
	last_result = 0.0
		
	for num in flux:
		if not num == '–':
			add = float(num)
			result.append(add)
			last_result = add
		else:
			result.append(last_result)
		
	return result



def race_souper(html):
	
	soup = BeautifulSoup(html, 'html.parser')

	horse_table = soup.find('div', class_='pseudo-body')
	race_horses = []
	
	for child in horse_table.children:
		
		if type(child) == type(horse_table):
			name = find_results(child, 'div', 'runner-name-wrapper')
			tote = clean(find_results(child, 'ul', 'tote-mm-numbers-list'))
			win_cell = find_results(child, 'div', 'win-cell')
			place_cell = find_results(child, 'div', 'price-cell')
			metadata_cell = find_results(child, 'dl', 'runner-metadata-list')

			full_flux = tote[0:2]
			full_flux.extend(tote[-4:])
			
			if tote:
				full_flux = flux_cleaner(full_flux)

			full_flux_json = json.dumps(full_flux)

			horse = {}
			horse['name'] = name[0]
			horse['flux'] = full_flux_json
			horse['win'] = win_cell[0]
			horse['place'] = place_cell[2]
			horse['jockey'] = metadata_cell[1]
			horse['trainer'] = metadata_cell[3]
			horse['form'] = metadata_cell[5]
			horse['weight'] = metadata_cell[7]
			horse['rating'] = metadata_cell[9]
			
			race_horses.append(horse)
			
#			race_horses[name[0]] = horse
			
	return race_horses
	
		
def result_souper(html):
	
	soup = BeautifulSoup(html, 'html.parser')
	tag = soup.find('table', class_='race-table')
	tbody = tag.find('tbody')
	
	winners = []
	
	for child in tbody.children:
		if type(child) == type(tag):
			name = find_results(child, 'td', 'runner-details')
			fixed_odds = find_results(child, 'td', 'result-fixed-odds')
			place = find_results(child, 'td', 'result-position')
			
			horse = {}
			horse['name'] = name
			horse['fixed_odds'] = fixed_odds
			horse['place'] = place
			
			winners.append(horse)
			
				
	return winners
	
def scratch_remover(race):
	results = []
	for dictionary in race:
		if dictionary['win'] == 'SCR':
			continue

		else:
			results.append(dictionary)

	return results
	
#html = fetch_race('https://www.tab.com.au/racing/2016-10-12/WARWICK-FARM/WFM/R/8')
#print(race_name(html))
#print(race_souper(html))
#

#html = fetch_results('https://www.tab.com.au/racing/2016-10-12/WARWICK-FARM/WFM/R/1')
#print(race_name(html))
#print(result_souper(html))
