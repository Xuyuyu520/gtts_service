from flask import render_template, request, jsonify, current_app, url_for
from app.web import bp
from app.services.tts_service import TTSService


@bp.route('/', methods=['GET'])
def index():
    """首页"""
    # 获取可用语音列表
    voices = TTSService.list_voices()

    # 清理旧文件
    TTSService.clean_old_files()

    return render_template('index.html',
                           title='gTTS 语音合成服务',
                           voices=voices)


@bp.route('/generate', methods=['POST'])
def generate_speech():
    """Web界面的语音生成处理"""
    text = request.form.get('text')
    voice = request.form.get('voice', current_app.config['DEFAULT_VOICE'])
    rate = request.form.get('rate', '+0%')
    volume = request.form.get('volume', '+0%')
    pitch = request.form.get('pitch', '+0Hz')

    if not text:
        return jsonify({'success': False, 'error': '文本不能为空'})

    # 生成语音
    result = TTSService.generate_speech(text, voice, rate, volume, pitch)
    return jsonify(result)


@bp.route('/docs', methods=['GET'])
def docs():
    """API文档页面"""
    return render_template('docs.html',
                           title='API文档 - gTTS 语音合成服务',
                           api_version=current_app.config['API_VERSION'])


@bp.route('/about', methods=['GET'])
def about():
    """关于页面"""
    return render_template('about.html',
                           title='关于 - gTTS 语音合成服务')
