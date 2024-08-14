import csv
from datetime import datetime

# Nama file input
input_file = 'dlresult.csv'

# Mendapatkan tanggal dan waktu saat ini untuk nama file output
timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
output_file = f'output-{timestamp}.csv'

# Fungsi untuk memproses setiap baris dan memecah konten menjadi kolom
def process_lines(lines):
    data = []
    current_record = {
        'distributionList': '',
        'zimbraMailAlias': [],
        'zimbraMailForwardingAddress': [],
        'members': []
    }

    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            if any(current_record.values()):  # Simpan record sebelumnya jika ada
                data.append(current_record)
            # Inisialisasi record baru
            current_record = {
                'distributionList': '',
                'zimbraMailAlias': [],
                'zimbraMailForwardingAddress': [],
                'members': []
            }
            # Mengambil hanya alamat email dari baris distributionList
            if 'distributionList' in line:
                email_part = line.split(' ')[2]  # Mengambil email yang ada setelah 'distributionList'
                current_record['distributionList'] = email_part
        elif line.startswith('zimbraMailAlias:'):
            current_record['zimbraMailAlias'].append(line.split(': ', 1)[1])
        elif line.startswith('zimbraMailForwardingAddress:'):
            current_record['zimbraMailForwardingAddress'].append(line.split(': ', 1)[1])
        elif '@' in line:  # Anggap sebagai member
            current_record['members'].append(line)

    if any(current_record.values()):  # Simpan record terakhir jika ada
        data.append(current_record)

    return data

# Membaca file dan menghapus baris kosong
with open(input_file, 'r', newline='') as csvfile:
    lines = [line for line in csvfile if line.strip()]  # Hapus baris kosong

# Proses dan pisahkan konten menjadi kolom
processed_data = process_lines(lines)

# Menulis hasil ke file CSV
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['distributionList', 'zimbraMailAlias', 'zimbraMailForwardingAddress', 'members']
    writer = csv.writer(csvfile)
    
    # Menulis header
    writer.writerow(fieldnames)
    
    # Menulis data
    for record in processed_data:
        max_len = max(len(record['zimbraMailAlias']), len(record['zimbraMailForwardingAddress']), len(record['members']))
        
        for i in range(max_len):
            writer.writerow([
                record['distributionList'] if i == 0 else '',  # Tulis hanya di baris pertama
                record['zimbraMailAlias'][i] if i < len(record['zimbraMailAlias']) else '',
                record['zimbraMailForwardingAddress'][i] if i < len(record['zimbraMailForwardingAddress']) else '',
                record['members'][i] if i < len(record['members']) else ''
            ])

print(f"Pemisahan selesai! File baru disimpan sebagai '{output_file}'.")
