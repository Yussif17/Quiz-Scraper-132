from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import tkinter as tk
import threading
from creds import QUIZ_URL, REFRESH_INTERVAL, WAIT_FOR_LOGIN_TIME

def notify_user():
    def show_popup():
        root = tk.Tk()
        root.title("QUIZ OPEN!")
        root.attributes('-fullscreen', True)
        label = tk.Label(root, text="QUIZ IS NOW OPEN!", font=("Arial", 80), fg="red")
        label.pack(expand=True)
        root.configure(bg='black')
        root.mainloop()
    
    threading.Thread(target=show_popup).start()

def monitor_quiz(driver):
    driver.get(QUIZ_URL)
    while True:
        try:
            take_quiz_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Take the Quiz')]")
            print("[+] Quiz is now OPEN!")
            notify_user()
            break
        except NoSuchElementException:
            print("[-] Quiz not open yet. Refreshing...")
            time.sleep(REFRESH_INTERVAL)
            driver.refresh()

def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Step 1: Go to Canvas login page
        driver.get("https://wustl.instructure.com")
        print(f"[*] Please log in manually using your WUSTL Key. You have {WAIT_FOR_LOGIN_TIME} seconds.")
        time.sleep(WAIT_FOR_LOGIN_TIME)

        # Step 2: Start monitoring the quiz
        monitor_quiz(driver)

    except Exception as e:
        print("[!] Error:", e)
    finally:
        print("[*] Done.")

if __name__ == "__main__":
    main()