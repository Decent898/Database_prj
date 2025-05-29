/**
 * 博客文章编辑器脚本
 */
document.addEventListener('DOMContentLoaded', function() {
    // 获取content textarea元素
    const contentTextarea = document.getElementById('id_content');
    
    // 移除required属性，使用JavaScript验证代替
    if (contentTextarea) {
        contentTextarea.removeAttribute('required');
    }
    
    // 初始化编辑器
    var easyMDE = new EasyMDE({
        element: contentTextarea,
        autosave: {
            enabled: true,
            uniqueId: 'post_content_editor',
            delay: 1000,
        },
        spellChecker: false,
        toolbar: [
            "bold", "italic", "heading", "|", 
            "quote", "code", "unordered-list", "ordered-list", "|",
            "link", "image", "table", "horizontal-rule", "|",
            "preview", "side-by-side", "fullscreen", "|",
            "guide"
        ],
        placeholder: "在此处开始撰写您的精彩内容...",
        status: ["autosave", "words", "lines"],
        renderingConfig: {
            codeSyntaxHighlighting: true,
            singleLineBreaks: false,
        },
        previewRender: function(plainText) {
            let preview = this.parent.markdown(plainText);
            setTimeout(function() {
                renderMathInElement(document.getElementsByClassName('editor-preview-side')[0], {
                    delimiters: [
                        {left: '$$', right: '$$', display: true},
                        {left: '$', right: '$', display: false},
                        {left: '\\(', right: '\\)', display: false},
                        {left: '\\[', right: '\\]', display: true}
                    ],
                    throwOnError: false,
                    trust: true
                });
            }, 100);
            return preview;
        }
    });
    
    // 标签页切换功能
    const tabNavItems = document.querySelectorAll('.tab-nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabNavItems.forEach(item => {
        item.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            
            // 更新标签页状态
            tabNavItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // 更新内容区域状态
            tabContents.forEach(c => c.classList.add('d-none'));
            document.getElementById(target).classList.remove('d-none');
            
            // 如果是预览标签页，更新预览内容
            if (target === 'previewTab') {
                document.getElementById('previewTitle').textContent = 
                    document.getElementById('id_title').value || '文章标题';
                
                const content = easyMDE.value();
                document.getElementById('previewContent').innerHTML = easyMDE.markdown(content);
                
                // 渲染数学公式
                renderMathInElement(document.getElementById('previewContent'), {
                    delimiters: [
                        {left: '$$', right: '$$', display: true},
                        {left: '$', right: '$', display: false},
                        {left: '\\(', right: '\\)', display: false},
                        {left: '\\[', right: '\\]', display: true}
                    ],
                    throwOnError: false,
                    trust: true
                });
            }
        });
    });
      // 标签选择器功能
    const tagBadges = document.querySelectorAll('.tag-badge');
    const tagsSelect = document.getElementById('id_tags');
    
    // 初始化已选标签
    function initSelectedTags() {
        // 检查tagsSelect是否存在并且有selectedOptions属性
        if (tagsSelect && tagsSelect.selectedOptions) {
            const selectedOptions = Array.from(tagsSelect.selectedOptions);
            const selectedIds = selectedOptions.map(option => option.value);
            
            tagBadges.forEach(badge => {
                const tagId = badge.getAttribute('data-tag-id');
                if (selectedIds.includes(tagId)) {
                    badge.classList.add('active');
                }
            });
        }
    }
      // 绑定标签点击事件
    tagBadges.forEach(badge => {
        badge.addEventListener('click', function() {
            const tagId = this.getAttribute('data-tag-id');
            this.classList.toggle('active');
            
            // 确保tagsSelect存在
            if (tagsSelect) {
                // 更新下拉选择框的值
                const options = Array.from(tagsSelect.options || []);
                const option = options.find(opt => opt.value === tagId);
                
                if (option) {
                    option.selected = this.classList.contains('active');
                }
            }
        });
    });
    
    // 初始化标签
    initSelectedTags();

    // 自动生成slug
    var titleInput = document.getElementById('id_title');
    var slugInput = document.getElementById('id_slug');
    
    // 只在创建新文章且slug未填写时自动生成
    if (!slugInput.value) {
        titleInput.addEventListener('input', function() {
            slugInput.value = titleInput.value
                .toLowerCase()
                .replace(/[^\w\s-]/g, '') // 移除非字母数字字符
                .replace(/\s+/g, '-')     // 替换空格为连字符
                .replace(/-+/g, '-');     // 替换多个连字符为单个连字符
        });
    }
      // 添加表单提交前的验证
    document.getElementById('postForm').addEventListener('submit', function(e) {
        const title = document.getElementById('id_title').value.trim();
        const content = easyMDE.value().trim();
        
        if (!title) {
            e.preventDefault();
            alert('请填写文章标题');
            document.getElementById('id_title').focus();
            return;
        }
        
        if (!content) {
            e.preventDefault();
            alert('请填写文章内容');
            easyMDE.codemirror.focus();
            return;
        }
        
        // 在提交前将内容写回原始的textarea
        document.getElementById('id_content').value = content;
        
        // 移除required属性以避免浏览器验证隐藏元素
        document.getElementById('id_content').removeAttribute('required');
    });
    });
    
    // 为标题、内容添加淡入动画
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
        el.classList.add('visible');
    });
});
