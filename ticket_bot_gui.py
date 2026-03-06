import threading
import socket
import struct
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time
from pathlib import Path

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

CARD_SEC_NUM = "345"

# ==================================================
# グローバル
# ==================================================
selenium_started = False
driver_global = None
# NICT 時刻との差分（秒）
time_offset = 0.0

# ==================================================
# Selenium 設定
# ==================================================
def set_selenium_options():
    options = webdriver.ChromeOptions()
    profile_dir = Path.cwd() / "Cookie"
    # profile_dir = Path.cwd() / "Cookie_another_accaunt"
    profile_dir.mkdir(parents=True, exist_ok=True)
    options.add_argument(f"--user-data-dir={str(profile_dir)}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--lang=ja")
    # options.add_argument("--blink-settings=imagesEnabled=false")
    # options.add_argument("--headless")
    return options

# ==================================================
# LivePocket
# ==================================================
def livepocket_new(driver, wait, ticket_index, ticket_count, payment, test_mode):
    # --- チケットを購入する ボタンをクリック ---
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.event-detail-ticket-button"))
    ).click()

    # --- チケット枚数選択 ---
    selects = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "select.input-select__select.js-ticket-select"))
    )
    # 上から{ticket_index}番目のチケットを{ticket_count}枚選択
    Select(selects[ticket_index - 1]).select_by_value(str(ticket_count))
    
    # --- 次へ進む ボタンをクリック ---
    driver.find_element(
        By.CSS_SELECTOR, "button.js-ticket-submit-button"
    ).click()

    # --- 支払い方法選択 ---
    if payment == "cvs": # コンビニ決済
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[.//span[normalize-space()='コンビニ決済']]")
        )).click()
        
        #ファミリーマートを選択
        cvs_selects = wait.until(
            EC.presence_of_element_located((By.ID, "order_form_sbps_web_cvs_type"))
        )
        cvs_select = Select(cvs_selects)
        cvs_select.select_by_visible_text("ファミリーマート")
    
    else: # クレジットカード決済
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[.//span[normalize-space()='クレジットカード決済']]")
        )).click()
        # カード番号等の入力はログイン情報から自動入力されるはずなので不要
        # カード番号入力も不要

    # --- 同意チェック ---
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "label.input-check--block"))
    ).click()
    
    # --- チケット購入 ボタンをクリック　---
    if not test_mode:
        wait.until(EC.element_to_be_clickable(
            (By.ID, "submit-button"))
        ).click()

# ==================================================
# TicketDive
# ==================================================
def ticketdive(driver, wait, ticket_index, ticket_count, payment, last, first, phone, test_mode):
    # time.sleep(0.5)
    # チケットカード出現待ち
    # select出現待ち
    # wait.until(
    #     EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, "select.TicketTypeCard_numberSelector__UcNLO")
    #     )
    # )
    # --- チケット枚数選択 ---
    cards = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.TicketTypeCard_ticketTypeContainer__DP0TP")
    ))

    # 上から{ticket_index}番目のチケットを{ticket_count}枚選択
    target_select = cards[ticket_index - 1].find_element(By.TAG_NAME, "select")
    Select(target_select).select_by_value(str(ticket_count))


    # --- 申し込みをする ボタンをクリック ---
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.Button_rectMain___A3NV"))
    ).click()

    # --- お目当てを選択 ---
    select_elem = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//span[contains(normalize-space(), 'お目当てのグループ')]"
            "/ancestor::div[1]//select"
        ))
    )
    select = Select(select_elem)
    select.select_by_index(1)
    # select.select_by_visible_text("キュートアグレッションズ")
    # select.select_by_visible_text("Twilight BlooM.")
    # select.select_by_visible_text("Aim")
    # --- 決済方法を選択 ---
    if payment == "cvs": # コンビニ決済
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='コンビニ決済（前払い）']/ancestor::label"))
        ).click()

        # 氏名・電話番号を入力
        driver.find_element(By.NAME, "lastName").send_keys(last)
        driver.find_element(By.NAME, "firstName").send_keys(first)
        driver.find_element(By.NAME, "phoneNumber").send_keys(phone)

    else: # クレジットカード決済
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='クレジットカード']/ancestor::label"))
        ).click()

        # 表示テキスト「セキュリティコード」を起点に親要素を取得
        label_elem = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[normalize-space(text())='セキュリティコード']")
            )
        )
        # その直後のiframeを取得
        cvc_iframe = label_elem.find_element(By.XPATH, "following::iframe[1]")
        # iframeに切り替え
        driver.switch_to.frame(cvc_iframe)
        # iframe内inputを取得
        cvc_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input")))
        # 入力
        cvc_input.clear()
        cvc_input.send_keys(CARD_SEC_NUM)
        # 親フレームへ戻る
        driver.switch_to.default_content()

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

