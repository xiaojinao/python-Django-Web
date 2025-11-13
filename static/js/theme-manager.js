/**
 * 主题管理JavaScript模块
 * 提供主题切换和管理功能
 */
class ThemeManager {
    constructor() {
        this.currentTheme = this.getCurrentTheme();
        this.init();
    }

    /**
     * 初始化主题管理器
     */
    init() {
        this.applyTheme(this.currentTheme);
        
        this.setupEventListeners();
        
        // 不再自动从服务器加载主题变量，使用本地定义的变量
        // this.loadThemeVariables();
    }

    /**
     * 获取当前主题
     */
    getCurrentTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        
        const themeAttr = document.body.getAttribute('data-theme');
        if (themeAttr) {
            return themeAttr;
        }
        
        return 'light';
    }

    /**
     * 应用主题
     */
    applyTheme(theme) {
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;
        
        this.updateThemeSelectorUI();
    }

    /**
     * 切换主题
     */
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.switchTheme(newTheme);
    }

    /**
     * 切换到指定主题
     */
    switchTheme(theme) {
        this.applyTheme(theme);
        
        // this.loadThemeVariables();
        
        this.notifyThemeChange(theme);
    }

    /**
     * 设置事件监听器
     */
    setupEventListeners() {
        const themeToggleBtn = document.getElementById('theme-toggle');
        if (themeToggleBtn) {
            themeToggleBtn.addEventListener('click', () => {
                this.toggleTheme();
            });
        }

        const themeOptions = document.querySelectorAll('.theme-option');
        themeOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.preventDefault();
                
                const themeOption = e.currentTarget;
                const theme = themeOption.getAttribute('data-theme');
                if (theme) {
                    this.switchTheme(theme);
                }
            });
        });

        const themeCards = document.querySelectorAll('.theme-card');
        themeCards.forEach(card => {
            card.addEventListener('click', (e) => {
                if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') {
                    return;
                }
                
                const themeId = card.getAttribute('data-theme-id');
                if (themeId) {
                    window.location.href = `/themes/switch/${themeId}/`;
                }
            });
        });
        
        const applyThemeBtns = document.querySelectorAll('.apply-theme-btn');
        applyThemeBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const theme = btn.getAttribute('data-theme');
                if (theme) {
                    this.switchTheme(theme);
                }
            });
        });
        
        const quickThemeBtns = document.querySelectorAll('.theme-quick-btn');
        quickThemeBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const theme = btn.getAttribute('data-theme');
                if (theme) {
                    this.switchTheme(theme);
                    quickThemeBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                }
            });
        });
    }

    /**
     * 更新主题选择器UI
     */
    updateThemeSelectorUI() {
        const themeOptions = document.querySelectorAll('.theme-option');
        themeOptions.forEach(option => {
            const theme = option.getAttribute('data-theme');
            if (theme === this.currentTheme) {
                option.classList.add('active');
                const indicator = option.querySelector('.active-indicator');
                if (indicator) {
                    indicator.classList.remove('d-none');
                }
            } else {
                option.classList.remove('active');
                const indicator = option.querySelector('.active-indicator');
                if (indicator) {
                    indicator.classList.add('d-none');
                }
            }
        });

        const themeCards = document.querySelectorAll('.theme-card');
        themeCards.forEach(card => {
            const isActive = card.classList.contains('active');
            const themeId = card.getAttribute('data-theme-id');
            
            if (isActive) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });

        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.checked = this.currentTheme === 'dark';
        }
        
        const quickThemeBtns = document.querySelectorAll('.theme-quick-btn');
        quickThemeBtns.forEach(btn => {
            const theme = btn.getAttribute('data-theme');
            if (theme === this.currentTheme) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    /**
     * 从服务器加载主题变量
     */
    async loadThemeVariables() {
        try {
            const response = await fetch('/api/theme-variables/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
            });
            
            if (response.ok) {
                const variables = await response.json();
                this.applyThemeVariables(variables);
            }
        } catch (error) {
            console.error('加载主题变量失败:', error);
        }
    }

    /**
     * 应用主题变量
     */
    applyThemeVariables(variables) {
        const root = document.documentElement;
        
        for (const [name, value] of Object.entries(variables)) {
            root.style.setProperty(`--${name}`, value);
        }
    }

    /**
     * 通知服务器主题变更
     */
    async notifyThemeChange(theme) {
        // 这里可以根据需要实现服务器通知逻辑
        // 例如发送AJAX请求到服务器记录用户的主题偏好
        console.log(`主题已切换到: ${theme}`);
    }

    /**
     * 获取CSRF令牌
     */
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                return cookie.substring('csrftoken='.length);
            }
        }
        return '';
    }

    /**
     * 添加新主题
     */
    addTheme(themeData) {
        // 这里可以实现添加新主题的逻辑
        // 例如发送AJAX请求到服务器创建新主题
        console.log('添加新主题:', themeData);
    }

    /**
     * 删除主题
     */
    removeTheme(themeId) {
        // 这里可以实现删除主题的逻辑
        // 例如发送AJAX请求到服务器删除主题
        console.log('删除主题:', themeId);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

window.ThemeManager = ThemeManager;