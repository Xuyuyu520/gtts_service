from marshmallow import Schema, fields, validate

class TTSRequestSchema(Schema):
    """TTS请求参数验证"""
    text = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    voice = fields.String(required=False)
    # gTTS不支持这些参数，但保留以保持API兼容性
    rate = fields.String(required=False)
    volume = fields.String(required=False)
    pitch = fields.String(required=False)

class VoiceSchema(Schema):
    """语音信息"""
    ShortName = fields.String()
    DisplayName = fields.String()
    Gender = fields.String()

class VoiceResponseSchema(Schema):
    """语音列表响应"""
    zh = fields.List(fields.Nested(VoiceSchema))
    en = fields.List(fields.Nested(VoiceSchema))
    other = fields.List(fields.Nested(VoiceSchema))
