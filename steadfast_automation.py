from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def steadfast_payment_request():
    # Chrome options for headless mode (GitHub Actions এ চলার জন্য)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("🚀 Starting automation...")
        
        # Step 1: Login page এ যান
        print("📍 Going to login page...")
        driver.get("https://steadfast.com.bd/login")
        time.sleep(3)
        
        # Step 2: Login করুন
        print("🔐 Logging in...")
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_field = driver.find_element(By.NAME, "password")
        
        email_field.send_keys("mojakkeralam16@gmail.com")
        password_field.send_keys("Libas@12")
        
        # Login button click
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(5)
        
        # Step 3: Payment Request page এ যান
        print("💰 Going to payment request page...")
        driver.get("https://steadfast.com.bd/user/payment-request")
        time.sleep(3)
        
        # Step 4: Dropdown থেকে "Bank" select করুন
        print("🏦 Selecting Bank option...")
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "payment_method"))
        )
        dropdown.click()
        time.sleep(1)
        
        # "Bank" option select করুন
        bank_option = driver.find_element(By.XPATH, "//option[contains(text(), 'Bank')]")
        bank_option.click()
        time.sleep(2)
        
        # Step 5: Send Request button এ click করুন
        print("✅ Clicking Send Request button...")
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send Request')]"))
        )
        send_button.click()
        time.sleep(3)
        
        print("✨ Payment request sent successfully!")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        driver.save_screenshot("error_screenshot.png")
        raise
        
    finally:
        driver.quit()
        print("🏁 Automation completed!")

if __name__ == "__main__":
    steadfast_payment_request()
