FROM python:3.9-slim

# Menyiapkan direktori kerja
WORKDIR /app

# Menyalin file requirements dan menginstalnya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode ke dalam container
COPY . .

# Membuka port 7860 sesuai aturan Hugging Face
EXPOSE 7860

# Menjalankan aplikasi
CMD ["python", "app.py"]