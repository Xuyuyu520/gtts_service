import uuid
import os
import time
from datetime import datetime
from pathlib import Path
from flask import current_app
from gtts import gTTS, lang


class TTSService:
    @staticmethod
    def list_voices():
        """获取所有可用的语音列表"""
        try:
            # gTTS支持的语言列表
            languages = lang.tts_langs()

            # 按语言分组
            result = {
                'zh': [{'ShortName': 'zh-CN', 'DisplayName': '中文 (普通话)', 'Gender': 'Neutral'}],
                'en': [{'ShortName': 'en', 'DisplayName': '英语', 'Gender': 'Neutral'}],
                'other': []
            }

            # 添加其他语言
            for code, name in languages.items():
                if code not in ['zh-CN', 'en']:
                    result['other'].append({
                        'ShortName': code,
                        'DisplayName': name,
                        'Gender': 'Neutral'
                    })

            return result
        except Exception as e:
            print(f"获取语音列表出错: {str(e)}")
            return {'error': str(e)}

    @staticmethod
    def generate_speech(text, voice=None, rate=None, volume=None, pitch=None):
        """生成语音文件"""
        try:
            if not voice:
                voice = current_app.config['DEFAULT_VOICE']

            # gTTS不支持rate/volume/pitch参数，这里忽略这些参数
            # 但保留参数以保持API兼容性

            # 生成唯一文件名
            file_id = str(uuid.uuid4())
            output_path = Path(current_app.config['AUDIO_DIR']) / f"{file_id}.mp3"

            # 调用gTTS生成语音
            tts = gTTS(text=text, lang=voice, slow=False)
            tts.save(str(output_path))

            # 返回文件信息
            return {
                'success': True,
                'file_id': file_id,
                'file_path': f"/static/audio/{file_id}.mp3",
                'created_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"生成语音出错: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def clean_old_files():
        """清理过期的音频文件"""
        try:
            retention_hours = current_app.config['AUDIO_RETENTION_HOURS']
            cutoff_time = time.time() - (retention_hours * 3600)

            audio_dir = Path(current_app.config['AUDIO_DIR'])
            for file in audio_dir.glob('*.mp3'):
                if file.stat().st_mtime < cutoff_time:
                    os.remove(file)
                    print(f"已删除过期文件: {file}")
        except Exception as e:
            print(f"清理文件出错: {str(e)}")
