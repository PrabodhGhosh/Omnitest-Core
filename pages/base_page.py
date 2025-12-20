import logging
from typing import Union

from playwright.sync_api import Page, Locator, Response, expect

from config.settings import settings

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, page:Page):
        self.page = page
        self.base_url = settings.UI_BASE_URL


    def _get_locator(self, selector_or_locator: Union[str, Locator]) -> Locator:
        """Helper to ensure we are always working with a Locator object."""
        if isinstance(selector_or_locator, str):
            return self.page.locator(selector_or_locator)
        return selector_or_locator

    def navigate(self, endpoint:str = ""):
        url = f"{self.base_url}/{endpoint}".strip("/")
        logger.info(f"Navigating to: {url}")
        response= self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
        self.wait_for_load()
        return response

    # ----- Injecting Global Behavior ----------

    def click(self, selector_or_locator: Union[str, Locator], name: str = "Element"):
        locator = self._get_locator(selector_or_locator)
        try:
            logger.info(f"Clicking on: {name}")
            # Playwright Locators have built-in auto-waiting
            locator.click()
        except Exception as e:
            logger.error(f"Failed to click on {name}: {e}")
            self.page.screenshot(path=f"failure_click_{name}.png")
            raise

    def fill(self, selector_or_locator: Union[str, Locator], value: str, name: str = "Input Field", secret: bool = False):
        locator = self._get_locator(selector_or_locator)
        log_value = "******" if secret else value
        logger.info(f"Filling {name} with {log_value}")

        try:
            # wait_for_selector is handled automatically by Locator.fill()
            locator.fill(value)
        except Exception as e:
            logger.error(f"Failed to fill {name}: {e}")
            self.page.screenshot(path=f"failure_fill_{name}.png")
            raise

    def get_text(self, selector_or_locator: Union[str, Locator]) -> str:
        locator = self._get_locator(selector_or_locator)
        # Using inner_text() which is generally preferred for visible text
        text = locator.inner_text()
        return text.strip() if text else ""

    def wait_for_load(self):
        """
        Stability for WSL/Windows
        Injects a global synchronization point to wait for the page to be 'quiet'.
        """
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            logger.warning("Network did not reach idle state, but continuing...")
