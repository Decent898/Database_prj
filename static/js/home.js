// 计数器动画函数
function animateCounter(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// 卡片淡入动画
function setupCardAnimations() {
    const cards = document.querySelectorAll('.signature-card, .post-card, .stats-box');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// 主页初始化
document.addEventListener('DOMContentLoaded', function() {
    // 创建随机旋转的签名作为背景装饰
    setupFeaturedSignatures();
    
    // 设置卡片动画
    setupCardAnimations();
    
    // 初始化统计数字动画
    initCounters();
});

// 初始化统计数字动画
function initCounters() {
    const statsNumbers = document.querySelectorAll('.stats-number');
    
    statsNumbers.forEach(counter => {
        const target = parseInt(counter.innerText.replace(/\D/g, ''), 10);
        animateCounter(counter, 0, target, 2000);
    });
}

// 设置特色签名作为背景
function setupFeaturedSignatures() {
    const container = document.getElementById('featured-signatures-container');
    if (!container) return;
    
    // 清除容器内容
    container.innerHTML = '';
    
    // 获取签名图片元素
    const signatureImgs = document.querySelectorAll('.signature-preview img');
    if (signatureImgs.length === 0) return;
    
    // 创建5-8个随机位置的签名
    const signatureCount = Math.min(Math.floor(Math.random() * 4) + 5, signatureImgs.length * 2);
    
    for (let i = 0; i < signatureCount; i++) {
        const img = document.createElement('img');
        img.src = signatureImgs[i % signatureImgs.length].src;
        img.alt = "装饰签名";
        img.classList.add('featured-signature');
        
        // 随机位置和旋转
        const randomX = Math.floor(Math.random() * 80);
        const randomY = Math.floor(Math.random() * 80);
        const randomRotate = Math.floor(Math.random() * 360);
        const randomScale = 0.2 + Math.random() * 0.3;
        
        img.style.left = randomX + '%';
        img.style.top = randomY + '%';
        img.style.transform = `rotate(${randomRotate}deg) scale(${randomScale})`;
        
        container.appendChild(img);
    }
}
