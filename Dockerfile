FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPYCACHEPREFIX=/tmp/pycache \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-spa && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd --system openscan && \
    useradd --system --gid openscan --create-home openscan

COPY . /app
RUN python -m pip install --no-cache-dir '.[web]' && \
    chown -R openscan:openscan /app

USER openscan
EXPOSE 10000

# Render supplies PORT=10000; the fallback also allows local Docker testing.
CMD ["sh", "-c", "exec streamlit run app/streamlit_app.py --server.address=0.0.0.0 --server.port=${PORT:-10000} --server.headless=true --browser.gatherUsageStats=false"]
