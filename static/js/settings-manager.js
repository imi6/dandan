/**
 * 设置管理器 - 管理所有应用设置
 */
class SettingsManager {
    constructor() {
        this.storageKey = 'danplay_settings';
        this.defaultSettings = {
            // 常规设置
            general: {
                theme: 'auto',           // auto, light, dark
                language: 'zh-CN',       // zh-CN, zh-TW, en, ja
                autoMatch: true,         // 自动匹配弹幕
                saveHistory: true        // 保存播放历史
            },
            // 播放器设置
            player: {
                engine: 'native',        // native, nplayer, artplayer, dplayer
                defaultVolume: 80,       // 0-100
                autoPlay: false,         // 自动播放
                rememberPosition: true   // 记忆播放位置
            },
            // 弹幕设置
            danmaku: {
                opacity: 100,            // 0-100 透明度
                fontSize: 'medium',      // small, medium, large, xlarge
                speed: 'normal',         // slow, normal, fast
                blockTop: false,         // 屏蔽顶部弹幕
                blockBottom: false,      // 屏蔽底部弹幕
                blockScroll: false,      // 屏蔽滚动弹幕
                smartBlock: false        // 智能防挡
            },
            // 网络设置
            network: {
                apiServer: 'https://api.dandanplay.net/api/v2',
                useProxy: false,
                proxyUrl: '',
                enableCache: true,
                cacheExpiry: 86400      // 缓存过期时间(秒)
            },
            // 高级设置
            advanced: {
                hardwareAcceleration: true,
                debugMode: false,
                logLevel: 'info',       // debug, info, warning, error
                maxUploadSize: 500      // MB
            }
        };
        
        this.settings = this.loadSettings();
        this.listeners = new Map();
    }

