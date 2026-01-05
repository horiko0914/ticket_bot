const waitForUrlChange = (prevUrl, timeout = 10000) => {
    return new Promise((resolve, reject) => {
      const start = Date.now();
      const timer = setInterval(() => {
        if (location.href !== prevUrl) {
          clearInterval(timer);
          resolve(location.href);
        }
        if (Date.now() - start > timeout) {
          clearInterval(timer);
          reject(new Error('URL change timeout'));
        }
      }, 50); // 50ms単位で監視
    });
  };


// メイン関数
(async () => {

    /* チケットを購入するボタン押す */
    const before1 = location.href;
    document.querySelector('a.event-detail-ticket-button').click();
    await waitForUrlChange(before1);
  
    /* チケット枚数を選択する */
    const ids = Array.from(document.querySelectorAll('select.input-select__select.js-ticket-select'),el => el.id);
    const ticketSelect = document.querySelector(`#${ids[2]}`);
    ticketSelect.value = "1";
    ticketSelect.dispatchEvent(new Event('change', { bubbles: true }));
  
    /* 次へ進むボタンを押す */
    const before2 = location.href;
    document.querySelector('button.js-ticket-submit-button').click();
    await waitForUrlChange(before2);
    
    /* コンビニ決済を選択 */
    document.querySelector('#order_form_payment_method_cvs').click();

    /* クレカ決済を選択 */
    // document.querySelector('#order_form_payment_method_credit').click();

    /* ファミリーマートを選択 */
    const cvsSelect = document.querySelector('#order_form_sbps_web_cvs_type');
    const option = [...cvsSelect.options].find(o => o.text === 'ファミリーマート');
    cvsSelect.value = option.value;
    cvsSelect.dispatchEvent(new Event('change', { bubbles: true }));

    /* 同意チェック */
    document.querySelector('#order_form_purchase_agreement_content').click();
  
    /* チケット購入ボタン */
    document.querySelector('#submit-button').click();
  
  })();
  