// DanDanPlay Python Frontend
const API_BASE = '/api';
let currentVideoId = null;
let currentEpisodeId = null;

// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const selectBtn = document.getElementById('select-btn');
const uploadProgress = document.getElementById('upload-progress');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');
const videoInfo = document.getElementById('video-info');
const playerSection = document.getElementById('player-section');
const videoPlayer = document.getElementById('video-player');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupUploadHandlers();
    setupDanmakuControls();
    playlistManager.init('playlist-container');
    
    // Listen for video change events
    window.addEventListener('videoChanged', (e) => {
        const video = e.detail;
        if (video.id) {
            currentVideoId = video.id;
            currentEpisodeId = video.episodeId;
            
            // Check MD5 if not calculated
            if (!video.md5) {
                checkMD5Status();
            }
        }
    });
});

// Upload Handlers
function setupUploadHandlers() {
    // File select button
    selectBtn.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        if (files.length > 0) {
            uploadMultipleFiles(files);
        }
    });
    
    // Drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files);
        if (files.length > 0) {
            uploadMultipleFiles(files);
        }
    });
}

// Upload multiple files
async function uploadMultipleFiles(files) {
    // Filter video files only
    const videoFiles = files.filter(file => {
        return file.type.startsWith('video/') || 
               file.name.match(/\.(mp4|mkv|avi|mov|wmv|flv|webm)$/i);
    });
    
    if (videoFiles.length === 0) {
        alert('请选择视频文件');
        return;
    }
    
    // Show playlist section
    document.getElementById('playlist-section').style.display = 'block';
    
    // Upload files one by one
    for (let i = 0; i < videoFiles.length; i++) {
        const file = videoFiles[i];
        showNotification(`正在上传 ${i + 1}/${videoFiles.length}: ${file.name}`);
        await uploadFile(file, i === 0); // Auto play first video
    }
    
    showNotification(`成功上传 ${videoFiles.length} 个文件`, 'success');
}

// Upload single file
async function uploadFile(file, autoPlay = true) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Show progress
    uploadProgress.style.display = 'block';
    
    try {
        const xhr = new XMLHttpRequest();
        
        // Progress tracking
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete + '%';
                progressText.textContent = Math.round(percentComplete) + '%';
            }
        });
        
        // Handle completion
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                handleUploadSuccess(response.data, autoPlay);
            } else {
                alert('上传失败: ' + xhr.statusText);
            }
            uploadProgress.style.display = 'none';
        });
        
        // Send request
        xhr.open('POST', `${API_BASE}/video/upload`);
        xhr.send(formData);
        
    } catch (error) {
        alert('上传错误: ' + error.message);
        uploadProgress.style.display = 'none';
    }
}

// Handle successful upload
async function handleUploadSuccess(data, autoPlay = true) {
    // Add to playlist
    const videoIndex = playlistManager.addVideo(data);
    
    // Show sections
    document.getElementById('playlist-section').style.display = 'block';
    videoInfo.style.display = 'block';
    playerSection.style.display = 'block';
    
    if (autoPlay) {
        // Play the video
        playlistManager.playVideo(videoIndex);
        currentVideoId = data.id;
        
        // Start MD5 calculation check
        checkMD5StatusForVideo(videoIndex, data.id);
    }
}

// Check MD5 calculation status
async function checkMD5Status() {
    const checkInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/video/md5/${currentVideoId}`);
            const data = await response.json();
            
            if (data.ready && data.md5) {
                document.getElementById('video-md5').textContent = data.md5;
                clearInterval(checkInterval);
                
                // Auto match video
                matchVideo(data.md5);
            }
        } catch (error) {
            console.error('MD5 check error:', error);
        }
    }, 1000);
}

// Match video
async function matchVideo(md5Hash) {
    const videoName = document.getElementById('video-name').textContent;
    const videoSizeText = document.getElementById('video-size').textContent;
    const videoSize = parseInt(videoSizeText.replace(/[^\d]/g, ''));
    
    try {
        const response = await fetch(`${API_BASE}/match/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                file_name: videoName,
                file_hash: md5Hash,
                file_size: videoSize
            })
        });
        
        const data = await response.json();
        
        if (data.is_matched && data.matches.length > 0) {
            const match = data.matches[0];
            document.getElementById('match-result').textContent = 
                `${match.anime_title} - ${match.episode_title}`;
            currentEpisodeId = match.episode_id;
            
            // Load danmaku
            loadDanmaku(match.episode_id);
        } else {
            document.getElementById('match-result').textContent = '未匹配到视频';
        }
    } catch (error) {
        document.getElementById('match-result').textContent = '匹配失败';
        console.error('Match error:', error);
    }
}

// Load danmaku
async function loadDanmaku(episodeId) {
    try {
        const response = await fetch(`${API_BASE}/danmaku/${episodeId}?format=raw`);
        const data = await response.json();
        
        if (data.success && data.count > 0) {
            console.log(`加载了 ${data.count} 条弹幕`);
            // Here you would integrate with a danmaku library
            // For now, just log the result
            displayDanmakuInfo(data.count);
        }
    } catch (error) {
        console.error('Load danmaku error:', error);
    }
}

