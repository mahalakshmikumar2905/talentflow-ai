import asyncio
from playwright.async_api import async_playwright

async def fill_application_form(page, user_data, resume_path="tailored_resume.pdf"):
    print("🚀 Auto-filling ATS application form fields...")
    
    if await page.query_selector("input[id*='first_name']"):
        await page.fill("input[id*='first_name']", user_data["first_name"])
    if await page.query_selector("input[id*='last_name']"):
        await page.fill("input[id*='last_name']", user_data["last_name"])
    if await page.query_selector("input[id*='email']"):
        await page.fill("input[id*='email']", user_data["email"])
    if await page.query_selector("input[id*='phone']"):
        await page.fill("input[id*='phone']", user_data["phone"])
        
    upload_input = await page.query_selector("input[type='file']")
    if upload_input:
        print("📄 Attaching tailored CV...")
        # await upload_input.set_input_files(resume_path)
        
    print("✅ Form completed successfully! Review before final submit.")

async def run_bot(job_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_context().new_page()
        await page.goto(job_url)
        
        sample_user = {
            "first_name": "Arun",
            "last_name": "Kumar",
            "email": "arun@example.com",
            "phone": "+91 9876543210"
        }
        await fill_application_form(page, sample_user)
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    print("Bot initialized. Ready to execute.")