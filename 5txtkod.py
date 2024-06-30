import os
import pandas as pd
from PIL import Image

def convert_coordinates_to_yolo(xmin, ymin, xmax, ymax, img_width, img_height):
    x_center = round(((xmin + xmax + img_width) / 2) / img_width, 6)
    y_center = round(((ymin + ymax + img_height) / 2) / img_height, 6)
    width = round((xmax - xmin) / img_width, 6)
    height = round((ymax - ymin) / img_height, 6)
    return x_center, y_center, width, height

def get_class_id(etiket_adi, birads):
    if etiket_adi == "Mass":
        if birads == 2:
            return 0  # M2
        elif birads == 4:
            return 2  # M4
        elif birads == 5:
            return 4  # M5
    elif etiket_adi == "Calcification":
        if birads == 4:
            return 1  # C4
        elif birads == 5:
            return 3  # C5
    return -1  # Tanınmayan sınıf

# CSV dosyasını oku
csv_file = 'veribilgisi3.csv'
data = pd.read_csv(csv_file, delimiter=';')

# Etiketleri ve dosya yollarını al
unique_files = data['DOSYA ADI'].unique()

for file in unique_files:
    # Aynı dosya adı için tüm satırları al
    file_data = data[data['DOSYA ADI'] == file]

  # Görüntü dosyasının varlığını kontrol et
    img_path = os.path.join(os.getcwd(), file)
    if not os.path.exists(img_path):
        continue
    
    # Görüntü boyutlarını oku
    with Image.open(img_path) as img:
        img_width, img_height = img.size
    
    # Dosyanın sınıf adını ve koordinatlarını al
    for index, row in file_data.iterrows():
        etiket_adi = row['ETİKET ADI']
        birads = int(row['BIRADS'][6:])  # BIRADS numarasını al (örneğin: "BIRADS2" -> 2)
        adjusted_coords = [tuple(map(float, coord.split(','))) for coord in row['ETİKET KOORDİNATLARI'].replace('"', '').split(';')]
        
        # Koordinatları parse et
        x1, y1 = adjusted_coords[0]
        x2, y2 = adjusted_coords[2]  # Sağ alt köşe

        if(x1 >= x2):
            xmax = x1
            xmin = x2
        elif(x1 < x2):
            xmax = x2
            xmin = x1
            
        if(y1 >= y2):
            ymax = y1
            ymin = y2
        elif(x1 < x2):
            ymax = y2
            ymin = y1
        
        # YOLO formatına dönüştür
        x_center, y_center, width, height = convert_coordinates_to_yolo(xmin, ymin, xmax, ymax, img_width, img_height)
        
        # Class ID'yi belirle
        class_id = get_class_id(etiket_adi, birads)
        
        # TXT dosyasının yolunu oluştur
        txt_file_path = os.path.splitext(file)[0] + '.txt'
        
        # TXT dosyasına yaz
        with open(txt_file_path, 'a') as f:
            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

print("Process completed.")
