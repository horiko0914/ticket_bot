import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# sub func
def set_selenium_options():
    options = webdriver.ChromeOptions()

    # Cookieの保存先指定
    options.add_argument(r"--user-data-dir=C:\selenium\chrome-profile")
    # ウィンドウを起動時に最大化する
    options.add_argument("--start-maximized")
    # ヘッドレスモード（画面を表示しない）
    # options.add_argument('--headless')
    # GPU（ハードウェアアクセラレーション）を無効化
    options.add_argument('--disable-gpu')
    # Web通知（Notification API）を無効化
    options.add_argument('--disable-desktop-notifications')
    # Chrome 拡張機能をすべて無効化
    options.add_argument("--disable-extensions")
    # ブラウザの言語設定を日本語にする
    options.add_argument('--lang=ja')
    # 画像の読み込みを無効化
    options.add_argument('--blink-settings=imagesEnabled=false')
    # OS や環境変数で設定されたプロキシを使わず直接接続
    options.add_argument("--proxy-server='direct://'")
    # すべてのホストでプロキシをバイパスする
    options.add_argument("--proxy-bypass-list=*")

    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-notifications")

    return options

def login(): # no_use
    login    = "horiko19960914@gmail.com"
    password = "Horiko914!"
    # driver.find_element_by_link_text("ログイン").click()
    driver.execute_script('document.getElementById("login_id").value="%s";' % login)
    driver.execute_script('document.getElementById("password").value="%s";' % password) 
    #For check box to remember
    #driver.find_element_by_name('rememberMe').click()
    driver.find_element_by_class_name('button').submit()

def wait_until(target_time_str: str):
    """
    target_time_str: 'YYYY-MM-DD HH:MM:SS'
    """
    target_time = datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S")

    while True:
        now = datetime.now()
        diff = (target_time - now).total_seconds()

        if diff <= 0:
            # 表示を消して Selenium に集中
            print("\r" + " " * 30 + "\r", end="", flush=True)
            break

        # 時刻表示（HH:MM:SS）
        print(f"\r現在時刻 {now.strftime('%H:%M:%S')}", end="", flush=True)

        if diff > 1:
            time.sleep(0.5)
        else:
            time.sleep(0.01)

def print_finish_time():
    finish_time = datetime.now().strftime("%H:%M:%S")
    print(f"完了時刻 {finish_time}")


# main func
def new_livepocket(url):
    driver.get(url)
    input("ログイン完了したら Enter を押してください")
    
    # start = time.perf_counter()

    # --- チケットを購入する ---
    driver.find_element(By.CSS_SELECTOR, "a.event-detail-ticket-button").click()

    # --- チケット枚数選択 ---
    ticket_selects = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "select.input-select__select.js-ticket-select"))
    )
    ticket_select = Select(ticket_selects[2]) # 上から3番目のチケット
    ticket_select.select_by_value("1") # 枚数を１枚を選択

    # --- 次へ進む ---
    driver.find_element(By.CSS_SELECTOR, "button.js-ticket-submit-button").click()

    # --- コンビニ決済を選択 ---
    cvs_label = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='order_form_payment_method_cvs'], #order_form_payment_method_cvs + span"))
    )
    cvs_label.click()

    # --- ファミリーマート選択 ---
    cvs_selects = wait.until(
        EC.presence_of_element_located((By.ID, "order_form_sbps_web_cvs_type"))
    )
    cvs_select = Select(cvs_selects)
    cvs_select.select_by_visible_text("ファミリーマート")

    # --- 同意チェック ---
    agree_label = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label.input-check--block"))
    )
    agree_label.click()
    # print(time.perf_counter() - start) # 2.23s

    # input("ログイン完了したら Enter を押してください")

    # --- チケット購入 ---
    # submit_button =wait.until(
    #     EC.element_to_be_clickable((By.ID, "submit-button"))
    # )
    # submit_button.click()

def ticketdive(url, target_time_str):
    # --- 発売画面に遷移 ---
    driver.get(url)

    # --- 発売時間まで待機 ---
    wait_until(target_time_str)
    driver.refresh()

    # --- チケット枚数選択 ---
    ticket_cards = driver.find_elements(By.CSS_SELECTOR, "div.TicketTypeCard_ticketTypeContainer__DP0TP")
    # 上から 0,1,2
    ticket_card_select = Select(ticket_cards[0].find_element(By.TAG_NAME, "select"))
    # 枚数を選択
    ticket_card_select.select_by_value("1")

    # --- 申し込みをするボタンを押す ---
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_rectMain___A3NV"))
    )
    button.click()

    zero_yen = True
    if zero_yen != True :
        # --- お目当てを選択 ---
        group_selects = wait.until(
            EC.presence_of_element_located((By.XPATH, "//select[option[text()='キュートアグレッションズ']]"))
        )
        group_select = Select(group_selects)
        group_select.select_by_visible_text("キュートアグレッションズ")

        # --- 決済方法を選択 ---
        konbini_label = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='コンビニ決済（前払い）']/ancestor::label"))
        )
        konbini_label.click()

        # 氏名・電話番号を入力
        last_name = wait.until(EC.presence_of_element_located((By.NAME, "lastName")))
        first_name = driver.find_element(By.NAME, "firstName")
        phone = driver.find_element(By.NAME, "phoneNumber")

        last_name.clear()
        last_name.send_keys("堀")

        first_name.clear()
        first_name.send_keys("弘二")

        phone.clear()
        phone.send_keys("08026631429")

    # --- チケット購入 ---
    complete_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='申し込みを完了する']]"))
    )
    complete_button.click()

if __name__ == "__main__":
    options = set_selenium_options()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    # url = r"https://livepocket.jp/e/0d_m0"
    # new_livepocket(url)
    
    target_time = "2026-01-04 23:52:00"
    # url = r"https://ticketdive.com/event/20260125_"
    url = r"https://ticketdive.com/event/SHIROMIZAKANA-live0105"
    ticketdive(url, target_time)
    print_finish_time()
    input()



# https://qiita.com/nkhiiiiii/items/d2d695ecdeaf7d473ffa
