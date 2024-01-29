from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass

INSTANCE_URL = "https://url goes here.atlassian.net/" #REPLACE WITH YOUR ATLASSIAN CLOUD URL
PORTAL_ONLY_CUSTOMER_URL = "https://admin.atlassian.com/s/instance id goes here/jira-service-management/portal-only-customers" #REPLACE WITH YOUR PORTAL ONLY URL

if __name__ == "__main__":
    email_id = input("Email ID : ")
    pw = getpass.getpass("Password : ")

    if email_id != '' and pw != '':
        try:
            options = webdriver.ChromeOptions()
            #options.add_argument("--headless=new") #Remove the comment for headless
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(e)
            exit()

        print("Logging in...")
        driver.get(INSTANCE_URL)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID,'username')))
        driver.find_element(By.ID,'username').send_keys(email_id)
        driver.find_element(By.ID,'login-submit').click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID,'password')))
        driver.find_element(By.ID,'password').send_keys(pw)
        driver.find_element(By.ID,'login-submit').click()
        time.sleep(2)
        driver.get(PORTAL_ONLY_CUSTOMER_URL)
        time.sleep(10)
        print("Deactivating...")
        while True:
            time.sleep(5)
            overflows = driver.find_elements(By.XPATH,'//button[@class="css-9snh2d"]')
            for overflow in overflows:
                overflow.click()
                time.sleep(2)
                selections = driver.find_elements(By.XPATH,'//button[@class="css-homugq"]')
                decision = selections[2].find_element(By.XPATH, './/span[@data-item-title="true"]').text.strip()
                if decision == "Revoke access":
                    selections[2].click()
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//button[@class="css-1yeatxf"]')))
                    driver.find_element(By.XPATH, '//button[@class="css-1yeatxf"]').click()
                    time.sleep(2)
                else:
                    overflow.click()
                    pass

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//button[@aria-label="Next"]')))
            button = driver.find_element(By.XPATH,'//button[@aria-label="Next"]')
            tabindex = button.get_attribute('tabindex')
            if tabindex == '0':
                button.click()
            elif tabindex == '-1':
                break
        print('Deactivated.')
        driver.quit()
        exit()
    else:
        exit()