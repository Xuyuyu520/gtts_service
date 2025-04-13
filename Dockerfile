FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV HOST=0.0.0.0
ENV PORT=5000
ENV DEBUG=False
ENV AUDIO_RETENTION_HOURS=24

# 创建音频目录
RUN mkdir -p app/static/audio && chmod 777 app/static/audio

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
