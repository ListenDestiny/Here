// Web3工作抓取器前端JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 初始化应用
    initializeApp();
});

function initializeApp() {
    // 初始化工具提示
    initializeTooltips();
    
    // 初始化搜索功能
    initializeSearch();
    
    // 初始化统计更新
    initializeStatsUpdate();
    
    // 初始化管理功能
    initializeAdminFeatures();
}

// 初始化Bootstrap工具提示
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 初始化搜索功能
function initializeSearch() {
    const searchForm = document.querySelector('form[action="/jobs"]');
    if (searchForm) {
        // 添加搜索建议功能
        const searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(handleSearchInput, 300));
        }
    }
}

// 搜索输入处理
function handleSearchInput(event) {
    const query = event.target.value.trim();
    if (query.length >= 2) {
        // 这里可以添加搜索建议功能
        console.log('搜索查询:', query);
    }
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 初始化统计更新
function initializeStatsUpdate() {
    // 每30秒更新一次统计信息
    if (window.location.pathname === '/' || window.location.pathname === '/admin') {
        setInterval(updateStats, 30000);
    }
}

// 更新统计信息
async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        // 更新统计卡片
        updateStatCard('total_jobs', stats.total_jobs);
        updateStatCard('recent_jobs', stats.recent_jobs);
        updateStatCard('remote_jobs', stats.remote_jobs);
        updateStatCard('translated_jobs', stats.translated_jobs);
        
    } catch (error) {
        console.error('更新统计信息失败:', error);
    }
}

// 更新单个统计卡片
function updateStatCard(statName, value) {
    const elements = document.querySelectorAll(`[data-stat="${statName}"]`);
    elements.forEach(element => {
        if (element.textContent !== value.toString()) {
            element.textContent = value;
            // 添加更新动画
            element.classList.add('stat-updated');
            setTimeout(() => {
                element.classList.remove('stat-updated');
            }, 1000);
        }
    });
}

// 初始化管理功能
function initializeAdminFeatures() {
    // 抓取按钮处理
    const scrapeButton = document.querySelector('button[type="submit"][form*="scrape"]');
    if (scrapeButton) {
        scrapeButton.addEventListener('click', handleScrapeClick);
    }
    
    // 测试邮件按钮处理
    const testEmailButton = document.querySelector('button[type="submit"][form*="test-email"]');
    if (testEmailButton) {
        testEmailButton.addEventListener('click', handleTestEmailClick);
    }
}

// 处理抓取按钮点击
function handleScrapeClick(event) {
    const button = event.target;
    const originalText = button.innerHTML;
    
    // 显示加载状态
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 抓取中...';
    
    // 显示进度提示
    showNotification('开始抓取工作信息，请稍候...', 'info');
    
    // 设置超时恢复按钮状态
    setTimeout(() => {
        if (button.disabled) {
            button.disabled = false;
            button.innerHTML = originalText;
        }
    }, 60000); // 60秒后恢复
}

// 处理测试邮件按钮点击
function handleTestEmailClick(event) {
    const button = event.target;
    const originalText = button.innerHTML;
    
    // 显示加载状态
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 发送中...';
    
    // 显示提示
    showNotification('正在发送测试邮件...', 'info');
    
    // 设置超时恢复按钮状态
    setTimeout(() => {
        if (button.disabled) {
            button.disabled = false;
            button.innerHTML = originalText;
        }
    }, 10000); // 10秒后恢复
}

// 显示通知
function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const iconClass = type === 'success' ? 'fa-check-circle' : 
                     type === 'error' ? 'fa-exclamation-circle' : 
                     type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
    
    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas ${iconClass} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // 自动移除通知
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// 工作卡片交互
function initializeJobCards() {
    const jobCards = document.querySelectorAll('.job-card, .card');
    
    jobCards.forEach(card => {
        // 添加悬停效果
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// 搜索结果高亮
function highlightSearchResults(searchTerm) {
    if (!searchTerm) return;
    
    const elements = document.querySelectorAll('.job-title, .card-text');
    elements.forEach(element => {
        const text = element.textContent;
        const highlightedText = text.replace(
            new RegExp(searchTerm, 'gi'),
            `<mark>$&</mark>`
        );
        if (highlightedText !== text) {
            element.innerHTML = highlightedText;
        }
    });
}

// 无限滚动加载（如果需要）
function initializeInfiniteScroll() {
    let loading = false;
    let page = 1;
    
    window.addEventListener('scroll', () => {
        if (loading) return;
        
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
            loading = true;
            loadMoreJobs(++page).finally(() => {
                loading = false;
            });
        }
    });
}

// 加载更多工作
async function loadMoreJobs(page) {
    try {
        const url = new URL(window.location);
        url.searchParams.set('page', page);
        
        const response = await fetch(url);
        const html = await response.text();
        
        // 解析HTML并添加到页面
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newJobs = doc.querySelectorAll('.job-card');
        
        const container = document.querySelector('.job-container');
        if (container && newJobs.length > 0) {
            newJobs.forEach(job => {
                container.appendChild(job);
            });
            
            // 重新初始化新添加的卡片
            initializeJobCards();
        }
        
    } catch (error) {
        console.error('加载更多工作失败:', error);
    }
}

// 复制链接功能
function copyJobLink(jobId) {
    const url = `${window.location.origin}/job/${jobId}`;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
            showNotification('工作链接已复制到剪贴板', 'success');
        });
    } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = url;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('工作链接已复制到剪贴板', 'success');
    }
}

// 收藏工作功能（本地存储）
function toggleJobFavorite(jobId) {
    const favorites = JSON.parse(localStorage.getItem('favoriteJobs') || '[]');
    const index = favorites.indexOf(jobId);
    
    if (index > -1) {
        favorites.splice(index, 1);
        showNotification('已从收藏中移除', 'info');
    } else {
        favorites.push(jobId);
        showNotification('已添加到收藏', 'success');
    }
    
    localStorage.setItem('favoriteJobs', JSON.stringify(favorites));
    updateFavoriteButtons();
}

// 更新收藏按钮状态
function updateFavoriteButtons() {
    const favorites = JSON.parse(localStorage.getItem('favoriteJobs') || '[]');
    
    document.querySelectorAll('[data-job-id]').forEach(button => {
        const jobId = parseInt(button.dataset.jobId);
        const isFavorite = favorites.includes(jobId);
        
        button.classList.toggle('favorited', isFavorite);
        button.innerHTML = isFavorite ? 
            '<i class="fas fa-heart"></i>' : 
            '<i class="far fa-heart"></i>';
    });
}

// 键盘快捷键
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K 聚焦搜索框
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // ESC 清除搜索
    if (event.key === 'Escape') {
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput && searchInput === document.activeElement) {
            searchInput.value = '';
            searchInput.blur();
        }
    }
});

// 页面可见性变化时更新数据
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // 页面变为可见时更新统计信息
        updateStats();
    }
});

// CSS动画类
const style = document.createElement('style');
style.textContent = `
    .stat-updated {
        animation: statUpdate 1s ease-in-out;
    }
    
    @keyframes statUpdate {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); color: #28a745; }
        100% { transform: scale(1); }
    }
    
    .favorited {
        color: #dc3545 !important;
    }
    
    mark {
        background-color: #fff3cd;
        padding: 2px 4px;
        border-radius: 3px;
    }
`;
document.head.appendChild(style);