import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# ==================================================
# 定数
# ==================================================
TD_DISABLED_TEXT = "不要"
TD_DEFAULT_LAST = "堀"
TD_DEFAULT_FIRST = "弘二"
TD_DEFAULT_PHONE = "08026631429"

# ==================================================
# グローバル
# ==================================================
selenium_started = False

# ==================================================
# Selenium 設定
# ==================================================
def set_selenium_options():
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=C:\selenium\chrome-profile")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--lang=ja")
    options.add_argument("--blink-settings=imagesEnabled=false")
    return options

# ==================================================
# LivePocket
# ==================================================
def livepocket_new(driver, wait, ticket_index, ticket_count, payment, test_mode):
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.event-detail-ticket-button"))
    ).click()

    selects = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "select.input-select__select.js-ticket-select"))
    )
    Select(selects[ticket_index - 1]).select_by_value(str(ticket_count))

    driver.find_element(
        By.CSS_SELECTOR, "button.js-ticket-submit-button"
    ).click()

    if payment == "cvs":
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[.//span[normalize-space()='コンビニ決済']]")
        )).click()
    else:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[.//span[normalize-space()='クレジットカード決済']]")
        )).click()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "label.input-check--block"))
    ).click()

    if not test_mode:
        wait.until(EC.element_to_be_clickable(
            (By.ID, "submit-button"))
        ).click()

# ==================================================
# TicketDive
# ==================================================
def ticketdive(driver, wait, payment, last, first, phone, test_mode):
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.Button_rectMain___A3NV"))
    ).click()

    if payment == "cvs":
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='コンビニ決済（前払い）']/ancestor::label"))
        ).click()

        driver.find_element(By.NAME, "lastName").send_keys(last)
        driver.find_element(By.NAME, "firstName").send_keys(first)
        driver.find_element(By.NAME, "phoneNumber").send_keys(phone)

    else:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='クレジットカード']/ancestor::label"))
        ).click()

    if not test_mode:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='申し込みを完了する']]"))
        ).click()

# ==================================================
# 日時
# ==================================================
def get_target_datetime():
    return datetime(
        int(year_var.get()),
        int(month_var.get()),
        int(day_var.get()),
        int(hour_var.get()),
        int(minute_var.get()),
        int(second_var.get())
    )

# ==================================================
# Selenium 実行
# ==================================================
def selenium_runner():
    global selenium_started
    driver = None

    try:
        target_dt = get_target_datetime()

        driver = webdriver.Chrome(options=set_selenium_options())
        wait = WebDriverWait(driver, 10)

        driver.get(url_var.get())

        while datetime.now() < target_dt:
            if driver.service.process.poll() is not None:
                raise RuntimeError("ブラウザが閉じられました")
            time.sleep(0.05)

        driver.refresh()

        if site_var.get() == "livepocket":
            livepocket_new(
                driver, wait,
                int(ticket_index_var.get()),
                int(ticket_count_var.get()),
                payment_var.get(),
                test_mode_var.get()
            )
        else:
            ticketdive(
                driver, wait,
                payment_var.get(),
                last_name_var.get(),
                first_name_var.get(),
                phone_var.get(),
                test_mode_var.get()
            )

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("エラー", str(e)))

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        selenium_started = False
        root.after(0, lambda: start_btn.config(state="normal"))

# ==================================================
# GUI制御
# ==================================================
def update_td_state(*_):
    is_td_cvs = site_var.get() == "ticketdive" and payment_var.get() == "cvs"

    if is_td_cvs:
        last_name_var.set(TD_DEFAULT_LAST)
        first_name_var.set(TD_DEFAULT_FIRST)
        phone_var.set(TD_DEFAULT_PHONE)
        style_name = "Enabled.TEntry"
        state = "normal"
    else:
        last_name_var.set(TD_DISABLED_TEXT)
        first_name_var.set(TD_DISABLED_TEXT)
        phone_var.set(TD_DISABLED_TEXT)
        style_name = "Disabled.TEntry"
        state = "disabled"

    for _, ent in td_entries:
        ent.config(state=state, style=style_name)

