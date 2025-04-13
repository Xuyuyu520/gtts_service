import os
from pathlib import Path


class Config:
    # 应用配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

    # 路径配置
    BASE_DIR = Path(__file__).resolve().parent
    AUDIO_DIR = BASE_DIR / 'app' / 'static' / 'audio'

    # TTS配置
    DEFAULT_VOICE = 'zh-CN'  # gTTS使用的语言代码
    AUDIO_RETENTION_HOURS = 24  # 音频文件保留时间（小时）

    # API配置
    API_TITLE = 'gTTS API'
    API_VERSION = 'v1'
    API_DESCRIPTION = 'API for text-to-speech conversion using Google Text-to-Speech'

    # 服务器配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
