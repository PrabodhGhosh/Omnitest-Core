
![Omnitest CI](https://github.com/PrabodhGhosh/Omnitest-Core/actions/workflows/pipeline.yml/badge.svg)

# Omnitest-Core 🚀

A professional-grade automated testing framework designed for end-to-end (E2E) validation of web applications. This project demonstrates a hybrid testing approach combining **API**, **UI**, and **Integration** tests in a single pipeline.

---

## 📊 Live Test Reports
Every push to the main branch triggers a full test suite execution. You can view the latest results here:
👉 **[View Live Allure Report](https://prabodhghosh.github.io/Omnitest-Core/)**

---

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Test Runner:** Pytest
* **UI Automation:** Playwright
* **API Testing:** Requests
* **Reporting:** Allure Reports
* **Infrastructure:** Docker & GitHub Actions (Ubuntu 22.04)

## 🏗 Project Architecture
The project is structured to ensure clean separation of concerns:
- **`tests/api`**: Focuses on backend endpoint validation and schema checks.
- **`tests/ui`**: End-to-end user journey automation using Playwright.
- **`tests/hybrid`**: Specialized tests that use API for setup/cleanup and UI for verification.
- **`api_services/`**: Page Object Model (POM) equivalent for API clients.

## 🚀 Getting Started (Local Development)

### Prerequisites
- **WSL2 (Ubuntu 22.04)** is recommended for a seamless experience.
- Docker installed.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/PrabodhGhosh/Omnitest-Core.git](https://github.com/PrabodhGhosh/Omnitest-Core.git)
   cd Omnitest-Core
2. Build and run via Docker:
   ```bash
   docker build -t omnitest-core .
   docker run --env-file .env omnitest-core

### CI/CD Pipeline

This project utilizes GitHub Actions to automate the testing lifecycle:

**`Docker Build:`** Creates a consistent environment on Ubuntu 22.04.

**`Parallel Execution:`** Uses pytest-xdist to run tests across multiple workers.

**`Secret Masking:`** Sensitive credentials (USER_EMAIL, API_BASE_URL) are securely managed via GitHub Secrets.

**`Auto-Deployment:`** Post-test, the Allure results are processed and deployed to GitHub Pages.
