from PIL import Image
import os

def siyah_mi_beyaz_mi(goruntu_yolu):
    
    img = Image.open(goruntu_yolu).convert('RGB')  # Renkli olarak aç

    pikseller = img.getdata()    
    # Siyah ve beyaz piksel sayacı
    siyah_sayac = 0
    beyaz_sayac = 0
    
    # Pikselleri incele
    for piksel in pikseller:
        if piksel == (0, 0, 0):
            siyah_sayac += 1
        elif piksel == (255, 255, 255):
            beyaz_sayac += 1

    # Sonuçları karşılaştır
    if siyah_sayac < beyaz_sayac:
        return 1  # Beyaz piksel sayısı siyahdan az ise 1 döndür
    elif beyaz_sayac < siyah_sayac:
        return 0  # Beyaz piksel sayısı siyahdan fazla veya eşitse 0 döndür

def beyaz_piksel_ekle(img, genislik_farki, saga_ekle):
    # Görüntünün genişliğini ve yüksekliğini al
    width, height = img.size
    
    # Sağa ekleme yapacaksa
    if saga_ekle:
        yeni_goruntu = Image.new('RGB', (width + genislik_farki, height))
        yeni_goruntu.paste(img, (0, 0))
        yeni_goruntu.paste(Image.new('RGB', (genislik_farki, height), renk), (width, 0))
    else:  # Sola ekleme yapacaksa
        yeni_goruntu = Image.new('RGB', (width + genislik_farki, height))
        yeni_goruntu.paste(img, (genislik_farki, 0))  # Burada sola ekliyoruz
        yeni_goruntu.paste(Image.new('RGB', (genislik_farki, height), renk), (0, 0))

    return yeni_goruntu
    
def sagda_mi(goruntu_yolu):
    # Görüntüyü yükle
    img = Image.open(goruntu_yolu)
    
    # Görüntünün genişliğini ve yüksekliğini al
    width, height = img.size

    # Piksel değerlerini hesapla
    sag_kenar_pikselleri = sum(img.getdata()[i * width - width] for i in range(1, height + 1))  # Sağ kenar piksel değerleri
    sol_kenar_pikselleri = sum(img.getdata()[(i * width) - 1] for i in range(1, height + 1))  # Sol kenar piksel değerleri

    # Eğer sağ kenardaki piksel değerleri, sol kenardaki piksel değerlerinden büyükse, görüntü sağdadır
    return sag_kenar_pikselleri > sol_kenar_pikselleri

def ortala_meme(mamografi_yolu):
    # Mamografi görüntüsünü yükle
    img = Image.open(mamografi_yolu)

    # Görüntünün genişliğini ve yüksekliğini al
    width, height = img.size

    # Meme genişliği
    meme_genislik = width // 2

    # Sağ memenin sol başlangıç ve bitiş noktaları
    sag_baslangic = meme_genislik
    sag_bitis = width

    # Sol memenin sol başlangıç ve bitiş noktaları
    sol_baslangic = 0
    sol_bitis = meme_genislik

    # Sağ ve sol memeleri al
    sag_meme = img.crop((sag_baslangic, 0, sag_bitis, height))
    sol_meme = img.crop((sol_baslangic, 0, sol_bitis, height))

    return sag_meme, sol_meme, width, height

def kare_yap(img):
    width, height = img.size  # Görüntünün genişliğini ve yüksekliğini al
    
    if width > height:
        fark = width - height
        yeni_yukseklik = height + fark
        yeni_goruntu = Image.new('RGB', (width, yeni_yukseklik), renk)
        yeni_goruntu.paste(img, (0, fark // 2))
    elif height > width:
        fark = height - width
        yeni_genislik = width + fark
        yeni_goruntu = Image.new('RGB', (yeni_genislik, height), renk)
        yeni_goruntu.paste(img, (fark // 2, 0))
    
    return yeni_goruntu

# Mevcut çalışma dizinindeki mamografi dosyalarını işle
for dosya in os.listdir():
    if dosya.endswith(".jpg"):  # Sadece jpg uzantılı dosyaları işle
        mamografi_dosyasi = os.path.join(os.getcwd(), dosya)

        sag_meme, sol_meme, genislik, yukseklik = ortala_meme(mamografi_dosyasi)
            
        if siyah_mi_beyaz_mi(mamografi_dosyasi) == 1:
           renk = (255, 255, 255)
           if sagda_mi(mamografi_dosyasi):
              kaydirma_miktari = genislik - sag_meme.width
              print(f"{dosya} görüntüsü sağda.")
              saga_ekle = True  # Sağda ise sağa ekleme yapacak şekilde ayarlıyoruz
           else:
              kaydirma_miktari = genislik - sol_meme.width
              print(f"{dosya} görüntüsü solda.")
              saga_ekle = False  # Solda ise sola ekleme yapacak şekilde ayarlıyoruz
        elif siyah_mi_beyaz_mi(mamografi_dosyasi) == 0:
           renk = (0, 0, 0)
           if sagda_mi(mamografi_dosyasi):
              kaydirma_miktari = genislik - sol_meme.width
              print(f"{dosya} görüntüsü solda.")
              saga_ekle = False  # Sağda ise sağa ekleme yapacak şekilde ayarlıyoruz
           else:
              kaydirma_miktari = genislik - sag_meme.width
              print(f"{dosya} görüntüsü sağda.")
              saga_ekle = True  # Solda ise sola ekleme yapacak şekilde ayarlıyoruz
        
        # Görüntüyü yükle
        img = Image.open(mamografi_dosyasi)
        yeni_goruntu = beyaz_piksel_ekle(img, kaydirma_miktari, saga_ekle)
        
        # Kare yap
        yeni_goruntu = kare_yap(yeni_goruntu)
        
        # Sonuçları kaydet
        yeni_goruntu.save(dosya)

    





