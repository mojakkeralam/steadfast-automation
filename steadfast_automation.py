from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time
import sys

def steadfast_payment_request():
    print("=" * 60)
    print("🚀 Steadfast Payment Request Automation Starting...")
    print("=" * 60)
    
    # Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # ChromeDriver service setup - try multiple paths
    import os
    import shutil
    
    # Find chromedriver
    chromedriver_path = shutil.which('chromedriver')
    if not chromedriver_path:
        chromedriver_paths = [
            '/usr/bin/chromedriver',
            '/usr/lib/chromium-browser/chromedriver',
        ]
        for path in chromedriver_paths:
            if os.path.exists(path):
                chromedriver_path = path
                break
    
    print(f"Using ChromeDriver at: {chromedriver_path}")
    
    driver = None
    try:
        if chromedriver_path:
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            # Try without explicit path
            driver = webdriver.Chrome(options=chrome_options)
        print(f"✓ ChromeDriver initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ChromeDriver: {str(e)}")
        sys.exit(1)
    
    try:
        # Chrome version info
        print(f"\n📌 Chrome Version: {driver.capabilities['browserVersion']}")
        print(f"📌 ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]}")
        
        # ==================== STEP 1: LOGIN ====================
        print("\n" + "="*60)
        print("STEP 1: LOGIN")
        print("="*60)
        
        print("📍 Navigating to login page...")
        driver.get("https://steadfast.com.bd/login")
        time.sleep(5)
        print(f"✓ Current URL: {driver.current_url}")
        
        print("\n🔐 Entering login credentials...")
        
        # Find email field
        email_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        print("✓ Email field found")
        
        # Find password field
        password_field = driver.find_element(By.NAME, "password")
        print("✓ Password field found")
        
        # Enter credentials
        email_field.clear()
        email_field.send_keys("mojakkeralam16@gmail.com")
        print("✓ Email entered")
        time.sleep(1)
        
        password_field.clear()
        password_field.send_keys("Libas@12")
        print("✓ Password entered")
        time.sleep(1)
        
        # Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        print("✓ Login button found")
        login_button.click()
        print("✓ Login button clicked")
        
        print("\n⏳ Waiting for dashboard to load...")
        time.sleep(8)
        print(f"✓ Current URL: {driver.current_url}")
        
        # ==================== STEP 2: PAYMENT REQUEST PAGE ====================
        print("\n" + "="*60)
        print("STEP 2: NAVIGATE TO PAYMENT REQUEST")
        print("="*60)
        
        print("💰 Going to payment request page...")
        driver.get("https://steadfast.com.bd/user/payment-request")
        time.sleep(5)
        print(f"✓ Current URL: {driver.current_url}")
        
        # ==================== STEP 3: SELECT BANK ====================
        print("\n" + "="*60)
        print("STEP 3: SELECT BANK FROM DROPDOWN")
        print("="*60)
        
        print("🔍 Looking for payment method dropdown...")
        
        # Find dropdown
        dropdown = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select"))
        )
        print("✓ Dropdown found")
        
        # Create Select object
        select = Select(dropdown)
        
        # Show all options
        print("\n📋 Available payment methods:")
        for idx, option in enumerate(select.options):
            option_text = option.text.strip()
            option_value = option.get_attribute('value')
            is_selected = option.is_selected()
            status = "✓ (selected)" if is_selected else ""
            print(f"  [{idx}] {option_text} (value: '{option_value}') {status}")
        
        print("\n🏦 Selecting 'Bank' option...")
        
        # Select Bank (index 1 based on your screenshot)
        success = False
        
        # Try method 1: Select by index
        try:
            select.select_by_index(1)
            print("✓ Selected Bank using index 1")
            success = True
        except Exception as e1:
            print(f"✗ Index method failed: {str(e1)}")
            
            # Try method 2: Select by visible text
            try:
                select.select_by_visible_text("Bank")
                print("✓ Selected Bank using visible text")
                success = True
            except Exception as e2:
                print(f"✗ Visible text method failed: {str(e2)}")
                
                # Try method 3: Select by value
                try:
                    select.select_by_value("bank")
                    print("✓ Selected Bank using value")
                    success = True
                except Exception as e3:
                    print(f"✗ Value method failed: {str(e3)}")
        
        if not success:
            print("❌ Failed to select Bank option")
            driver.save_screenshot("select_bank_error.png")
            raise Exception("Could not select Bank from dropdown")
        
        time.sleep(3)
        
        # Verify selection
        selected_option = select.first_selected_option.text
        print(f"✓ Currently selected: '{selected_option}'")
        
        if selected_option.strip().lower() != "bank":
            print(f"⚠️  Warning: Selected option is '{selected_option}', not 'Bank'")
        
        # ==================== STEP 4: CLICK SEND REQUEST ====================
        print("\n" + "="*60)
        print("STEP 4: CLICK SEND REQUEST BUTTON")
        print("="*60)
        
        print("🔍 Looking for 'Send Request' button...")
        
        send_button = None
        
        # Try multiple methods to find the button
        try:
            # Method 1: By exact text
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Send Request']"))
            )
            print("✓ Button found by exact text")
        except:
            try:
                # Method 2: By contains text
                send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send Request')]")
                print("✓ Button found by contains text")
            except:
                try:
                    # Method 3: By submit type
                    send_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    print("✓ Button found by submit type")
                except Exception as e:
                    print(f"❌ Could not find Send Request button: {str(e)}")
                    driver.save_screenshot("button_error.png")
                    
                    # Save page source for debugging
                    with open("page_source.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print("📄 Page source saved to page_source.html")
                    
                    raise
        
        print("✓ Clicking 'Send Request' button...")
        send_button.click()
        print("✓ Button clicked successfully")
        
        time.sleep(5)
        
        # ==================== SUCCESS ====================
        print("\n" + "="*60)
        print("✨ PAYMENT REQUEST SENT SUCCESSFULLY! ✨")
        print("="*60)
        print(f"Final URL: {driver.current_url}")
        print(f"Page Title: {driver.title}")
        
        # Take final screenshot
        driver.save_screenshot("success_screenshot.png")
        print("📸 Success screenshot saved")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR OCCURRED")
        print("="*60)
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        
        # Save error screenshot
        driver.save_screenshot("error_screenshot.png")
        print("📸 Error screenshot saved")
        
        # Save page source
        with open("error_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 Error page source saved")
        
        sys.exit(1)
        
    finally:
        driver.quit()
        print("\n🏁 Browser closed")
        print("="*60)

if __name__ == "__main__":
    steadfast_payment_request()
