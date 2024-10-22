import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

class MovieScraper:
	def __init__(self, base_url, lists_to_search):
		self.base_url = base_url
		self.lists_to_search = lists_to_search
		self.catalogue_to_scrape = []  # Stores the URLs of catalogues to scrape
		self.movie_data = []  # Stores all scraped movie data
		self.user_reviews = []  # Stores all the user reviews for a single movie iteration and then clears
		self.movie_reviews = []  # Stores all the reviews for a movie
		self.driver = self.setup_driver()  # WebDriver initialization

	def setup_driver(self):
		"""Set up the Selenium WebDriver with Chrome options."""
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("--start-maximized")
		# chrome_options.add_argument("--headless")  # Uncomment for headless mode
		return webdriver.Chrome(options=chrome_options)

	def load_paginated_content(self, next_button_selector, item_selector):
		"""Function to load paginated content of the catalogue or movie review pages."""
		for _ in range(self.lists_to_search):
			current_items_count = len(self.driver.find_elements(By.CLASS_NAME, item_selector))
			next_button = self.driver.find_element(By.CLASS_NAME, next_button_selector)
			self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
			next_button.click()
			# Wait for new content to load
			WebDriverWait(self.driver, 10).until(
				lambda _: len(self.driver.find_elements(By.CLASS_NAME, item_selector)) > current_items_count
			)

	def scrape_catalogues_from_search(self):
		"""Scrape URLs of catalogues from the search page."""
		self.driver.get(self.base_url)
		time.sleep(8)
		self.driver.execute_script("window.stop()")
		self.load_paginated_content('load-more-search', 'list-link')
		hrefs = self.driver.find_elements(By.CLASS_NAME, 'list-link')
		for href in hrefs:
			url = href.get_attribute('href')
			self.catalogue_to_scrape.append(url)

	def scroll_to_load_content(self):
		"""Scroll the page to load dynamic content."""
		time.sleep(3)  # Let the page content load
		self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight/2)')
		time.sleep(3)  # Allow more content to load after scrolling

	def extract_movie_data_from_catalogue(self, url):
		"""Extract movie data from the provided URL."""
		self.driver.get(url)
		time.sleep(8)
		self.driver.execute_script("window.stop()")
		self.scroll_to_load_content()  # Load dynamic content
		movie_elements = self.driver.find_elements(By.CLASS_NAME, 'frame')  # Get movie elements

		for movie_metadata in movie_elements:
			movie_url = movie_metadata.get_attribute('href')
			movie_info = movie_metadata.get_attribute('data-original-title')

			if movie_info:  # Ensure movie info is available
				self.parse_and_store_movie_data(movie_info, movie_url)

		self.load_paginated_content_for_movies(is_review_page=False)

	def parse_and_store_movie_data(self, movie_info, movie_url):
		"""Parse and store movie data."""
		# Regex to extract movie name, year, and rating
		movie_pattern = re.compile(r'^(.*?)\s\((\d{4})\)\s(★{1,5}½?)$')
		match = movie_pattern.match(movie_info)

		if match:  # Only proceed if regex matches
			movie_name = match.group(1)
			print(movie_name)
			movie_year_of_release = match.group(2)
			movie_rating = match.group(3) if match.group(3) else 'No rating'

			# Append movie data as a dictionary
			self.movie_data.append({
				'url': movie_url,
				'name': movie_name,
				'year': movie_year_of_release,
				'rating': movie_rating
			})

	def load_paginated_content_for_movies(self, is_review_page):
		"""Handle pagination by clicking the 'Next' button and recursively scraping more pages."""
		try:
			next_button = WebDriverWait(self.driver, 3).until(
				EC.element_to_be_clickable((By.CLASS_NAME, 'next'))
			)
			while next_button.is_enabled():
				new_url = next_button.get_attribute('href')
				print("Navigating to the next page:", new_url)

				if is_review_page:
					self.scrape_movie_reviews(new_url)
				else:
					self.extract_movie_data_from_catalogue(new_url)  # Recursive call to scrape next page
		except:
			print(f"No more pages to load in this catalogue")

	def scrape_movie_reviews(self, url):
		"""Scrape reviews of a movie from the given URL."""
		self.driver.get(url)
		# Expand all the reviews
		more_links = self.driver.find_elements(By.CLASS_NAME, 'reveal.js-reveal')
		for more in more_links:
			try:
				self.driver.execute_script("arguments[0].scrollIntoView(true);", more)
				more.click()
				time.sleep(3)
			finally:
				continue

		reviews = self.driver.find_elements(By.CLASS_NAME, 'body-text')
		for review in reviews:
			self.user_reviews.append(review.text)

		self.load_paginated_content_for_movies(is_review_page=True)

	def get_user_reviews(self, movies):
		"""Get user reviews for each movie."""
		for movie in movies:
			# Clear user reviews of the old iteration
			self.user_reviews.clear()
			review_page = movie['url'] + 'reviews/by/activity/'
			self.scrape_movie_reviews(review_page)

			self.movie_reviews.append({
				'name': movie['name'],
				'reviews': self.user_reviews
			})

		return self.movie_reviews

	def find_tamil_movies(self):
		"""Scraping pipeline"""
		# Scrape all the catalogue available
		self.scrape_catalogues_from_search()

		# For each catalogue URL, extract movie data
		for url in self.catalogue_to_scrape:
			self.extract_movie_data_from_catalogue(url)

		self.driver.quit()  # Close the browser when done
		return self.movie_data


if __name__ == "__main__":
	# list_to_search: 
	# Number of paginated catalogue results to search.
	# Higher the value, more time it will take to scrape all the Tamil movies
	scraper = MovieScraper("https://letterboxd.com/search/lists/tamil/", lists_to_search=1)
	movie_data = scraper.find_tamil_movies()
	movie_reviews = scraper.get_user_reviews(movie_data)
	print(movie_reviews)
	
	
# Store in DB 
# Use LLM models (ideally ChatGPT's model), to rank the movies in the CSV
