// Playlist Management
class PlaylistManager {
    constructor() {
        this.videos = [];
        this.currentIndex = 0;
        this.container = null;
    }

    // Initialize playlist
    init(containerId) {
        this.container = document.getElementById(containerId);
        this.render();
    }

    // Add video to playlist
    addVideo(videoInfo) {
        this.videos.push({
            ...videoInfo,
            id: videoInfo.id,
            name: videoInfo.name,
            size: videoInfo.size,
            url: videoInfo.url,
            md5: null,
            match: null,
            episodeId: null,
            danmakuCount: 0,
            status: 'uploaded' // uploaded, processing, matched, failed
        });
        this.render();
        return this.videos.length - 1;
    }

    // Add multiple videos
    addVideos(videoInfos) {
        videoInfos.forEach(info => this.addVideo(info));
    }

    // Update video info
    updateVideo(index, updates) {
        if (this.videos[index]) {
            Object.assign(this.videos[index], updates);
            this.render();
        }
    }

    // Remove video from playlist
    removeVideo(index) {
        if (confirm(`确定要移除 ${this.videos[index].name} 吗？`)) {
            this.videos.splice(index, 1);
            if (this.currentIndex >= this.videos.length) {
                this.currentIndex = Math.max(0, this.videos.length - 1);
            }
            this.render();
        }
    }

    // Play video at index
    playVideo(index) {
        if (index >= 0 && index < this.videos.length) {
            this.currentIndex = index;
            const video = this.videos[index];
            
            // Update video player
            const videoPlayer = document.getElementById('video-player');
            if (videoPlayer) {
                videoPlayer.src = video.url;
            }

            // Update UI
            this.render();
            this.updateVideoInfo(video);
            
            // Trigger video change event
            window.dispatchEvent(new CustomEvent('videoChanged', { detail: video }));
        }
    }

    // Play next video
    playNext() {
        if (this.currentIndex < this.videos.length - 1) {
            this.playVideo(this.currentIndex + 1);
        } else {
            // Loop to first video if enabled
            const loopEnabled = localStorage.getItem('dandanplay_settings')?.player?.loopPlay;
            if (loopEnabled) {
                this.playVideo(0);
            }
        }
    }

    // Play previous video
    playPrevious() {
        if (this.currentIndex > 0) {
            this.playVideo(this.currentIndex - 1);
        }
    }

    // Get current video
    getCurrentVideo() {
        return this.videos[this.currentIndex] || null;
    }

    // Update video info display
    updateVideoInfo(video) {
        // Update video name
        const videoName = document.getElementById('video-name');
        if (videoName) videoName.textContent = video.name;

        // Update video size
        const videoSize = document.getElementById('video-size');
        if (videoSize) videoSize.textContent = this.formatFileSize(video.size);

        // Update MD5
        const videoMd5 = document.getElementById('video-md5');
        if (videoMd5) {
            videoMd5.textContent = video.md5 || '计算中...';
        }

        // Update match result
        const matchResult = document.getElementById('match-result');
        if (matchResult) {
            if (video.match) {
                matchResult.textContent = `${video.match.anime_title} - ${video.match.episode_title}`;
            } else {
                matchResult.textContent = video.status === 'processing' ? '匹配中...' : '未匹配';
            }
        }
    }

    // Render playlist UI
    render() {
        if (!this.container) return;

        if (this.videos.length === 0) {
            this.container.innerHTML = '<div class="empty-playlist">播放列表为空</div>';
            return;
        }

        const html = `
            <div class="playlist-header">
                <h3>播放列表 (${this.videos.length})</h3>
                <div class="playlist-controls">
                    <button class="btn-small" onclick="playlistManager.clearAll()">清空列表</button>
                </div>
            </div>
            <div class="playlist-items">
                ${this.videos.map((video, index) => this.renderVideoItem(video, index)).join('')}
            </div>
            <div class="playlist-footer">
                <button class="btn-small" onclick="playlistManager.playPrevious()" ${this.currentIndex === 0 ? 'disabled' : ''}>
                    ⏮ 上一个
                </button>
                <span>${this.currentIndex + 1} / ${this.videos.length}</span>
                <button class="btn-small" onclick="playlistManager.playNext()" ${this.currentIndex === this.videos.length - 1 ? 'disabled' : ''}>
                    下一个 ⏭
                </button>
            </div>
        `;

        this.container.innerHTML = html;
    }

    // Render single video item
    renderVideoItem(video, index) {
        const isActive = index === this.currentIndex;
        const statusIcon = this.getStatusIcon(video.status);
        const statusText = this.getStatusText(video.status);

        return `
            <div class="playlist-item ${isActive ? 'active' : ''}" data-index="${index}">
                <div class="playlist-item-info" onclick="playlistManager.playVideo(${index})">
                    <div class="playlist-item-number">${index + 1}</div>
                    <div class="playlist-item-details">
                        <div class="playlist-item-name">${video.name}</div>
                        <div class="playlist-item-meta">
                            <span class="size">${this.formatFileSize(video.size)}</span>
                            <span class="status ${video.status}">${statusIcon} ${statusText}</span>
                            ${video.danmakuCount > 0 ? `<span class="danmaku-count">弹幕: ${video.danmakuCount}</span>` : ''}
                        </div>
                        ${video.match ? `
                            <div class="playlist-item-match">
                                ${video.match.anime_title} - ${video.match.episode_title}
                            </div>
                        ` : ''}
                    </div>
                </div>
                <div class="playlist-item-actions">
                    ${isActive ? '<span class="playing-indicator">▶</span>' : ''}
                    <button class="btn-icon" onclick="playlistManager.removeVideo(${index})" title="移除">
                        ❌
                    </button>
                </div>
            </div>
        `;
    }

    // Get status icon
    getStatusIcon(status) {
        const icons = {
            'uploaded': '📁',
            'processing': '⏳',
            'matched': '✅',
            'failed': '❌'
        };
        return icons[status] || '❓';
    }

    // Get status text
    getStatusText(status) {
        const texts = {
            'uploaded': '已上传',
            'processing': '处理中',
            'matched': '已匹配',
            'failed': '匹配失败'
        };
        return texts[status] || '未知';
    }

    // Clear all videos
    clearAll() {
        if (confirm('确定要清空播放列表吗？')) {
            this.videos = [];
            this.currentIndex = 0;
            this.render();
            
            // Clear video player
            const videoPlayer = document.getElementById('video-player');
            if (videoPlayer) {
                videoPlayer.src = '';
            }

            // Hide video sections
            document.getElementById('video-info').style.display = 'none';
            document.getElementById('player-section').style.display = 'none';
        }
    }

    // Format file size
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    // Export playlist
    exportPlaylist() {
        const data = {
            videos: this.videos.map(v => ({
                name: v.name,
                size: v.size,
                match: v.match
            })),
            exportDate: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `playlist_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Create global instance
const playlistManager = new PlaylistManager();