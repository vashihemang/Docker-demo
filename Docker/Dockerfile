# base image 
FROM python:3.10-slim

# workingdir 
WORKDIR /docker_demo

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# copy requriments.txt file 
COPY requirements.txt .

# run 
RUN pip install --no-cache-dir -r requirements.txt

# copy 
COPY docker_demo.py .

# port
EXPOSE 8000

# command 
CMD ["uvicorn", "docker_demo:app", "--host", "0.0.0.0", "--port", "8000"]