import os

def rename_class_numbers(label_dir, class_mapping):
    """
    label_dir: Etiket dosyalarının bulunduğu klasör.
    class_mapping: Eski sınıf numaralarını yeni sınıf numaralarına dönüştürmek için bir sözlük.
                   Örneğin, {0: 0, 2: 1, 4: 2} sınıf 0'ı 0'a, 2'yi 1'e, 4'ü 2'ye dönüştürecektir.
    """
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

    for label_file in label_files:
        label_path = os.path.join(label_dir, label_file)

        with open(label_path, 'r') as f:
            lines = f.readlines()

        updated_lines = []
        for line in lines:
            parts = line.strip().split()
            class_num = int(parts[0])
            if class_num in class_mapping:
                parts[0] = str(class_mapping[class_num])
                updated_lines.append(' '.join(parts))

        with open(label_path, 'w') as f:
            f.writelines('\n'.join(updated_lines) + '\n')

# Klasör yolları ve sınıf dönüşümleri
label1_dir = 'labels1'
label2_dir = 'labels2'

# labels1 için sınıf dönüşümleri: 0 -> 0, 2 -> 1, 4 -> 2
class_mapping1 = {0: 0, 2: 1, 4: 2}

# labels2 için sınıf dönüşümleri: 1 -> 0, 3 -> 1
class_mapping2 = {1: 0, 3: 1}

# labels1 klasöründeki dosyaları yeniden adlandırma
rename_class_numbers(label1_dir, class_mapping1)

# labels2 klasöründeki dosyaları yeniden adlandırma
rename_class_numbers(label2_dir, class_mapping2)

print("Sınıf numaraları başarıyla yeniden adlandırıldı.")
