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
    # バックグラウンドでのネットワーク通信（自動更新・事前接続など）を無効化し、不要な通信を抑制
    options.add_argument("--disable-background-networking")
    # Chrome プロファイルの同期（Google アカウント同期）を無効化し、外部依存と副作用を回避
    options.add_argument("--disable-sync")
    # ブラウザ通知（Web Push / 権限要求ポップアップ）を無効化し、自動操作の安定性を向上
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

def print_time():
    now_time = datetime.now().strftime("%H:%M:%S")
    print(f"現在時刻 {now_time}")


# main func
def livepocket_new(url, target_time_str):
    # --- 発売画面に遷移 ---
    driver.get(url)
    
    # --- 発売時間まで待機 ---
    wait_until(target_time_str)
    driver.refresh()

    # --- iframe（AI Chat Support ウィジェット）を強制的に無効化 ---
    driver.execute_script("""
        const iframe = document.querySelector('iframe.ul-widget-main-window');
        if (iframe) {iframe.remove();}
    """)
    # --- チケットを購入する ボタンをクリック ---
    driver.find_element(By.CSS_SELECTOR, "a.event-detail-ticket-button").click()

    # --- チケット枚数選択 ---
    ticket_selects = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "select.input-select__select.js-ticket-select"))
    )
    ticket_select = Select(ticket_selects[0]) # 上から1番目のチケット
    ticket_select.select_by_value("1") # 枚数を１枚を選択

    # --- 次へ進む ボタンをクリック ---
    driver.find_element(By.CSS_SELECTOR, "button.js-ticket-submit-button").click()

    # --- コンビニ決済を選択 ---
    IS_COMBI = True
    if IS_COMBI:
        cvs_label = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[.//span[normalize-space()='コンビニ決済']]"
            ))
        )
        cvs_label.click()
        # --- ファミリーマート選択 ---
        cvs_selects = wait.until(
            EC.presence_of_element_located((By.ID, "order_form_sbps_web_cvs_type"))
        )
        cvs_select = Select(cvs_selects)
        cvs_select.select_by_visible_text("ファミリーマート")

    else: # IS_COMBI ==False
        cvs_label = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[.//span[text()='クレジットカード決済']]"
            ))
        )
        cvs_label.click()
    
    # --- 同意チェック ---
    agree_label = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label.input-check--block"))
    )
    agree_label.click()

    # --- チケット購入 ボタンをクリック　---
    submit_button =wait.until(
        EC.element_to_be_clickable((By.ID, "submit-button"))
    )
    submit_button.click()

def ticketdive(url, target_time_str):
    zero_yen = False # 当日払いの場合はtrue
    # --- 発売画面に遷移 ---
    driver.get(url)

    # --- 発売時間まで待機 ---
    wait_until(target_time_str)
    driver.refresh()

    # --- チケット枚数選択 ---
    # ticket_cards = driver.find_elements(By.CSS_SELECTOR, "div.TicketTypeCard_ticketTypeContainer__DP0TP")
    # ticket_card_select = Select(ticket_cards[0].find_element(By.TAG_NAME, "select")) # 上から1番目のチケット
    # ticket_card_select.select_by_value("1") # 枚数を1枚を選択

    # --- 申し込みをする ボタンをクリック ---
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_rectMain___A3NV"))
    )
    button.click()

    if zero_yen != True :
        # --- お目当てを選択 ---
        group_selects = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.FlexBox_flex__q0PvO select.Select_select__Wa03B"))
        )
        group_select = Select(group_selects)
        # group_select.select_by_visible_text("キュートアグレッションズ")
        group_select.select_by_visible_text("Twilight BlooM.")
        # group_select.select_by_visible_text("Aim")
        # TODO 一番上を選択

        # --- 決済方法を選択 ---
        konbini_label = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='コンビニ決済（前払い）']/ancestor::label"))
        )
        konbini_label.click()

        # 氏名・電話番号を入力
        # last_name = wait.until(EC.presence_of_element_located((By.NAME, "lastName")))
        last_name = wait.until(EC.visibility_of_element_located((By.NAME, "lastName")))
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

def tiget(url, target_time_str):
    # --- 発売画面に遷移 ---
    driver.get(url)
    
    # --- 発売時間まで待機 ---
    wait_until(target_time_str)
    driver.refresh()

def livepocket_old(url, target_time_str):
    # --- 発売画面に遷移 ---
    driver.get(url)
    
    # --- 発売時間まで待機 ---
    wait_until(target_time_str)
    driver.refresh()


if __name__ == "__main__":
    options = set_selenium_options()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    # url = r"https://livepocket.jp/e/0d_m0"
    # url = r"https://tiget.net/events/451871"
    # url = r"https://t.livepocket.jp/e/terasusekai_vol_04"
    
    url = r"https://livepocket.jp/e/g_assort4"

    target_time = "2026-01-31 22:30:00"

    print_time()
    livepocket_new(url, target_time)
    # ticketdive(url, target_time)
    # tiget(url, target_time)
    # livepocket_old(url, target_time)
    print_time()



# https://qiita.com/nkhiiiiii/items/d2d695ecdeaf7d473ffa
