import os
from flask import Flask
from flask_cors import CORS


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化CORS
    CORS(app)

    # 确保音频目录存在
    os.makedirs(app.config['AUDIO_DIR'], exist_ok=True)

    # 注册蓝图
    from app.api import bp as api_bp
    from app.web import bp as web_bp

    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(web_bp)

    # 注册错误处理
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
