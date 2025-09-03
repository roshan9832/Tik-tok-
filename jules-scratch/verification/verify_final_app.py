import pathlib
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # iPhone XR viewport
        context = browser.new_context(viewport={'width': 414, 'height': 896})
        page = context.new_page()

        # Get the absolute path to the HTML files
        base_path = pathlib.Path.cwd()
        index_url = f"file://{base_path / 'frontend' / 'index.html'}"
        upload_url = f"file://{base_path / 'frontend' / 'upload.html'}"
        messages_url = f"file://{base_path / 'frontend' / 'messages.html'}"
        profile_url = f"file://{base_path / 'frontend' / 'profile.html'}"
        chat_url = f"file://{base_path / 'frontend' / 'chat.html'}"

        # 1. Start at the main page
        print(f"Navigating to {index_url}")
        page.goto(index_url, wait_until="load")
        expect(page.locator("#footer-placeholder")).to_contain_text("Home")
        print("On index.html, footer loaded.")

        # 2. Navigate to Messages page
        page.locator('a[href="messages.html"]').click()
        expect(page).to_have_url(messages_url)
        print("Navigated to messages.html")

        # 3. Navigate to Chat page
        page.locator('a[href="chat.html"]').click()
        expect(page).to_have_url(chat_url)
        print("Navigated to chat.html")

        # 4. Navigate from Chat to Profile
        page.locator('a[href="profile.html"]').click()
        expect(page).to_have_url(profile_url)
        print("Navigated to profile.html")

        # 5. Navigate from Profile to Upload
        page.locator('a[href="upload.html"]').click()
        expect(page).to_have_url(upload_url)
        print("Navigated to upload.html")

        # 6. Navigate from Upload back to Home
        page.locator('a[href="index.html"]').click()
        expect(page).to_have_url(index_url)
        print("Navigated back to index.html.")

        # Final verification: check active link and take screenshot
        expect(page.locator('a[data-nav-link="index.html"]')).to_have_class(
            "flex flex-1 flex-col items-center justify-end gap-1 rounded-full text-white"
        )
        page.screenshot(path="jules-scratch/verification/final_app.png")
        print("Screenshot of final state taken. All links verified.")

        browser.close()

if __name__ == "__main__":
    run_verification()