    /**
     * 加载设置
     */
    loadSettings() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                const parsed = JSON.parse(stored);
                // 深度合并，确保新增的设置项有默认值
                return this.deepMerge(this.defaultSettings, parsed);
            }
        } catch (error) {
            console.error('Failed to load settings:', error);
        }
        return JSON.parse(JSON.stringify(this.defaultSettings));
    }

    /**
     * 保存设置
     */
    saveSettings() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.settings));
            this.notifyListeners('save', this.settings);
            return true;
        } catch (error) {
            console.error('Failed to save settings:', error);
            return false;
        }
    }

    /**
     * 获取设置值
     */
    get(path) {
        const keys = path.split('.');
        let value = this.settings;
        for (const key of keys) {
            if (value && typeof value === 'object' && key in value) {
                value = value[key];
            } else {
                return undefined;
            }
        }
        return value;
    }

    /**
     * 设置值
     */
    set(path, value) {
        const keys = path.split('.');
        const lastKey = keys.pop();
        let target = this.settings;
        
        for (const key of keys) {
            if (!(key in target) || typeof target[key] !== 'object') {
                target[key] = {};
            }
            target = target[key];
        }
        
        const oldValue = target[lastKey];
        target[lastKey] = value;
        
        // 立即应用设置
        this.applySettingChange(path, value, oldValue);
        
        // 保存到本地存储
        this.saveSettings();
        
        // 通知监听器
        this.notifyListeners('change', { path, value, oldValue });
    }

    /**
     * 应用设置变更
     */
    applySettingChange(path, value, oldValue) {
        switch (path) {
            case 'general.theme':
                this.applyTheme(value);
                break;
            case 'general.language':
                this.applyLanguage(value);
                break;
            case 'player.defaultVolume':
                this.applyVolume(value);
                break;
            case 'danmaku.opacity':
                this.applyDanmakuOpacity(value);
                break;
            case 'danmaku.fontSize':
                this.applyDanmakuFontSize(value);
                break;
            case 'danmaku.speed':
                this.applyDanmakuSpeed(value);
                break;
            case 'advanced.debugMode':
                this.applyDebugMode(value);
                break;
        }
    }

    /**
     * 应用主题
     */
    applyTheme(theme) {
        const root = document.documentElement;
        
        // 移除所有主题类
        root.classList.remove('theme-light', 'theme-dark', 'theme-auto');
        
        if (theme === 'auto') {
            // 检测系统主题
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            root.classList.add(prefersDark ? 'theme-dark' : 'theme-light');
        } else {
            root.classList.add(`theme-${theme}`);
        }
    }

    /**
     * 应用语言
     */
    applyLanguage(language) {
        document.documentElement.lang = language;
        // 这里可以添加i18n库的语言切换逻辑
        console.log(`Language changed to: ${language}`);
    }

    /**
     * 应用音量设置
     */
    applyVolume(volume) {
        const videoPlayer = document.getElementById('video-player');
        if (videoPlayer) {
            videoPlayer.volume = volume / 100;
        }
    }

    /**
     * 应用弹幕透明度
     */
    applyDanmakuOpacity(opacity) {
        const danmakuContainer = document.getElementById('danmaku-container');
        if (danmakuContainer) {
            danmakuContainer.style.opacity = opacity / 100;
        }
    }

    /**
     * 应用弹幕字号
     */
    applyDanmakuFontSize(size) {
        const sizeMap = {
            'small': '12px',
            'medium': '16px',
            'large': '20px',
            'xlarge': '24px'
        };
        
        document.documentElement.style.setProperty('--danmaku-font-size', sizeMap[size] || '16px');
    }

    /**
     * 应用弹幕速度
     */
    applyDanmakuSpeed(speed) {
        const speedMap = {
            'slow': '15s',
            'normal': '10s',
            'fast': '7s'
        };
        
        document.documentElement.style.setProperty('--danmaku-duration', speedMap[speed] || '10s');
    }

    /**
     * 应用调试模式
     */
    applyDebugMode(enabled) {
        if (enabled) {
            console.log('Debug mode enabled');
            window.DEBUG = true;
        } else {
            console.log('Debug mode disabled');
            window.DEBUG = false;
        }
    }

    /**
     * 重置设置
     */
    reset(category = null) {
        if (category && category in this.defaultSettings) {
            this.settings[category] = JSON.parse(JSON.stringify(this.defaultSettings[category]));
        } else {
            this.settings = JSON.parse(JSON.stringify(this.defaultSettings));
        }
        
        this.saveSettings();
        this.applyAllSettings();
        this.notifyListeners('reset', category);
    }

    /**
     * 导出设置
     */
    export() {
        const data = {
            version: '1.0.0',
            timestamp: new Date().toISOString(),
            settings: this.settings
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `danplay-settings-${Date.now()}.json`;
        a.click();
        
        URL.revokeObjectURL(url);
    }

    /**
     * 导入设置
     */
    async import(file) {
        try {
            const text = await file.text();
            const data = JSON.parse(text);
            
            if (data.settings) {
                this.settings = this.deepMerge(this.defaultSettings, data.settings);
                this.saveSettings();
                this.applyAllSettings();
                this.notifyListeners('import', data);
                return true;
            }
        } catch (error) {
            console.error('Failed to import settings:', error);
        }
        return false;
    }

    /**
     * 应用所有设置
     */
    applyAllSettings() {
        // 应用主题
        this.applyTheme(this.get('general.theme'));
        
        // 应用语言
        this.applyLanguage(this.get('general.language'));
        
        // 应用播放器设置
        this.applyVolume(this.get('player.defaultVolume'));
        
        // 应用弹幕设置
        this.applyDanmakuOpacity(this.get('danmaku.opacity'));
        this.applyDanmakuFontSize(this.get('danmaku.fontSize'));
        this.applyDanmakuSpeed(this.get('danmaku.speed'));
        
        // 应用调试模式
        this.applyDebugMode(this.get('advanced.debugMode'));
    }

    /**
     * 添加设置变更监听器
     */
    addListener(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }
        this.listeners.get(event).add(callback);
    }

    /**
     * 移除监听器
     */
    removeListener(event, callback) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).delete(callback);
        }
    }

    /**
     * 通知监听器
     */
    notifyListeners(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error('Listener error:', error);
                }
            });
        }
    }

    /**
     * 深度合并对象
     */
    deepMerge(target, source) {
        const result = { ...target };
        
        for (const key in source) {
            if (source.hasOwnProperty(key)) {
                if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
                    result[key] = this.deepMerge(result[key] || {}, source[key]);
                } else {
                    result[key] = source[key];
                }
            }
        }
        
        return result;
    }

    /**
     * 同步设置到服务器
     */
    async syncToServer() {
        try {
            const response = await fetch('/api/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.settings)
            });
            
            if (response.ok) {
                console.log('Settings synced to server');
                return true;
            }
        } catch (error) {
            console.error('Failed to sync settings:', error);
        }
        return false;
    }

    /**
     * 从服务器加载设置
     */
    async syncFromServer() {
        try {
            const response = await fetch('/api/settings');
            if (response.ok) {
                const serverSettings = await response.json();
                this.settings = this.deepMerge(this.defaultSettings, serverSettings);
                this.saveSettings();
                this.applyAllSettings();
                return true;
            }
        } catch (error) {
            console.error('Failed to load settings from server:', error);
        }
        return false;
    }
}

// 创建全局设置管理器实例
window.settingsManager = new SettingsManager();

// 页面加载时应用所有设置
document.addEventListener('DOMContentLoaded', () => {
    window.settingsManager.applyAllSettings();
});