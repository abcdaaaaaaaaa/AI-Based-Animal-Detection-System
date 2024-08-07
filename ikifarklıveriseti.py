import os
import shutil

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def move_files(label_dir, image_dir, label1_dir, image1_dir, label2_dir, image2_dir, class1, class2):
    """
    label_dir: Orijinal etiket dosyalarının bulunduğu klasör.
    image_dir: Orijinal görüntü dosyalarının bulunduğu klasör.
    label1_dir: 0, 2 ve 4 sınıfları için etiket dosyalarının taşınacağı yeni klasör.
    image1_dir: 0, 2 ve 4 sınıfları için görüntü dosyalarının taşınacağı yeni klasör.
    label2_dir: 1 ve 3 sınıfları için etiket dosyalarının taşınacağı yeni klasör.
    image2_dir: 1 ve 3 sınıfları için görüntü dosyalarının taşınacağı yeni klasör.
    class1: Birinci sınıf grubuna dahil olan sınıf numaraları listesi. (Ör: [0, 2, 4])
    class2: İkinci sınıf grubuna dahil olan sınıf numaraları listesi. (Ör: [1, 3])
    """
    create_dir(label1_dir)
    create_dir(image1_dir)
    create_dir(label2_dir)
    create_dir(image2_dir)

    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
    total_files = len(label_files)
    print(f"Toplam etiket dosyası sayısı: {total_files}")

    class1_count = 0
    class2_count = 0

    for label_file in label_files:
        label_path = os.path.join(label_dir, label_file)
        image_path = os.path.join(image_dir, label_file.replace('.txt', '.jpg'))  # veya görüntü dosya uzantısına göre değiştirin

        if not os.path.exists(image_path):
            print(f"Uyarı: {image_path} bulunamadı.")
            continue

        with open(label_path, 'r') as f:
            lines = f.readlines()

        class1_lines = []
        class2_lines = []
        for line in lines:
            parts = line.strip().split()
            class_num = int(parts[0])
            if class_num in class1:
                class1_lines.append(line)
            elif class_num in class2:
                class2_lines.append(line)

        if class1_lines:
            new_label_path1 = os.path.join(label1_dir, label_file)
            new_image_path1 = os.path.join(image1_dir, label_file.replace('.txt', '.jpg'))
            with open(new_label_path1, 'w') as f:
                f.writelines(class1_lines)
            shutil.copy2(image_path, new_image_path1)
            class1_count += 1

        if class2_lines:
            new_label_path2 = os.path.join(label2_dir, label_file)
            new_image_path2 = os.path.join(image2_dir, label_file.replace('.txt', '.jpg'))
            with open(new_label_path2, 'w') as f:
                f.writelines(class2_lines)
            shutil.copy2(image_path, new_image_path2)
            class2_count += 1

    print(f"Sınıf 1 dosya sayısı (class1): {class1_count}")
    print(f"Sınıf 2 dosya sayısı (class2): {class2_count}")

# Klasör yolları ve sınıf numaraları
label_dir = 'labels'
image_dir = 'images'
label1_dir = 'labels1'
image1_dir = 'images1'
label2_dir = 'labels2'
image2_dir = 'images2'

class1 = [0, 2, 4]  # Birinci grup sınıf numaraları
class2 = [1, 3]     # İkinci grup sınıf numaraları

# Dosyaları taşıma
move_files(label_dir, image_dir, label1_dir, image1_dir, label2_dir, image2_dir, class1, class2)