# NICT / NTP 時刻取得
def get_nict_time(server="ntp.nict.jp", timeout=5):
    """NICT の NTP サーバから現在時刻を取得して datetime を返す。"""
    try:
        addr = (server, 123)
        # NTP ヘッダー: LI=0, VN=3, Mode=3 (client)
        msg = b"\x1b" + 47 * b"\0"
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.sendto(msg, addr)
            data, _ = s.recvfrom(48)

        if len(data) < 48:
            return None

        unpacked = struct.unpack("!12I", data)
        transmit_timestamp = unpacked[10] + float(unpacked[11]) / 2**32
        # NTP epoch は 1900-01-01
        NTP_DELTA = 2208988800
        unix_time = transmit_timestamp - NTP_DELTA
        return datetime.fromtimestamp(unix_time)
    except Exception:
        return None


def sync_time_with_nict(label_var=None):
    """NICT 時刻と同期し、差分を time_offset に設定する。"""
    global time_offset
    nict_dt = get_nict_time()
    if nict_dt is None:
        if label_var:
            label_var.set("NICT時刻取得失敗")
        return False

    local_dt = datetime.now()
    time_offset = (nict_dt - local_dt).total_seconds()
    if label_var:
        label_var.set(
            f"NICT時刻: {nict_dt.strftime('%Y-%m-%d %H:%M:%S')} (差 {time_offset:+.3f}s)"
        )
    return True

# ==================================================
# Selenium 実行
# ==================================================
def selenium_runner():
    global selenium_started, driver_global

    try:
        target_dt = get_target_datetime()

        driver_global = webdriver.Chrome(options=set_selenium_options())
        driver = driver_global
        wait = WebDriverWait(driver, 10)

        driver.get(url_var.get())

        while datetime.fromtimestamp(time.time() + time_offset) < target_dt:
            if driver.service.process.poll() is not None:
                raise RuntimeError("ブラウザが閉じられました")
            time.sleep(0.05)
        print("処理開始:" + datetime.fromtimestamp(time.time() + time_offset).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
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
                int(ticket_index_var.get()),
                int(ticket_count_var.get()),
                payment_var.get(),
                last_name_var.get(),
                first_name_var.get(),
                phone_var.get(),
                test_mode_var.get()
            )

        print("処理完了:" + datetime.fromtimestamp(time.time() + time_offset).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("エラー", str(e)))

    finally:
        selenium_started = False
        root.after(0, lambda: start_btn.config(state="normal"))


def close_browser():
    global driver_global
    if driver_global:
        try:
            driver_global.quit()
        except:
            pass
        driver_global = None



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
    nict_now = datetime.fromtimestamp(time.time() + time_offset)
    diff = (nict_now - datetime.now()).total_seconds()
    nict_label_var.set(
        f"NICT時刻：{nict_now.strftime('%Y-%m-%d %H:%M:%S')} (差 {diff:+.3f}s)"
    )
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
test_mode_var = tk.BooleanVar(value=False)

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

nict_label_var = tk.StringVar()

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

# チケット番号 / 枚数
ttk.Label(root, text="チケット番号").grid(row=4, column=0)
ttk.Entry(root, textvariable=ticket_index_var, width=4,
          style="Enabled.TEntry").grid(row=4, column=1)

ttk.Label(root, text="枚数").grid(row=4, column=2)
ttk.Entry(root, textvariable=ticket_count_var, width=4,
          style="Enabled.TEntry").grid(row=4, column=3)

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

# NICT同期時刻
ttk.Label(root, textvariable=nict_label_var,
          font=("Meiryo", 11, "bold")).grid(row=7, column=0,
                                           columnspan=6, sticky="w")

# 開始
start_btn = ttk.Button(root, text="開始", command=on_start)
start_btn.grid(row=9, column=0, pady=10)

close_btn = ttk.Button(root, text="ブラウザ終了", command=close_browser)
close_btn.grid(row=9, column=1, pady=10)


update_td_state()
# 起動時に NICT 時刻と同期
sync_time_with_nict(nict_label_var)
update_now()
root.mainloop()
