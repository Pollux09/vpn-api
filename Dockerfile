FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .
WORKDIR /app/app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6767", "--reload"]
