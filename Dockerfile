FROM python:3.12-slim-bookworm

RUN pip install uv

WORKDIR /app

COPY src requirements.lock pyproject.toml README.md ./
RUN uv pip install --no-cache --system -r requirements.lock

EXPOSE 8000
CMD ["fastapi", "run", "src/dst_py/main.py", "--port", "8000"]
