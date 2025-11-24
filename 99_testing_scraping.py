from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import List


### APPROACH TO FIND THE
# <span class="offer-container">
#   ├── <p class="offer__label__text">Subscription</p>
#   └── <picture class="picture-element">
#       └── <img alt="HBO Max">

def extract_streaming_providers(url: str) -> List[str]:
    """
    Extract VOD streaming providers from a JustWatch movie page.
    Finds all offers labeled as "Subscription".

    Args:
        url: JustWatch movie URL (e.g., https://www.justwatch.com/us/movie/dune-part-two-2023)

    Returns:
        List of streaming provider names with subscription offers
    """
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Navigate to the URL - use 'domcontentloaded' instead of 'networkidle'
            page.goto(url, wait_until='domcontentloaded', timeout=30000)

            # Wait for the offer elements to appear
            try:
                page.wait_for_selector('p.offer__label__text', timeout=10000)
            except:
                print("Offer elements not found, continuing anyway...")

            # Wait a bit more for dynamic content
            page.wait_for_timeout(3000)

            # Get the rendered HTML
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')

            # Find all <span class="offer-container"> elements
            offer_containers = soup.find_all('span', class_='offer-container')

            providers = []

            for container in offer_containers:
                # Check if this container has a subscription label
                label = container.find('p', class_='offer__label__text')

                if label and label.get_text(strip=True) == 'Subscription':
                    # Find the picture element with provider info
                    picture = container.find('picture', class_='picture-element')

                    if picture:
                        # Extract the img alt attribute
                        img = picture.find('img', alt=True)
                        if img and img.get('alt'):
                            providers.append(img['alt'])

            # Remove duplicates while preserving order
            providers = list(dict.fromkeys(providers))

            return providers

        except Exception as e:
            print(f"Error: {e}")
            return []

        finally:
            browser.close()


if __name__ == "__main__":
    test_url = "https://www.justwatch.com/us/movie/dune-part-two-2023"

    print("Extracting subscription streaming providers...")
    providers = extract_streaming_providers(test_url)
    print(f"Providers: {providers}")