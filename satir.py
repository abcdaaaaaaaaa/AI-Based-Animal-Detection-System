import os

def count_total_lines_in_txt_files():
    folder_path = os.getcwd()
    total_lines = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                total_lines += sum(1 for line in file)
    
    return total_lines

if __name__ == "__main__":
    total_lines = count_total_lines_in_txt_files()
    print(f"Toplam satır sayısı: {total_lines}")
