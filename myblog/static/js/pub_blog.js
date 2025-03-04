window.onload = function() {
    const { createEditor, createToolbar, i18nChangeLanguage } = window.wangEditor;

    // 切換語言
    i18nChangeLanguage('zh-TW');  // 'zh-TW' 代表繁體中文

    // 編輯器設定
    const editorConfig = {
        placeholder: '請輸入內容...',
        onChange(editor) {
            const html = editor.getHtml();
            console.log('編輯器內容:', html);
        },
        // 添加圖片上傳配置
        MENU_CONF: {
            uploadImage: {
                server: '/blog/upload_image/',  // 圖片上傳接口 URL
                fieldName: 'image',        // 上傳圖片文件的字段名稱
                maxFileSize: 5 * 1024 * 1024,  // 最大文件大小 (5 MB)
                maxNumberOfFiles: 1,       // 最大上傳圖片數量
                allowedFileTypes: ['image/*'],  // 允許的文件類型
                // 自定義上傳圖片的 headers
                headers: {
                    'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()  // 添加 CSRF token
                },
                // 自定義上傳圖片參數
                meta: {
                    token: 'your-token'
                },
                onProgress: function (progress) {
                    console.log('上傳進度', progress);
                },
                onSuccess: function (file, response) {
                    console.log('上傳成功', file, response);

                    // 檢查返回的數據格式
                    if (response.data && response.data.url) {
                        const imageUrl = response.data.url;
                        console.log('圖片 URL:', imageUrl);

                        // 使用 insertImage 將圖片插入到編輯器中
                        try {
                            editor.insertImage(imageUrl);
                            console.log('圖片已插入編輯器:', imageUrl);
                        } catch (error) {
                            console.error('插入圖片時發生錯誤:', error);
                        }
                    } else {
                        console.error('上傳成功但沒有返回圖片 URL', response);
                    }
                },
                onFailed: function (file, response) {
                    console.error('上傳失敗', file, response);
                },
                onError: function (file, response) {
                    console.error('上傳錯誤', file, response);
                }
            }
        }
    };

    // 創建編輯器
    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // 或 'simple'
    });

    // 工具列設定
    const toolbarConfig = {};

    // 創建工具列
    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // 或 'simple'
    });

    $("#submit-btn").click(function(event) {
        // 阻止按鈕的默認行為
        event.preventDefault();
        console.log("提交按鈕被點擊");

        let title = $("input[name='title']").val();
        let category = $("select[name='category']").val();
        let content = editor.getHtml(); // 確保獲取編輯器內容
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax({
            url: '/blog/pub',  // 注意URL的準確性
            method: 'POST',
            data: {
                title: title,
                category: category,
                content: content,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            success: function(result) {
                if(result['code']==200){
                    // 獲取文章id
                    let blog_id = result['data']['blog_id']
                    // 發布成功跳轉到文章詳情頁
                    window.location='/blog/'+ blog_id
                }else{
                    alert(result['message']);
                }

            },
            error: function(xhr, status, error) {
                console.error("AJAX 請求失敗：", status, error);
                console.log(xhr.responseText);  // 顯示伺服器錯誤信息
            }
        });
    });
};
