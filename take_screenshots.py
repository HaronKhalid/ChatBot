# take_screenshots.py - Automated Screenshot Capture for ChatBot
import os
import sys
import time
import threading
from unittest.mock import MagicMock

# 1. Create Mock OpenAI class to run completely offline
class MockMessage:
    def __init__(self, content):
        self.content = content

class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

# Detailed Markdown response to showcase markdown rendering and Islamic teacher persona
mock_markdown_response = (
    "### What is Tawakkul (التوكل)?\n\n"
    "**Tawakkul** (reliance on Allah) is a central concept in Islam. It is the action of putting your absolute trust in Allah's plan while making your best effort.\n\n"
    "#### 1. Meaning of Tawakkul\n"
    "Tawakkul comes from the root word *wakala*, which means to entrust or delegate. Linguistically, it means relying on someone else for guidance, protection, or outcomes.\n\n"
    "#### 2. The Core Concept (Tying Your Camel)\n"
    "There is a famous Hadith from the Prophet Muhammad (ﷺ):\n"
    "> An Arab Bedouin asked the Prophet (ﷺ), \"Should I tie my camel and trust in Allah, or leave it untied and trust in Allah?\" The Prophet (ﷺ) replied, **\"Tie your camel and put your trust in Allah.\"** *(Tirmidhi)*\n\n"
    "#### 3. Quranic Evidence\n"
    "Allah (SWT) mentions the importance of Tawakkul in the Holy Quran:\n"
    "> *\"And whoever relies upon Allah - then He is sufficient for him.\"* — **(Surah At-Talaq, 65:3)**\n\n"
    "#### Key Takeaways:\n"
    "- **Effort is required**: We must take action first, then leave the outcome to Allah.\n"
    "- **Peace of mind**: True Tawakkul brings tranquility to the heart, knowing that whatever happens is by Allah's wisdom."
)

mock_openai_inst = MagicMock()
mock_openai_inst.chat.completions.create.return_value = MockResponse(mock_markdown_response)

class DummyOpenAI:
    def __init__(self, *args, **kwargs):
        pass
    
    @property
    def chat(self):
        return mock_openai_inst.chat

# Inject mock openai module before importing the Flask app
sys.modules['openai'] = MagicMock()
import openai
openai.OpenAI = DummyOpenAI

# 2. Import Flask app and run it in a daemon thread
print("Importing ChatBot application...")
import app as chatbot_app

print("Starting ChatBot Flask application on thread...")
server_thread = threading.Thread(
    target=lambda: chatbot_app.app.run(debug=False, port=5000, use_reloader=False)
)
server_thread.daemon = True
server_thread.start()

# Wait for the Flask server to start
print("Waiting for server to spin up...")
time.sleep(2)

# 3. Create screenshots folder
screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(screenshot_dir, exist_ok=True)
print(f"Created screenshots directory at: {screenshot_dir}")

# 4. Use Playwright to capture screenshots
from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        print("Launching headless Chromium browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Desktop viewport size
        page.set_viewport_size({"width": 1200, "height": 800})
        
        base_url = "http://127.0.0.1:5000"
        
        # View 1: Welcome / Landing Page
        print(f"Navigating to {base_url}...")
        page.goto(base_url, wait_until="networkidle")
        page.wait_for_timeout(500)
        
        welcome_screenshot_path = os.path.join(screenshot_dir, "welcome.png")
        page.screenshot(path=welcome_screenshot_path)
        print(f"Saved welcome screen: {welcome_screenshot_path}")
        
        # View 2: Click Suggestion and wait for Response
        print("Clicking 'What is Tawakkul?' suggestion...")
        # Select the suggestion button
        page.click('.sug-btn:has-text("What is Tawakkul?")')
        
        # Wait a fixed amount of time for typewriter effect to complete
        print("Waiting 15 seconds for AI response typing effect to finish...")
        page.wait_for_timeout(15000)
        
        chat_screenshot_path = os.path.join(screenshot_dir, "chat_demo.png")
        page.screenshot(path=chat_screenshot_path)
        print(f"Saved chat screen: {chat_screenshot_path}")
        
        print("Closing browser...")
        browser.close()
        
except Exception as e:
    print(f"Error during screenshot automation: {e}")
    sys.exit(1)

print("Screenshot automation completed successfully.")
sys.exit(0)
