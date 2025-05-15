/**
 * 子页面通用交互效果
 */
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有淡入元素
    initFadeEffects();
    
    // 初始化签名特效
    initSignatureEffects();
    
    // 初始化博客标签随机颜色
    initBlogTagColors();
    
    // 初始化统计数字动画
    initCounters();
});

/**
 * 设置淡入效果
 */
function initFadeEffects() {
    const fadeElements = document.querySelectorAll('.fade-in');
    
    if (fadeElements.length > 0) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    // 避免重复动画
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });
        
        fadeElements.forEach(element => {
            observer.observe(element);
        });
    }
}

/**
 * 签名动态效果
 */
function initSignatureEffects() {
    const signatureItems = document.querySelectorAll('.signature-item img');
    
    signatureItems.forEach(item => {
        // 添加随机轻微旋转
        const randomRotate = (Math.random() - 0.5) * 5; // -2.5 到 2.5 度
        item.style.transform = `rotate(${randomRotate}deg)`;
        
        // 添加悬停回正效果
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'rotate(0deg) scale(1.05)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = `rotate(${randomRotate}deg) scale(1)`;
        });
    });
}

/**
 * 为博客标签设置随机颜色
 */
function initBlogTagColors() {
    const blogTags = document.querySelectorAll('.blog-tag');
    const colors = [
        { bg: 'rgba(108, 92, 231, 0.1)', color: '#6c5ce7' }, // 紫色
        { bg: 'rgba(46, 204, 113, 0.1)', color: '#2ecc71' }, // 绿色
        { bg: 'rgba(52, 152, 219, 0.1)', color: '#3498db' }, // 蓝色
        { bg: 'rgba(230, 126, 34, 0.1)', color: '#e67e22' }, // 橙色
        { bg: 'rgba(231, 76, 60, 0.1)', color: '#e74c3c' }   // 红色
    ];
    
    blogTags.forEach(tag => {
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        tag.style.backgroundColor = randomColor.bg;
        tag.style.color = randomColor.color;
    });
}

/**
 * 数字计数动画
 */
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-count'));
        let count = 0;
        const speed = 2000 / target; // 确保动画在2秒内完成
        
        const updateCount = () => {
            if (count < target) {
                count++;
                counter.innerText = count;
                setTimeout(updateCount, speed);
            } else {
                counter.innerText = target;
            }
        };
        
        updateCount();
    });
}

/**
 * 图片加载动画
 */
function animateImageLoad() {
    const images = document.querySelectorAll('.animate-load');
    
    images.forEach(img => {
        // 初始状态
        img.style.opacity = '0';
        img.style.transform = 'scale(0.9)';
        
        // 监听加载完成事件
        img.addEventListener('load', function() {
            setTimeout(() => {
                img.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                img.style.opacity = '1';
                img.style.transform = 'scale(1)';
            }, 100);
        });
        
        // 如果图片已经加载完成
        if (img.complete) {
            setTimeout(() => {
                img.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                img.style.opacity = '1';
                img.style.transform = 'scale(1)';
            }, 100);
        }
    });
}

// 在页面加载完成后执行图片加载动画
window.addEventListener('load', animateImageLoad);
