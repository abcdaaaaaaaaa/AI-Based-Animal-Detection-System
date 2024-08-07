import os

def find_multi_class_files(label_dir):
    """
    label_dir: Etiket dosyalarının bulunduğu klasör.
    """
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
    multi_class_files = []

    for label_file in label_files:
        label_path = os.path.join(label_dir, label_file)

        with open(label_path, 'r') as f:
            lines = f.readlines()

        classes = set()
        for line in lines:
            parts = line.strip().split()
            class_num = int(parts[0])
            classes.add(class_num)

        if len(classes) > 1:
            multi_class_files.append((label_file, list(classes)))

    return multi_class_files

# Klasör yolu
label_dir = 'labels'

# Birden fazla farklı sınıf içeren dosyaları bulma
multi_class_files = find_multi_class_files(label_dir)

# Sonuçları yazdırma
print("Birden fazla farklı sınıf içeren dosyalar:")
for label_file, classes in multi_class_files:
    print(f"{label_file}: Sınıflar - {classes}")
