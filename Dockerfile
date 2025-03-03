# 使用官方 Python 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器内的 /app 目录
COPY . /app

# 安装项目的依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 默认的端口
EXPOSE 5000

# 设置环境变量，告诉 Flask 在开发环境中运行
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# 定义容器启动时执行的命令
CMD ["flask", "run", "--host=0.0.0.0"]
