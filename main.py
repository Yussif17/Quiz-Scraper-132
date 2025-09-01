from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import tkinter as tk
import threading
from creds import MAIN_URL, QUIZ_URL, REFRESH_INTERVAL, WAIT_FOR_LOGIN_TIME

def notify_user():
    def show_popup():
        root = tk.Tk()
        root.title("QUIZ OPEN!")
        root.configure(bg='black')

        # Ensure the window pops on top and fullscreen
        root.lift()
        root.attributes("-topmost", True)
        root.attributes('-fullscreen', True)

        label = tk.Label(
            root,
            text="QUIZ IS NOW OPEN!",
            font=("Arial", 80),
            fg="red",
            bg="black"
        )
        label.pack(expand=True)

        # Close on Escape or mouse click
        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<Button-1>", lambda e: root.destroy())

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
        driver.get(MAIN_URL)
        print(f"[*] Please log in manually using your WUSTL Key. You have {WAIT_FOR_LOGIN_TIME} seconds.")
        time.sleep(WAIT_FOR_LOGIN_TIME)

        # Step 2: Start monitoring the quiz
        monitor_quiz(driver)

        # Keep browser open for the quiz to be taken
        print("[*] Quiz is open. Waiting here so browser stays up.")
        while True:
            time.sleep(60)

    except Exception as e:
        print("[!] Error:", e)

if __name__ == "__main__":
    main()