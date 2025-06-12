from bs4 import BeautifulSoup
from urllib.parse import urljoin

from ..utils import get_relevant_images, extract_title, get_text_from_soup, clean_soup

class BeautifulSoupScraper:

    def __init__(self, link, session=None):
        self.link = link
        self.session = session

    def scrape(self):
        """
        This function scrapes content from a webpage by making a GET request, parsing the HTML using
        BeautifulSoup, and extracting script and style elements before returning the cleaned content.
        
        Returns:
          The `scrape` method is returning the cleaned and extracted content from the webpage specified
        by the `self.link` attribute. The method fetches the webpage content, removes script and style
        tags, extracts the text content, and returns the cleaned content as a string. If any exception
        occurs during the process, an error message is printed and an empty string is returned.
        """
        try:
            # Increased timeout from 4 to 30 seconds to handle slower websites
            response = self.session.get(self.link, timeout=30)
            soup = BeautifulSoup(
                response.content, "lxml", from_encoding=response.encoding
            )

            soup = clean_soup(soup)

            content = get_text_from_soup(soup)

            image_urls = get_relevant_images(soup, self.link)
            
            # Extract the title using the utility function
            title = extract_title(soup)

            return content, image_urls, title

        except Exception as e:
            error_type = type(e).__name__
            if "timeout" in str(e).lower():
                print(f"Timeout error scraping {self.link}: {error_type} - {str(e)}")
            else:
                print(f"Error scraping {self.link}: {error_type} - {str(e)}")
            return "", [], ""