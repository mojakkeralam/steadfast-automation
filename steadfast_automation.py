from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time
import sys
import os
import shutil

# Website configurations
WEBSITES = [
    {
        'name': 'Steadfast',
        'login_url': 'https://steadfast.com.bd/login',
        'payment_url': 'https://steadfast.com.bd/user/payment-request',
        'domain': '.steadfast.com.bd'
    },
    {
        'name': 'Packzy',
        'login_url': 'https://merchant.packzy.com/login',
        'payment_url': 'https://merchant.packzy.com/user/payment-request',
        'domain': '.packzy.com'
    }
]


def process_payment_page(driver, site_name):
    """Process payment request on the payment page"""
    
    print(f"\n{'='*60}")
    print(f"SELECT BANK & SUBMIT REQUEST ({site_name})")
    print(f"{'='*60}")
    
    print("🔍 Looking for payment method dropdown...")
    time.sleep(5)
    
    # Try to find dropdown
    dropdown = None
    try:
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "paymentMethod"))
        )
        print("✓ Dropdown found")
    except:
        try:
            dropdown = driver.find_element(By.CSS_SELECTOR, "select.form-control")
            print("✓ Dropdown found")
        except:
            try:
                dropdown = driver.find_element(By.TAG_NAME, "select")
                print("✓ Dropdown found")
            except Exception as e:
                print(f"❌ Could not find dropdown: {str(e)}")
                driver.save_screenshot(f"{site_name.lower()}_no_dropdown.png")
                return False
    
    # Create Select object
    select = Select(dropdown)
    
    # Show options
    print("\n📋 Available payment methods:")
    for idx, option in enumerate(select.options):
        print(f"  [{idx}] {option.text} (value={option.get_attribute('value')})")
    
    # Select Bank
    print("\n🏦 Selecting 'Bank' option...")
    try:
        select.select_by_value("1")
        time.sleep(2)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", dropdown)
        time.sleep(2)
        print("✓ Bank selected")
    except:
        try:
            select.select_by_visible_text("Bank")
            time.sleep(2)
            print("✓ Bank selected")
        except Exception as e:
            print(f"❌ Could not select Bank: {str(e)}")
            return False
    
    # Click Send Request button
    print("\n✅ Clicking 'Send Request' button...")
    try:
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send Request')]"))
        )
        send_button.click()
        time.sleep(5)
        print("✓ Request submitted!")
        return True
    except Exception as e:
        print(f"❌ Could not submit: {str(e)}")
        return False


def try_login_and_payment(driver, site_config, email, password):
    """Try to login and submit payment request"""
    
    site_name = site_config['name']
    login_url = site_config['login_url']
    payment_url = site_config['payment_url']
    
    print(f"\n{'='*60}")
    print(f"🌐 TRYING SITE: {site_name}")
    print(f"{'='*60}")
    
    try:
        # Login
        print(f"\n📍 Navigating to {site_name} login page...")
        driver.get(login_url)
        time.sleep(5)
        
        print(f"🔐 Entering credentials...")
        
        email_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_field = driver.find_element(By.NAME, "password")
        
        email_field.clear()
        email_field.send_keys(email)
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(1)
        
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        print("✓ Login button clicked")
        
        time.sleep(10)
        
        # Check login success
        if 'login' in driver.current_url.lower():
            print(f"⚠️  Login failed on {site_name}")
            return False
        
        print(f"✅ Login successful on {site_name}!")
        
        # Go to payment page
        print(f"\n💰 Going to payment request page...")
        driver.get(payment_url)
        time.sleep(5)
        
        if 'payment-request' not in driver.current_url:
            print(f"⚠️  Could not reach payment page on {site_name}")
            return False
        
        # Process payment
        result = process_payment_page(driver, site_name)
        
        if result:
            print(f"\n✨ PAYMENT REQUEST SENT SUCCESSFULLY ON {site_name}! ✨")
            driver.save_screenshot(f"{site_name.lower()}_success.png")
            return True
        else:
            return False
        
    except Exception as e:
        print(f"\n❌ Error on {site_name}: {str(e)}")
        driver.save_screenshot(f"{site_name.lower()}_error.png")
        return False