def on_start():
    global selenium_started
    if selenium_started:
        return
    selenium_started = True
    start_btn.config(state="disabled")
    threading.Thread(target=selenium_runner, daemon=True).start()

def update_now():
    now_label_var.set(datetime.now().strftime("現在時刻：%Y-%m-%d %H:%M:%S"))
    root.after(500, update_now)

# ==================================================
# GUI
# ==================================================
root = tk.Tk()
root.title("チケット自動購入")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")

style.configure(".", background="#1e1e1e", foreground="#ffffff")
style.configure("Enabled.TEntry", fieldbackground="#ffffff", foreground="#000000")
style.configure("Disabled.TEntry", fieldbackground="#444444", foreground="#aaaaaa")

now = datetime.now()

url_var = tk.StringVar()
site_var = tk.StringVar(value="livepocket")
payment_var = tk.StringVar(value="cvs")
test_mode_var = tk.BooleanVar(value=True)

ticket_index_var = tk.StringVar(value="1")
ticket_count_var = tk.StringVar(value="1")

last_name_var = tk.StringVar()
first_name_var = tk.StringVar()
phone_var = tk.StringVar()

year_var = tk.StringVar(value=now.year)
month_var = tk.StringVar(value=now.month)
day_var = tk.StringVar(value=now.day)
hour_var = tk.StringVar(value=now.hour)
minute_var = tk.StringVar(value="00")
second_var = tk.StringVar(value="00")

now_label_var = tk.StringVar()

# URL
ttk.Label(root, text="URL").grid(row=0, column=0, sticky="w")
ttk.Entry(root, textvariable=url_var, width=60,
          style="Enabled.TEntry").grid(row=0, column=1, columnspan=6)

# 日時
labels = ["年", "月", "日", "時", "分", "秒"]
vars_ = [year_var, month_var, day_var, hour_var, minute_var, second_var]

for i, t in enumerate(labels):
    ttk.Label(root, text=t).grid(row=1, column=i)
for i, v in enumerate(vars_):
    ttk.Entry(root, textvariable=v, width=4,
              style="Enabled.TEntry").grid(row=2, column=i)

# サイト
ttk.Radiobutton(root, text="LivePocket",
                variable=site_var, value="livepocket",
                command=update_td_state).grid(row=3, column=0)
ttk.Radiobutton(root, text="TicketDive",
                variable=site_var, value="ticketdive",
                command=update_td_state).grid(row=3, column=1)

# 決済
ttk.Radiobutton(root, text="コンビニ",
                variable=payment_var, value="cvs",
                command=update_td_state).grid(row=3, column=2)
ttk.Radiobutton(root, text="クレカ",
                variable=payment_var, value="card",
                command=update_td_state).grid(row=3, column=3)

# TicketDive
ttk.Label(root, text="姓").grid(row=5, column=0)
e1 = ttk.Entry(root, textvariable=last_name_var, width=10)
e1.grid(row=5, column=1)

ttk.Label(root, text="名").grid(row=5, column=2)
e2 = ttk.Entry(root, textvariable=first_name_var, width=10)
e2.grid(row=5, column=3)

ttk.Label(root, text="電話").grid(row=5, column=4)
e3 = ttk.Entry(root, textvariable=phone_var, width=18)
e3.grid(row=5, column=5)

td_entries = [(last_name_var, e1), (first_name_var, e2), (phone_var, e3)]

# テスト
ttk.Checkbutton(root, text="✓ テストモード（購入しない）",
                variable=test_mode_var).grid(row=6, column=0, columnspan=3)

# 現在時刻
ttk.Label(root, textvariable=now_label_var,
          font=("Meiryo", 11, "bold")).grid(row=7, column=0,
                                           columnspan=6, sticky="w")

# 開始
start_btn = ttk.Button(root, text="開始", command=on_start)
start_btn.grid(row=8, column=0, pady=10)

update_td_state()
update_now()
root.mainloop()
