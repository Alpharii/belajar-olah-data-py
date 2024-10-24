# Import library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt

# Membaca file Excel
file_path = 'Data_Bintang.xlsx'
excel_data = pd.ExcelFile(file_path)

# Memilih sheet yang ingin dianalisis
sensor_data = excel_data.parse('sensor_data_speed_2')

# Pembersihan data: Menghapus baris dengan nilai kosong pada kolom sensor_2_value
sensor_data_cleaned = sensor_data.dropna(subset=['sensor_2_value'])

# Membuat plot garis untuk sensor_2_value dari waktu ke waktu
plt.figure(figsize=(10,6))
plt.plot(sensor_data_cleaned['date'], sensor_data_cleaned['sensor_2_value'], marker='o')
plt.title('Nilai Kecepatan Sensor 2 dari Waktu ke Waktu')
plt.xlabel('Waktu')
plt.ylabel('Nilai Kecepatan')
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
print()

# Menghitung rata-rata kecepatan sensor 2
average_speed = sensor_data_cleaned['sensor_2_value'].mean()
print(f"Rata-rata kecepatan truk container dalam satu bulan: {average_speed:.2f}")
print()
# Visualisasi rata-rata kecepatan
plt.figure(figsize=(6, 4))
plt.bar(['Rata-rata Kecepatan'], [round(average_speed, 2)], color='skyblue')  # Membulatkan ke 2 desimal
plt.title('Rata-rata Kecepatan Truk Container')
plt.ylabel('Kecepatan (unit yang digunakan)')
plt.ylim(0, round(average_speed + 5, 2))  # Mengatur batas atas agar ada ruang
plt.grid(axis='y')
# Menampilkan nilai di atas batang (angka rata-rata)
for i, v in enumerate([round(average_speed, 2)]):
    plt.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
plt.show()

# Menghitung jumlah data kosong pada sensor 2
missing_data_count = sensor_data['sensor_2_value'].isna().sum()
print(f"Total data sensor 2 yang kosong: {missing_data_count}")
print()
# Diagram batang untuk data yang hilang
plt.figure(figsize=(10, 5))
plt.bar(['Total Data Kosong'], [missing_data_count], color='red')
plt.title('Jumlah Data Sensor 2 yang Kosong')
plt.ylabel('Jumlah Data Kosong')
plt.grid(axis='y')
plt.show()

# Kecepatan terendah dan tertinggi dari sensor 2
min_speed = sensor_data_cleaned['sensor_2_value'].min()
max_speed = sensor_data_cleaned['sensor_2_value'].max()
print(f"Kecepatan terendah truk: {min_speed}")
print(f"Kecepatan tertinggi truk: {max_speed}")
print()
# Diagram batang untuk kecepatan terendah dan tertinggi
plt.figure(figsize=(10, 5))
plt.bar(['Kecepatan Terendah', 'Kecepatan Tertinggi'], [min_speed, max_speed], color=['blue', 'green'])
plt.title('Kecepatan Truk')
plt.ylabel('Kecepatan (unit yang digunakan)')
plt.grid(axis='y')
plt.show()

# Menghitung jumlah gangguan per tanggal
sensor_data['date'] = pd.to_datetime(sensor_data['date'])  # Pastikan kolom tanggal dalam format datetime
sensor_errors_by_date = sensor_data[sensor_data['sensor_2_value'].isna()]['date'].dt.date.value_counts()
# Menampilkan tanggal dengan gangguan terbanyak
most_errors_date = sensor_errors_by_date.idxmax()
most_errors_count = sensor_errors_by_date.max()
print(f"Tanggal dengan gangguan terbanyak: {most_errors_date}, dengan total gangguan: {most_errors_count}")
print()
plt.figure(figsize=(12, 6))
sensor_errors_by_date.sort_index().plot(kind='bar', color='orange')
plt.title('Jumlah Gangguan Sensor 2 Berdasarkan Tanggal')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Gangguan')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# Menambahkan kolom minggu pada data
sensor_data['week'] = sensor_data['date'].dt.isocalendar().week
# Menghitung jumlah gangguan per minggu
sensor_errors_by_week = sensor_data[sensor_data['sensor_2_value'].isna()]['week'].value_counts().sort_index()
print("Jumlah gangguan sensor 2 berdasarkan minggu:")
print(sensor_errors_by_week)
print()
# Menampilkan minggu dengan gangguan terbanyak
sensor_errors_by_week.plot(kind='bar', title='Jumlah Gangguan Sensor 2 per Minggu')
plt.xlabel('Minggu')
plt.ylabel('Jumlah Gangguan')
plt.show()

# Menghitung durasi waktu di mana sensor 2 tidak berfungsi (data kosong berturut-turut)
sensor_data['gap'] = sensor_data['sensor_2_value'].isna() & sensor_data['sensor_2_value'].shift().notna()
# Menghitung total gangguan dalam jam atau hari
total_gangguan = sensor_data['gap'].sum()
print(f"Total durasi waktu gangguan sensor 2: {total_gangguan} kali berturut-turut.")

