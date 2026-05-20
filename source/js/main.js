// 存勤法税官网交互脚本

// 返回顶部功能
document.addEventListener('DOMContentLoaded', function() {
    const backToTop = document.getElementById('backToTop');
    
    if (backToTop) {
        // 监听滚动
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
        
        // 点击返回顶部
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // 移动端菜单
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const siteNav = document.querySelector('.site-nav');
    
    if (mobileMenuBtn && siteNav) {
        mobileMenuBtn.addEventListener('click', function() {
            siteNav.classList.toggle('active');
            this.querySelector('i').classList.toggle('fa-bars');
            this.querySelector('i').classList.toggle('fa-times');
        });
        
        // 点击导航链接后关闭菜单
        const navLinks = siteNav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                siteNav.classList.remove('active');
                mobileMenuBtn.querySelector('i').classList.add('fa-bars');
                mobileMenuBtn.querySelector('i').classList.remove('fa-times');
            });
        });
    }
    
    // 滚动时头部样式变化
    const siteHeader = document.querySelector('.site-header');
    if (siteHeader) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                siteHeader.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
                siteHeader.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
            } else {
                siteHeader.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
                siteHeader.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
            }
        });
    }
    
    // 数字动画效果
    const statNumbers = document.querySelectorAll('.stat-number');
    if (statNumbers.length > 0) {
        let animated = false;
        
        function animateNumbers() {
            if (animated) return;
            
            const statsSection = document.querySelector('.stats-section');
            if (!statsSection) return;
            
            const rect = statsSection.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                animated = true;
                
                statNumbers.forEach(number => {
                    const target = parseInt(number.textContent);
                    let current = 0;
                    const increment = target / 100;
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= target) {
                            current = target;
                            clearInterval(timer);
                        }
                        number.textContent = Math.floor(current);
                    }, 20);
                });
            }
        }
        
        window.addEventListener('scroll', animateNumbers);
        animateNumbers(); // 初始检查
    }
    
    // 平滑滚动到锚点
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // 表单验证（如果有联系表单）
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 简单验证
            const name = this.querySelector('[name="name"]');
            const email = this.querySelector('[name="email"]');
            const message = this.querySelector('[name="message"]');
            
            if (!name || !name.value.trim()) {
                alert('请填写您的姓名');
                return;
            }
            
            if (!email || !email.value.trim() || !email.value.includes('@')) {
                alert('请填写有效的邮箱地址');
                return;
            }
            
            if (!message || !message.value.trim()) {
                alert('请填写留言内容');
                return;
            }
            
            // 表单提交成功提示
            alert('感谢您的留言！我们会尽快与您联系。');
            this.reset();
        });
    }
    
    // 图片懒加载
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // 当前页面导航高亮
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.site-nav a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation ||
            (currentLocation.includes('/services') && link.getAttribute('href').includes('/services')) ||
            (currentLocation.includes('/cases') && link.getAttribute('href').includes('/cases')) ||
            (currentLocation.includes('/about') && link.getAttribute('href').includes('/about')) ||
            (currentLocation.includes('/contact') && link.getAttribute('href').includes('/contact'))) {
            link.style.color = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim();
            link.style.fontWeight = '600';
        }
    });
});

// 页面加载完成后的初始化
window.addEventListener('load', function() {
    // 隐藏加载动画（如果有）
    const loader = document.querySelector('.page-loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 500);
    }
    
    // 触发滚动事件以初始化某些状态
    window.dispatchEvent(new Event('scroll'));
});