// Display danmaku info
function displayDanmakuInfo(count) {
    const info = document.createElement('div');
    info.style.cssText = 'background: #4CAF50; color: white; padding: 10px; margin: 10px 0; border-radius: 5px;';
    info.textContent = `成功加载 ${count} 条弹幕`;
    playerSection.appendChild(info);
    
    setTimeout(() => info.remove(), 3000);
}

// Setup danmaku controls
function setupDanmakuControls() {
    // Toggle danmaku
    document.getElementById('toggle-danmaku')?.addEventListener('click', () => {
        console.log('Toggle danmaku');
    });
    
    // Manual match
    document.getElementById('manual-match')?.addEventListener('click', () => {
        document.getElementById('manual-match-dialog').style.display = 'flex';
    });
    
    document.getElementById('confirm-match')?.addEventListener('click', async () => {
        const url = document.getElementById('match-url').value;
        if (url) {
            await loadExternalDanmaku(url);
        }
        document.getElementById('manual-match-dialog').style.display = 'none';
    });
    
    document.getElementById('cancel-match')?.addEventListener('click', () => {
        document.getElementById('manual-match-dialog').style.display = 'none';
    });
    
    // Load XML
    document.getElementById('load-xml')?.addEventListener('click', () => {
        document.getElementById('xml-dialog').style.display = 'flex';
    });
    
    document.getElementById('confirm-xml')?.addEventListener('click', async () => {
        const xmlContent = document.getElementById('xml-content').value;
        if (xmlContent) {
            await parseXMLDanmaku(xmlContent);
        }
        document.getElementById('xml-dialog').style.display = 'none';
    });
    
    document.getElementById('cancel-xml')?.addEventListener('click', () => {
        document.getElementById('xml-dialog').style.display = 'none';
    });
}

// Load external danmaku
async function loadExternalDanmaku(url) {
    try {
        const response = await fetch(`${API_BASE}/danmaku/external?url=${encodeURIComponent(url)}&format=raw`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success && data.count > 0) {
            displayDanmakuInfo(data.count);
        }
    } catch (error) {
        alert('加载外部弹幕失败');
    }
}

// Parse XML danmaku
async function parseXMLDanmaku(xmlContent) {
    try {
        const response = await fetch(`${API_BASE}/danmaku/parse/xml?format=raw`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({xml_content: xmlContent})
        });
        const data = await response.json();
        
        if (data.success && data.count > 0) {
            displayDanmakuInfo(data.count);
        }
    } catch (error) {
        alert('解析XML弹幕失败');
    }
}

// Check MD5 for specific video
async function checkMD5StatusForVideo(videoIndex, videoId) {
    const checkInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/video/md5/${videoId}`);
            const data = await response.json();
            
            if (data.ready && data.md5) {
                clearInterval(checkInterval);
                
                // Update video in playlist
                playlistManager.updateVideo(videoIndex, {
                    md5: data.md5,
                    status: 'processing'
                });
                
                // If this is the current video, update display
                const currentVideo = playlistManager.getCurrentVideo();
                if (currentVideo && currentVideo.id === videoId) {
                    document.getElementById('video-md5').textContent = data.md5;
                }
                
                // Auto match video
                matchVideoInPlaylist(videoIndex, data.md5);
            }
        } catch (error) {
            console.error('MD5 check error:', error);
        }
    }, 1000);
}

// Match video in playlist
async function matchVideoInPlaylist(videoIndex, md5Hash) {
    const video = playlistManager.videos[videoIndex];
    if (!video) return;
    
    try {
        const response = await fetch(`${API_BASE}/match/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                file_name: video.name,
                file_hash: md5Hash,
                file_size: video.size
            })
        });
        
        const data = await response.json();
        
        if (data.is_matched && data.matches.length > 0) {
            const match = data.matches[0];
            
            // Update video in playlist
            playlistManager.updateVideo(videoIndex, {
                match: match,
                episodeId: match.episode_id,
                status: 'matched'
            });
            
            // If this is the current video, update display and load danmaku
            const currentVideo = playlistManager.getCurrentVideo();
            if (currentVideo && currentVideo.id === video.id) {
                document.getElementById('match-result').textContent = 
                    `${match.anime_title} - ${match.episode_title}`;
                currentEpisodeId = match.episode_id;
                loadDanmaku(match.episode_id);
            }
        } else {
            playlistManager.updateVideo(videoIndex, {
                status: 'failed'
            });
            
            const currentVideo = playlistManager.getCurrentVideo();
            if (currentVideo && currentVideo.id === video.id) {
                document.getElementById('match-result').textContent = '未匹配到视频';
            }
        }
    } catch (error) {
        playlistManager.updateVideo(videoIndex, {
            status: 'failed'
        });
        console.error('Match error:', error);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
