from playwright.sync_api import sync_playwright
import time

USERNAME = "spector2701"
PASSWORD = "theInsider"
VIDEO_PATH = "path_to_your_video.mp4"
CAPTION = "Your Reel caption here"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Login
    page.goto("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    page.fill("input[name='username']", USERNAME)
    page.fill("input[name='password']", PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_timeout(5000)

    # Go to Create page
    page.goto("https://www.instagram.com/")
    time.sleep(3)
    page.click("[aria-label='New post']")  # or use selector for "+" icon

    # Upload Reel (this part may vary by layout changes on Instagram)
    page.set_input_files("input[type='file']", VIDEO_PATH)

    # Wait for video upload UI
    time.sleep(5)

    # Click next buttons & post
    page.click("text=Next")
    time.sleep(3)
    page.click("textarea")  # caption box
    page.fill("textarea", CAPTION)
    time.sleep(1)
    page.click("text=Share")

    print("Posted successfully!")
    time.sleep(10)
    browser.close()
