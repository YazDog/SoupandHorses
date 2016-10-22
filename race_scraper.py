from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import datetime

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
	driver = webdriver.Chrome('/Users/tim/Desktop/The Project/Chrome Driver/chromedriver')
	driver.get(page)
	flucs = driver.find_element_by_xpath("//race-runners[@class='ng-isolate-scope']/div[@class='race-runners-wrapper']/div[@class='race-runners-menu-wrapper clearfix ng-scope']/menu[@class='form-filters-menu']/div[@class='different-button-grouped compact ng-scope']/button[@class='toggle-flucs-button different-button ng-scope button-inactive']/span[@class='long-title ng-binding']")
	flucs.click()
	html = driver.page_source
	driver.close()
	return html
	
def fetch_results(page):
	driver = webdriver.Chrome('/Users/tim/Desktop/The Project/Chrome Driver/chromedriver')
	driver.get(page)
	html = driver.page_source
	driver.close()
	return html

	
	
def race_name(html):
	"""
	Takes in HTML from a racing page and returns the race name and time as a list in this format:
	[number, time, horse name]
	"""
	soup = BeautifulSoup(html, 'html.parser')
		
	race_header = soup.find('header', class_='race-header')
		
	race_name_time = []
		
	for child in race_header.children:
		if type(child) == type(race_header):
			time = find_results(child, 'div', 'race-heading')
			name = find_results(child, 'div', 'race-name')
				
			if time and name:
				race_name_time.extend(time)
				race_name_time.extend(name)
		
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


def get_race_list_2(html):
	soup = BeautifulSoup(html, 'html.parser')
	race_table = soup.find('div', class_='race-card-races-wrapper')
	
	for child in race_table.children:
		if type(child) == type(race_table):
			for subchild in child:
				if type(subchild) == type(race_table):
					times = find_results(subchild, 'time', 'race-start-time')
					links = child.get('href')
					print(links)
					print(times)
					print(subchild)
				


def get_race_list(html):
	"""
	Returns a list of tuples, time in datetime format: [(html, time),]"""
	soup = BeautifulSoup(html, 'html.parser')
	race_table = soup.find('div', class_='race-card-domestic')
	a = race_table.find_all('a')
	
	times = []
	
	result = []
	
	for child in race_table.children:
		time_date = {}
		
		if type(child) == type(race_table):
			times = find_results(child, 'time', 'race-start-time')
			b = child.find_all('a')
			for link in b:
				print(link.get('href'))
#				links.append('https://www.tab.com.au{}'.format(link.get('href')))
			for time in times:
				print(time)
	
	
	links = []
	
	for link in a:
		links.append('https://www.tab.com.au{}'.format(link.get('href')))
		
		
	times_edit = []	
	
	for time in times:
		split = time.split(':')
		hours = int(split[0])
		minutes = int(split[1])
		
		date = datetime.date.today()
		time = datetime.time(hours, minutes)
		date_time = datetime.datetime.combine(date, time)
		
		times_edit.append(date_time)
	
#	final = []
#	for pair in zip(links, times_edit):
#		link_time = {}
#		link_time['link'] = pair[0]
#		link_time['datetime'] = pair[1]
		
		
	return zip(links, times_edit)
		
			

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
	
	
	
	
html = fetch_results('https://www.tab.com.au/racing/meetings/today/R')
races = get_race_list_2(html)


#for race in races:
#	print(race)








#for race in races:
#	race_html = fetch_results(race)
#	print(race_name(race_html))



#html = fetch_race('https://www.tab.com.au/racing/2016-10-20/PAKENHAM/PAK/R/8')
##print(race_name(html))
#race = race_souper(html)
#name = race_name(html)
#print(race)
#print('\n---------------------')
#
#
#for horse in race:
#	a = horse['flux']
#	b = json.loads(a)
#	print(b)
#	if horse['win'] == 'SCR':
#		continue
#	
#	else:
#		print(type(b[0]))

#html = fetch_results('https://www.tab.com.au/racing/2016-10-12/WARWICK-FARM/WFM/R/1')
#print(race_name(html))
#print(result_souper(html))