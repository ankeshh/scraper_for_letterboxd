# Movie Scraper for Tamil Movies

This project is a web scraper built using Python and Selenium to extract movie data and user reviews from Letterboxd's Tamil movie lists. The scraper collects information such as the movie name, release year, rating, and user reviews from catalogued movie lists.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [TODO](#todo)
- [License](#license)

## Installation

To run this project, ensure you have the following prerequisites:

### Prerequisites

- Python 3.x
- [Selenium](https://www.selenium.dev/) for web scraping
- [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for Selenium
- Required Python libraries (can be installed via pip):

    ```bash
    pip install selenium
    ```

### Setup

1. Download and install ChromeDriver. Ensure the ChromeDriver version matches your installed Chrome version.
2. Add ChromeDriver to your system’s PATH or specify the driver path in the code.
3. Install the required Python libraries using:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Open the `scraper.py` file.
2. Modify the `base_url` and the `lists_to_search` parameters as needed. The default setup scrapes Tamil movies from Letterboxd.

    ```python
    scraper = MovieScraper("https://letterboxd.com/search/lists/tamil/", lists_to_search=1)
    ```

3. Run the script by executing:

    ```bash
    python3 -u scraper.py
    ```

## How It Works

- **`MovieScraper` Class**: Handles the main scraping logic.
  - **`scrape_catalogues_from_search`**: Scrapes Tamil movie catalogues.
  - **`extract_movie_data_from_catalogue`**: Extracts movie data from each list (movie title, year, and rating).
  - **`scrape_movie_reviews`**: Scrapes user reviews for each movie.
  - **`get_user_reviews`**: Combines all user reviews and stores them.
- **Pagination Handling**: Functions to navigate through paginated content, both for movie lists and user reviews.
- **Review Collection**: User reviews for each movie are gathered and stored alongside the movie details.

### Output

The script will output the scraped data and movie reviews in the following format:

```json
[
    {
        "name": "Anniyan",
        "reviews": [
            "Review 1 text...",
            "Review 2 text..."
        ]
    },
    {
        "name": "Kannathil Muthamittal",
        "reviews": [
            "Review 1 text...",
            "Review 2 text..."
        ]
    }
]
```

## TODO

- Store the scraped movie data and reviews in a database (e.g., SQLite, PostgreSQL).
- Export the scraped data to a CSV file.
- Use a Language Learning Model (LLM), such as GPT-3 or ChatGPT, to rank the movies based on their reviews and ratings.
- Improve error handling and edge case detection.

## License

This project is licensed under the MIT License.
