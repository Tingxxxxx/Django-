window.onload = function() {
    const { createEditor, createToolbar, i18nChangeLanguage } = window.wangEditor;

    // 切換語言為繁體中文
    i18nChangeLanguage('zh-cn');  // 'zh-TW' 代表繁體中文

    // 編輯器設定
    const editorConfig = {
        placeholder: '請輸入內容...',
        onChange(editor) {
            const html = editor.getHtml();
            console.log('編輯器內容:', html);
        },
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
};