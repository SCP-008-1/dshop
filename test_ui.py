from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/home/jules/verification/videos")
        page = context.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: console_messages.append(f"[pageerror] {err}"))

        page.goto("http://localhost:8080")
        page.wait_for_timeout(500)

        # Take initial homepage screenshot
        page.screenshot(path="/home/jules/verification/screenshots/verification.png", full_page=True)
        page.wait_for_timeout(500)

        # Click on the card body directly (testing whole card clickability)
        first_card = page.locator(".package-card").first
        first_card.click()
        page.wait_for_timeout(500)

        # Screenshot modal with overview & trust/resource panels
        page.screenshot(path="/home/jules/verification/screenshots/modal_card_clicked.png")
        page.wait_for_timeout(500)

        # Switch modal tabs
        page.click("#modalTabBtnReadme")
        page.wait_for_timeout(800)
        page.click("#modalTabBtnCompatibility")
        page.wait_for_timeout(500)
        page.click("#modalTabBtnReviews")
        page.wait_for_timeout(500)

        # Close modal
        page.click("#detailCloseBtn")
        page.wait_for_timeout(500)

        # Test Omnibar Search with Enter key
        page.click("#searchInput")
        page.fill("#searchInput", "mcp")
        page.wait_for_timeout(300)
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)

        # Toggle theme
        page.click("#themeToggleBtn")
        page.wait_for_timeout(500)

        # Toggle language
        page.click("#langToggleBtn")
        page.wait_for_timeout(1000)

        context.close()
        browser.close()

        print("Console messages:")
        for m in console_messages:
            print(m)

if __name__ == "__main__":
    test()
