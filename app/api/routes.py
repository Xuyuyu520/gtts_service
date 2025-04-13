from flask import request, jsonify, current_app
from app.api import bp
from app.services.tts_service import TTSService
from app.api.schemas import TTSRequestSchema, VoiceResponseSchema


@bp.route('/voices', methods=['GET'])
def get_voices():
    """获取所有可用的语音列表"""
    voices = TTSService.list_voices()

    # 使用schema格式化响应
    schema = VoiceResponseSchema()
    return jsonify(schema.dump(voices))


@bp.route('/tts', methods=['POST'])
def generate_speech():
    """生成语音文件"""
    # 验证请求数据
    schema = TTSRequestSchema()
    errors = schema.validate(request.json)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    # 提取参数
    text = request.json.get('text')
    voice = request.json.get('voice', current_app.config['DEFAULT_VOICE'])
    rate = request.json.get('rate', '+0%')
    volume = request.json.get('volume', '+0%')
    pitch = request.json.get('pitch', '+0Hz')

    # 生成语音
    result = TTSService.generate_speech(text, voice, rate, volume, pitch)

    if result['success']:
        # 构建完整URL
        host_url = request.host_url.rstrip('/')
        result['url'] = f"{host_url}{result['file_path']}"
        return jsonify(result)
    else:
        return jsonify(result), 500


@bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'version': current_app.config['API_VERSION']
    })