def payment_automation():
    print("=" * 60)
    print("🚀 Payment Request Automation Starting...")
    print("=" * 60)
    
    # Get credentials
    email = os.environ.get('STEADFAST_EMAIL')
    password = os.environ.get('STEADFAST_PASSWORD')
    cookies_string = os.environ.get('STEADFAST_COOKIES')
    
    if not email or not password:
        print("❌ ERROR: Credentials not found!")
        sys.exit(1)
    
    print(f"✓ Credentials loaded")
    print(f"✓ Email: {email[:3]}***@{email.split('@')[1]}")
    
    # Check cookies
    use_cookies = bool(cookies_string)
    if use_cookies:
        print("✓ Cookies found - will use cookie authentication!")
        print("✅ This will bypass CAPTCHA and skip login!")
    else:
        print("⚠️  No cookies found - will use regular login")
    
    # Chrome setup
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Find ChromeDriver
    chromedriver_path = shutil.which('chromedriver')
    if not chromedriver_path:
        chromedriver_paths = ['/usr/bin/chromedriver', '/usr/lib/chromium-browser/chromedriver']
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
            driver = webdriver.Chrome(options=chrome_options)
        print("✓ ChromeDriver initialized")
    except Exception as e:
        print(f"❌ Failed to initialize ChromeDriver: {str(e)}")
        sys.exit(1)
    
    try:
        print(f"\n📌 Chrome: {driver.capabilities['browserVersion']}")
        
        success = False
        
        # ========== COOKIE-BASED AUTHENTICATION ==========
        if use_cookies:
            print("\n" + "="*60)
            print("🍪 COOKIE AUTHENTICATION MODE")
            print("="*60)
            
            # Navigate to domain first
            print("📍 Navigating to Steadfast...")
            driver.get("https://steadfast.com.bd")
            time.sleep(3)
            
            # Add cookies
            print("🍪 Loading saved cookies...")
            cookies_added = 0
            cookie_pairs = cookies_string.split('; ')
            
            for cookie_pair in cookie_pairs:
                if '=' in cookie_pair:
                    try:
                        name, value = cookie_pair.split('=', 1)
                        driver.add_cookie({
                            'name': name.strip(),
                            'value': value.strip(),
                            'domain': '.steadfast.com.bd',
                            'path': '/',
                        })
                        cookies_added += 1
                    except:
                        continue
            
            print(f"✓ Loaded {cookies_added} cookies")
            
            # Try to access payment page
            print("\n💰 Accessing payment page with cookies...")
            driver.get("https://steadfast.com.bd/user/payment-request")
            time.sleep(5)
            
            current_url = driver.current_url
            print(f"✓ Current URL: {current_url}")
            
            # Check if logged in
            if 'login' in current_url.lower():
                print("⚠️  Cookies expired or invalid!")
                print("⚠️  Falling back to regular login...")
                use_cookies = False
            elif 'payment-request' in current_url:
                print("✅ Cookie authentication successful!")
                print("✅ Bypassed login & CAPTCHA!")
                
                # Process payment
                result = process_payment_page(driver, "Steadfast")
                if result:
                    success = True
                    print("\n🎉 SUCCESS via Cookie Authentication!")
            else:
                print("⚠️  Unexpected page, falling back to login...")
                use_cookies = False
        
        # ========== REGULAR LOGIN FLOW ==========
        if not use_cookies and not success:
            print("\n" + "="*60)
            print("🔐 REGULAR LOGIN MODE")
            print("="*60)
            
            # Try Steadfast first
            result = try_login_and_payment(driver, WEBSITES[0], email, password)
            if result:
                success = True
                print("\n🎉 SUCCESS via Steadfast!")
            else:
                # Try Packzy as fallback
                print("\n⚠️  Steadfast failed, trying Packzy...")
                result = try_login_and_payment(driver, WEBSITES[1], email, password)
                if result:
                    success = True
                    print("\n🎉 SUCCESS via Packzy!")
        
        if not success:
            print("\n" + "="*60)
            print("❌ ALL METHODS FAILED")
            print("="*60)
            sys.exit(1)
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ CRITICAL ERROR")
        print("="*60)
        print(f"Error: {str(e)}")
        driver.save_screenshot("critical_error.png")
        sys.exit(1)
        
    finally:
        driver.quit()
        print("\n🏁 Browser closed")
        print("="*60)

if __name__ == "__main__":
    payment_automation()
