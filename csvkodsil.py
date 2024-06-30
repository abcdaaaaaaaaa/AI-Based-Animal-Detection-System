import os
import pandas as pd

# CSV dosyasını oku
csv_file = 'veribilgisi3.csv'
data = pd.read_csv(csv_file, delimiter=';')

# İlgili sütunları al
birads_column = 'BIRADS'
filename_column = 'DOSYA ADI'

# Dosya adlarını listele
file_groups = data.groupby(birads_column)[filename_column].apply(list).to_dict()

# Mevcut çalışma dizini
current_dir = os.getcwd()

# Klasörlerdeki dosyaları kontrol et ve sil
for birads, files in file_groups.items():
    folder_path = os.path.join(current_dir, birads)
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename not in files:
                file_path = os.path.join(folder_path, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

print("Process completed.")
