import logging
from playwright.sync_api import Page, Response, expect

from config.settings import settings

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, page:Page):
        self.page = page
        self.base_url = settings.UI_BASE_URL


    def navigate(self, endpoint:str = ""):
        url = f"{self.base_url}/{endpoint}".strip("/")
        logger.info(f"Navigating to: {url}")
        return self.page.goto(url, wait_until="networkidle")

    # ----- Injecting Global Behavior ----------

    def click(self, selector:str, name:str = "Element"):
        """
        Unified Logging & Enhanced Actionability
        Instead of just clicking, we log the human-readable name of the element.
        """
        try:
            logger.info(f"Clicking on: {name}")
            self.page.click(selector)
        except Exception as e:
            """
            Global Error Handling
            We can trigger a screenshot automatically on any click failure 
            """
            logger.info(f"Failed to click on {name}:{e}")
            self.page.screenshot(path=f"failure_{name}.png")
            raise

    def fill(self, selector:str, value:str, name:str="Input Field", secret: bool=False):
        """
        Security & Debugging
        If 'secret' is True, we don't log the actual value (e.g., passwords).
        """
        log_value = "******" if secret else value
        logger.info(f"Filling {name} with {log_value}")
        """
        Explicit Wait before interaction
        Ensures the field is ready for input even if the UI is lagging
        """
        self.page.wait_for_selector(selector,state="visible")
        self.page.fill(selector,value)

    def get_text(self, selector:str) -> str:
        """
        Standardization ensures we always strip whitespace from UI text for cleaner assertions.

        """
        self.page.wait_for_selector(selector)
        text = self.page.text_content(selector)
        return text.strip() if text else ""

    def wait_for_load(self):
        """
        Stability for WSL/Windows
        Injects a global synchronization point to wait for the page to be 'quiet'.
        """
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")
