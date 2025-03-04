/*JQuery入口函數，保證html頁面加載完後再執行*/
/* JQuery入口函數，保證html頁面加載完後再執行 */
$(function(){
    // 定義綁定驗證碼按鈕點擊事件的函數
    function verify_code_click_event(){
        // 使用jQuery ID選擇器選擇獲取驗證碼的按鈕
        $verifycode = $("#verifycode") 
        // 為按鈕綁定點擊事件
        $verifycode.click(function(){
            // 使用$this儲存當前按鈕的引用
            let $this = $(this);
            // 獲取電子信箱輸入框的值
            let email = $("input[name='email']").val() 
            // 如果電子信箱為空，彈出提示信息並返回
            if(!email){
                alert('請先輸入電子信箱');
                return
            }
            // 如果已有信箱，則取消按鈕的點擊事件，防止多次點擊,並進入倒計時
            $this.off('click')

            // 發送ajax請求(發送驗證email)
            $.ajax({
                url: 'code?email=' + encodeURIComponent(email), // 编码 email
                method: 'GET',
                success: function(result) {
                    if(result['code']==200){
                        alert('驗證信已經發送到您的電子信箱')
                    }else{
                        alert(result['result']);
                    }
                },
                error: function(xhr, status, error) {  // 使用 error 而非 fail
                    console.error('Error:', error);
                }
            });
            

            // 設置倒數計時的初始值
            let counter = 60*5
            // 開始倒數計時
            let timer = setInterval(function(){
                // 如果倒數結束，將按鈕文字設置為“獲取驗證碼”
                if(counter <= 0){
                    $this.text('獲取驗證碼')
                    // 倒數結束後，清除計時器以避免異常
                    clearInterval(timer)
                    // 重新綁定點擊事件，恢復按鈕的功能
                    verify_code_click_event()
                }
                else{ 
                    // 如果倒數計時大於0，按鈕文字顯示剩餘秒數
                    counter--;
                    $verifycode.text(counter + "秒")
                }
            }, 1000) // 每秒執行一次
        })
    }
    // 調用綁定點擊事件的函數
    verify_code_click_event()
});

/*
使用 $(function() {...}) 保證在HTML頁面加載完畢後再執行代碼。

定義 verify_code_click_event 函數，並綁定點擊事件到ID為 verifycode 的按鈕。

當按鈕被點擊時：

檢查電子信箱輸入框是否為空。如果是空的，則顯示提示信息，要求用戶先輸入電子信箱。

禁用按鈕的點擊事件以防止多次點擊。

開始一個從10秒倒數的計時器，在此期間按鈕會顯示剩餘秒數。

一旦倒數結束，按鈕文字變回“獲取驗證碼”，並重新綁定點擊事件。

*/
