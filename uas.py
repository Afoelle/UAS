import pwinput
import csv
import os
from prettytable import PrettyTable
from datetime import datetime
import pyfiglet
import time

simbol  = [  
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", 
    "{", "}", "[", "]", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "|", "~", " "
]

angka = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pilihan(nama):
	role = None
	try:
		with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["nama"].lower() == nama.lower():
					role = row["role"]
					break
	except FileNotFoundError:
		print("File tidak ditemukan.")	
	if role == "biasa":
		menu_biasa(nama)
	if role == "vip":
		menu_vip(nama)
	else:
		print("role tidak ditemukan, kembali ke menu login")
		menu_login()

def cek_nama(nama):
	akun = nama.lower()
	try:
		with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["nama"].lower() == akun:
					return True
			return False
	except FileNotFoundError:
		print("File tidak ditemukan")

def simpan_akun(nama, password):
	data_header = ["nama", "password", "role", "saldo", "voucher", "akun"]
	data_akun = [{
		"nama": nama, "password": password, "role": "biasa", "saldo": 0, "voucher":["diskon 5", "diskon 10"], "akun": "buka"
	}]
	try:
		with open("akun.csv", mode="a", newline="", encoding="utf-8") as file:
			writer = csv.DictWriter(file, fieldnames=data_header)
			file.seek(0,2)
			if file.tell() == 0:
				writer.writeheader()
			writer.writerows(data_akun)
		print("data berhasil disimpan, kembali ke menu login...")
		time.sleep(3)
		menu_login()
	except FileNotFoundError:
		print("File tidak ditemukan")

def register():
	clear()
	print(pyfiglet.figlet_format("REGISTER", font="slant"))
	while True:
		nama = input("Masukan nama: ").strip()
		if any(char in simbol for char in nama) or any (char in angka for char in nama):
			print("Nama tidak boleh dispasi atau mengandung simbol atau angka.")
			continue
		if cek_nama(nama):
			print("Nama sudah digunakan silahkan ganti nama lain.")
			continue
		if nama == "":
			print("Nama tidak boleh kosong.")
			continue
		password = pwinput.pwinput("Masukan password: ").strip()
		simpan_akun(nama, password)

def cek_role(nama, password):
	try:
		with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["nama"].lower() == nama.lower() and row["password"] == password:
					return row["role"]
			return None
	except FileNotFoundError:
		print("File tidak ditemukan")

def cek_role_beli(nama):
	try:
		with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["nama"] == nama:
					return row["role"]
			return None
	except FileNotFoundError:
		print("File tidak ditemukan")

def kunci(nama):
    try:
        with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data_akun = list(reader)
    except FileNotFoundError:
        print("File tidak ditemukan")

    try:
        with open("akun.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["nama", "password", "role", "saldo", "voucher", "akun"])
            writer.writeheader()
            for row in data_akun:
                if row["nama"].lower() == nama.lower():
                    row["akun"] = "kunci"
                    print("\n╔═══════════════════════════════════════════════╗")
                    print("║   Kesempatan anda habis akun anda terkunci    ║")           
                    print("╚═══════════════════════════════════════════════╝")
                writer.writerow(row)
    except FileNotFoundError:
        print("File tidak ditemukan")

def cek_akun_terkunci(nama):
    try:
        with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["nama"].lower() == nama.lower():
                    return row["akun"]
            return None  
    except FileNotFoundError:
        print("File tidak ditemukan")


def menu_kunci(nama):
    print("\n╔═══════════════════════════════╗")
    print("║  Apakah anda ingin membuka    ║")
    print("║         akun anda?            ║")
    print("╠═══════════════════════════════╣")
    print("║ [Y] Buka dengan menunggu 5s   ║")
    print("║ [N] Kembali ke menu login     ║")
    print("╚═══════════════════════════════╝")
    
    pil = input("Masukan pilihan anda: ").lower()
    
    if pil == "y":
        print("Silahkan menunggu 5 detik....")
        time.sleep(5)

        try:
            with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                data_akun = list(reader)
                fieldnames = reader.fieldnames
            
            for row in data_akun:
                if row["nama"].lower() == nama.lower():
                    row["akun"] = "buka"
            
            with open("akun.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_akun)
                
            print("\n╔═══════════════════╗")
            print("║   AKUN TERBUKA    ║")           
            print("╚═══════════════════╝")
            print("\nKembali ke menu login...")
            time.sleep(1)
            menu_login()
                
        except FileNotFoundError:
            print("File tidak ditemukan")
            menu_login()
            
    elif pil == "n":
        print("Kembali ke menu login..")
        time.sleep(1)
        menu_login()
    else:
        print("Pilihan tidak valid!")
        menu_kunci(nama)

def login():
	clear()
	kesempatan = 3
	print(pyfiglet.figlet_format("LOGIN", font="slant"))
	while True:
		nama = input("Masukan nama: ")
		password = pwinput.pwinput("Masukan password: ")

		role = cek_role(nama, password)
		akun = cek_akun_terkunci(nama)
        
		if akun == "kunci":
			menu_kunci(nama)
		elif akun == "buka" and role == "biasa":
			clear()
			print(pyfiglet.figlet_format("SEDANG LOGIN ."))
			print("                        0  ")
			print("                        |  ")
			print("                     ___|__")
			print("                     |/\/\/")
			print("                 0   |     ")
			print("                 |   |/\/\/")
			print("                _|___|_____")
			print("               |/\/\/\/\/\/")
			print("               |           ")
			print("               |           ")
			print("               | ~ ~ ~ ~ ~ ")
			print("               |___________")
			time.sleep(1)
			clear()
			print(pyfiglet.figlet_format("SEDANG LOGIN . ."))
			print("                               0   0")
			print("                               |   |")
			print("                           ____|___|")
			print("                        0  |~ ~ ~ ~ ")
			print("                        |  |        ")
			print("                     ___|__|________")
			print("                     |/\/\/\/\/\/\/")
			print("                 0   |             ")
			print("                 |   |/\/\/\/\/\/\/")
			print("                _|___|_____________")
			print("               |/\/\/\/\/\/\/\/\/\/")
			print("               |                   ")
			print("               |                   ")
			print("               | ~ ~ ~ ~ ~ ~ ~ ~ ~ ")
			print("               |___________________")
			time.sleep(1)
			clear()
			print(pyfiglet.figlet_format("SEDANG LOGIN . . ."))
			print("                               0   0")
			print("                               |   |")
			print("                           ____|___|____")
			print("                        0  |~ ~ ~ ~ ~ ~|   0")
			print("                        |  |           |   |")
			print("                     ___|__|___________|___|__")
			print("                     |/\/\/\/\/\/\/\/\/\/\/\/|")
			print("                 0   |                       |   0")
			print("                 |   |/\/\/\/\/\/\/\/\/\/\/\/|   |")
			print("                _|___|_______________________|___|__")
			print("               |/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/|")
			print("               |                                   |")
			print("               |                                   |")
			print("               | ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |")
			print("               |___________________________________|")
			time.sleep(1)
			menu_biasa(nama)

		elif akun == "buka" and role == "vip":
			clear()
			print(pyfiglet.figlet_format("SEDANG LOGIN ."))
			print("                        0  ")
			print("                        |  ")
			print("                     ___|__")
			print("                     |/\/\/")
			print("                 0   |     ")
			print("                 |   |/\/\/")
			print("                _|___|_____")
			print("               |/\/\/\/\/\/")
			print("               |           ")
			print("               |           ")
			print("               | ~ ~ ~ ~ ~ ")
			print("               |___________")
			time.sleep(1)
			clear()
			print(pyfiglet.figlet_format("SEDANG LOGIN . ."))
			print("                               0   0")
			print("                               |   |")
			print("                           ____|___|")
			print("                        0  |~ ~ ~ ~ ")
			print("                        |  |        ")
			print("                     ___|__|________")
			print("                     |/\/\/\/\/\/\/")
			print("                 0   |             ")
			print("                 |   |/\/\/\/\/\/\/")
			print("                _|___|_____________")
			print("               |/\/\/\/\/\/\/\/\/\/")
			print("               |                   ")
			print("               |                   ")
			print("               | ~ ~ ~ ~ ~ ~ ~ ~ ~ ")
			print("               |___________________")
			time.sleep(1)
			clear()
			print(pyfiglet.figlet_format("SEDANG LOGIN . . ."))
			print("                               0   0")
			print("                               |   |")
			print("                           ____|___|____")
			print("                        0  |~ ~ ~ ~ ~ ~|   0")
			print("                        |  |           |   |")
			print("                     ___|__|___________|___|__")
			print("                     |/\/\/\/\/\/\/\/\/\/\/\/|")
			print("                 0   |                       |   0")
			print("                 |   |/\/\/\/\/\/\/\/\/\/\/\/|   |")
			print("                _|___|_______________________|___|__")
			print("               |/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/|")
			print("               |                                   |")
			print("               |                                   |")
			print("               | ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |")
			print("               |___________________________________|")
			time.sleep(1)
			menu_vip(nama)
		else:
			kesempatan -= 1
			print(f"Nama atau password salah, kesempatan tersisa {kesempatan}.")
			if kesempatan == 0:
				kunci(nama)
				print("Kembali ke menu login...")
				time.sleep(3)
				menu_login()
			continue

def lihat_semua():
	print(pyfiglet.figlet_format("SEMUA", font="slant"))
	tabel = PrettyTable(["ID", "NAMA", "JENIS", "HARGA", "STOK"])
	try:
		with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				format = format_nominal(float(row["harga"]))
				tabel.add_row([row["id"], row["nama"], row["jenis"],format, row["stok"]])
			print(tabel)
	except FileNotFoundError:
		print("File tidak ditemukan")

def lihat_brownies():
	print(pyfiglet.figlet_format("BROWNIES", font="slant"))
	tabel = PrettyTable(["ID", "NAMA", "JENIS", "HARGA", "STOK"])
	try:
		with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["jenis"].lower() == "brownies":
					format = format_nominal(float(row["harga"]))
					tabel.add_row([row["id"], row["nama"], row["jenis"],format, row["stok"]])
			print(tabel)
	except FileNotFoundError:
		print("File tidak ditemukan")

def lihat_pastry():
	print(pyfiglet.figlet_format("PASTRY", font="slant"))
	tabel = PrettyTable(["ID", "NAMA", "JENIS", "HARGA", "STOK"])
	try:
		with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["jenis"].lower() == "pastry":
					format = format_nominal(float(row["harga"]))
					tabel.add_row([row["id"], row["nama"], row["jenis"],format, row["stok"]])
			print(tabel)
	except FileNotFoundError:
		print("File tidak ditemukan")

def lihat_bolu():
	print(pyfiglet.figlet_format("BOLU", font="slant"))
	tabel = PrettyTable(["ID", "NAMA", "JENIS", "HARGA", "STOK"])
	try:
		with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["jenis"].lower() == "bolu":
					format = format_nominal(float(row["harga"]))
					tabel.add_row([row["id"], row["nama"], row["jenis"],format, row["stok"]])
			print(tabel)
	except FileNotFoundError:
		print("File tidak ditemukan")

def lihat_premium():
	print(pyfiglet.figlet_format("PREMIUM PRODUCT", font="slant"))
	tabel = PrettyTable(["ID", "NAMA", "JENIS", "HARGA", "STOK"])
	try:
		with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["jenis"].lower() == "premium product":
					format = format_nominal(float(row["harga"]))
					tabel.add_row([row["id"], row["nama"], row["jenis"],format, row["stok"]])
			print(tabel)
	except FileNotFoundError:
		print("File tidak ditemukan")

def lihat_seasonal():
	print(pyfiglet.figlet_format("SEASONAL PRODUCT", font="slant"))
	tabel = PrettyTable(["ID", "NAMA", "JENIS", "HARGA", "STOK"])
	try:
		with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["jenis"].lower() == "seasonal product":
					format = format_nominal(float(row["harga"]))
					tabel.add_row([row["id"], row["nama"], row["jenis"],format, row["stok"]])
			print(tabel)
	except FileNotFoundError:
		print("File tidak ditemukan")

def lihat_timed(nama):
    clear()
    current_time = datetime.now().time()
    current_hour = current_time.hour
    
    print(pyfiglet.figlet_format("TIMED MENU"))
    print(f"\nWaktu saat ini: {current_time.strftime('%H:%M')}")
    
    if 7 <= current_hour < 12:
        print("\nBREAKFAST MENU (07:00 - 12:00)")
        print("═" * 45)
        tabel = PrettyTable(["ID", "NAMA", "HARGA", "STOK"])
        tabel.add_row([43, "Breakfast Set", "Rp. 75.000", 10])
        tabel.add_row([44, "Morning Pastry", "Rp. 65.000", 15])
        tabel.add_row([45, "Fruit Parfait", "Rp. 45.000", 20])
        
    elif 12 <= current_hour < 19:
        print("\nLUNCH & TEA MENU (12:00 - 19:00)")
        print("═" * 45)
        tabel = PrettyTable(["ID", "NAMA", "HARGA", "STOK"])
        tabel.add_row([46, "Lunch Box", "Rp. 85.000", 12])
        tabel.add_row([47, "Tea Time Set", "Rp. 95.000", 8])
        tabel.add_row([48, "Savory Box", "Rp. 70.000", 15])
        
    elif 19 <= current_hour < 24:
        print("\nEVENING MENU (19:00 - 24:00)")
        print("═" * 45)
        tabel = PrettyTable(["ID", "NAMA", "HARGA", "STOK"])
        tabel.add_row([49, "Dessert Box", "Rp. 90.000", 10])
        tabel.add_row([50, "Evening Set", "Rp. 75.000", 12])
        tabel.add_row([51, "Sweet Box", "Rp. 80.000", 8])
        
    else:
        print("\nToko tutup!")
        print("Jam operasional:")
        print("Breakfast : 07:00 - 12:00")
        print("Lunch&Tea : 12:00 - 19:00")
        print("Evening   : 19:00 - 24:00")
        input("\nTekan Enter untuk kembali...")
        return
    
    print(tabel)
    print("\n1. Beli")
    print("0. Kembali")
    
    while True:
        pilihan = input("\nPilihan: ")
        if pilihan == "1":
            beli(nama)
            break
        elif pilihan == "0":
            menu_beli(nama)
            break
        else:
            print("Pilihan tidak valid!")

def get_timed_product(id):
    current_hour = datetime.now().hour
    
    breakfast_products = {
        43: {"nama": "Breakfast Set", "harga": 75000, "stok": 10},
        44: {"nama": "Morning Pastry", "harga": 65000, "stok": 15},
        45: {"nama": "Fruit Parfait", "harga": 45000, "stok": 20}
    }
    
    lunch_products = {
        46: {"nama": "Lunch Box", "harga": 85000, "stok": 12},
        47: {"nama": "Tea Time Set", "harga": 95000, "stok": 8},
        48: {"nama": "Savory Box", "harga": 70000, "stok": 15}
    }
    
    evening_products = {
        49: {"nama": "Dessert Box", "harga": 90000, "stok": 10},
        50: {"nama": "Evening Set", "harga": 75000, "stok": 12},
        51: {"nama": "Sweet Box", "harga": 80000, "stok": 8}
    }
    
    if 7 <= current_hour < 12:
        return breakfast_products.get(id)
    elif 12 <= current_hour < 19:
        return lunch_products.get(id)
    elif 19 <= current_hour < 24:
        return evening_products.get(id)
    return None

def cek_id(id):
	try:
		with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if int(row["id"]) == id:
					return False
			return True
	except FileNotFoundError:
		print("File tidak ditemukan")
		return True

def beli(nama):
    while True:
        id_input = input("Masukan id yang ingin dibeli (ketik 0 untuk kembali): ")
        if id_input == "0":
            menu_beli(nama)
            return
        
        qty_input = input("Masukan jumlah yang ingin dibeli: ")

        if id_input == "" or qty_input == "":
            print("tidak boleh kosong.")
            continue
        
        try:
            id = int(id_input)
            qty = int(qty_input)
        except ValueError:
            print("id dan jumlah harus berupa angka")
            continue

        timed_product = get_timed_product(id)
        if timed_product:
            if qty > timed_product["stok"]:
                print(f"Stok tidak mencukupi. Stok tersedia: {timed_product['stok']}")
                continue
                
            data_kue = {
                "nama": nama,
                "id kue": id,
                "nama kue": timed_product["nama"],
                "jumlah": qty,
                "harga": timed_product["harga"],
                "jenis": "Timed Product"
            }
            
            keranjang = []
            try:
                with open("keranjang.csv", mode="r", newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    updated = False
                    for row in reader:
                        if row["nama"] == nama and int(row["id kue"]) == id:
                            row["jumlah"] = str(int(row["jumlah"]) + qty)
                            updated = True
                        keranjang.append(row)
                    
                    if not updated:
                        keranjang.append(data_kue)
                        
            except FileNotFoundError:
                keranjang.append(data_kue)

            try:
                with open("keranjang.csv", mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["nama", "id kue", "nama kue", "jumlah", "harga", "jenis"])
                    writer.writeheader()
                    writer.writerows(keranjang)
                print(f"\nBerhasil menambahkan {qty} {timed_product['nama']} ke keranjang")
                print("Anda akan dikembalikan ke menu utama...")
                time.sleep(3)
                pilihan(nama)
                return
            except Exception as e:
                print(f"Terjadi kesalahan: {str(e)}")
                continue

        try:
            with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                item_found = False
                for row in reader:
                    if int(row["id"]) == id:
                        item_found = True
                        nama_kue = row["nama"]
                        harga = int(row["harga"])
                        jenis = row["jenis"]
                        stok = int(row["stok"])
                        break
                
                if not item_found:
                    print("Barang tidak ditemukan")
                    continue
                    
                if qty > stok:
                    print(f"Stok tidak mencukupi. Stok tersedia: {stok}")
                    continue

        except FileNotFoundError:
            print("File tidak ditemukan.")
            continue

        keranjang = []
        item_updated = False

        try:
            with open("keranjang.csv", mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["nama"] == nama and int(row["id kue"]) == id:
                        row["jumlah"] = str(int(row["jumlah"]) + qty)
                        item_updated = True
                    keranjang.append(row)

            if not item_updated:
                data_kue = {
                    "nama": nama,
                    "id kue": id,
                    "nama kue": nama_kue,
                    "jumlah": qty,
                    "harga": harga,
                    "jenis": jenis
                }
                keranjang.append(data_kue)

        except FileNotFoundError:
            data_kue = {
                "nama": nama,
                "id kue": id,
                "nama kue": nama_kue,
                "jumlah": qty,
                "harga": harga,
                "jenis": jenis
            }
            keranjang.append(data_kue)

        try:
            with open("keranjang.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["nama", "id kue", "nama kue", "jumlah", "harga", "jenis"])
                writer.writeheader()
                writer.writerows(keranjang)
            print(f"\nBerhasil menambahkan {qty} {nama_kue} ke keranjang")
            print("Anda akan dikembalikan ke menu utama...")
            time.sleep(3)
            pilihan(nama)
            return
        except FileNotFoundError:
            print("File tidak ditemukan")
            continue

def format_nominal(nominal):
    return f"Rp. {nominal:,.0f}".replace(',', '.')

def topup(nama):
    clear()
    print(pyfiglet.figlet_format("TOP UP", font='slant'))
    print("╔════════════════ TOP UP Menu ═══════════════╗")
    print("║                                            ║")
    print("║     💰 Tambahkan Saldo Ke Akun Anda 💰     ║")
    print("║                                            ║")
    print("╚════════════════════════════════════════════╝")
    
    saldo = None
    akun = []

    try:
        with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                akun.append(row)
                if row["nama"] == nama:
                    saldo = float(row["saldo"])
                    member_type = row["role"]
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return

    print("\n╔═══════════ Current Balance ═══════════╗")
    print("║                                       ║")
    print(f"║  Saldo: {format_nominal(saldo):<20}   ║")
    print("║                                       ║")
    print("╚═══════════════════════════════════════╝")

    print("\n╔══════════ Quick Top-up Options ═══════╗")
    print("║  1. Rp    50.000                      ║")
    print("║  2. Rp   100.000                      ║")
    print("║  3. Rp   250.000                      ║")
    print("║  4. Rp   500.000                      ║")
    print("║  5. Rp 1.000.000                      ║")
    print("║  6. Custom Amount                     ║")
    print("║  0. Back to Menu                      ║")
    print("╚═══════════════════════════════════════╝")

    while True:
        choice = input("\nPilih opsi (0-6): ")
        
        if choice == "0":
            print("\nKembali ke menu utama...")
            time.sleep(1)
            pilihan(nama)
            break
            
        amount = 0
        if choice == "1":
            amount = 50000
        elif choice == "2":
            amount = 100000
        elif choice == "3":
            amount = 250000
        elif choice == "4":
            amount = 500000
        elif choice == "5":
            amount = 1000000
        elif choice == "6":
            while True:
                try:
                    custom_amount = input("\nMasukkan jumlah top-up (min. Rp 10.000): ")
                    amount = int(custom_amount)
                    if amount < 10000:
                        print("Minimum top-up adalah Rp 10.000")
                        continue
                    break
                except ValueError:
                    print("Masukkan angka yang valid!")
                    continue
        else:
            print("Pilihan tidak valid!")
            continue

        try:
            for account in akun:
                if account["nama"] == nama:
                    account["saldo"] = float(account["saldo"]) + amount
                    saldo = account["saldo"]
            
            with open("akun.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["nama", "password", "role", "saldo", "voucher", "akun"])
                writer.writeheader()
                writer.writerows(akun)
            
            clear()
            print("\n╔═══════════ Top-up Success! ═══════════╗")
            print("║                                        ║")
            print(f"║  Amount Added: {format_nominal(amount):<22}║")
            print(f"║  New Balance: {format_nominal(saldo):<23}║")
            print("║                                        ║")
            print("╚════════════════════════════════════════╝")
            
            print("\nKembali ke menu utama dalam 3 detik...")
            time.sleep(3)
            pilihan(nama)
            break

        except Exception as e:
            print(f"\nError during top-up: {e}")
            print("Silakan coba lagi.")
            continue


def lihat_keranjang(nama):
    clear()
    print(pyfiglet.figlet_format("KERANJANG", font="slant"))
    tabel = PrettyTable(["ID", "Nama Kue", "Jumlah", "Harga", "Jenis", "Stok"])
    kue_data = {}
    keranjang_kosong = True 

    try:
        with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                id_kue = row["id"]
                kue_data[id_kue] = row
    except FileNotFoundError:
        print("File kue.csv tidak ditemukan.")
        pilihan(nama)
        return

    try:
        with open("keranjang.csv", mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["nama"] == nama:
                    keranjang_kosong = False
                    id_kue = row["id kue"]
                    
                    if row["jenis"] == "Timed Product":
                        timed_product = get_timed_product(int(id_kue))
                        if timed_product:
                            tabel.add_row([
                                id_kue,
                                row["nama kue"],
                                row["jumlah"],
                                f"Rp {row['harga']}",
                                row["jenis"],
                                timed_product["stok"]
                            ])
                    elif id_kue in kue_data:
                        stok = kue_data[id_kue]["stok"]
                        tabel.add_row([
                            id_kue,
                            row["nama kue"],
                            row["jumlah"],
                            f"Rp {row['harga']}",
                            row["jenis"],
                            stok
                        ])

        if keranjang_kosong:
            print("\n╔══════════════════════════════════════╗")
            print("║   😥Keranjang anda masih kosong!😥   ║")
            print("╚══════════════════════════════════════╝")
            input("\nTekan Enter untuk kembali...")
            pilihan(nama)
            return
        else:
            print(tabel)

    except FileNotFoundError:
        print("File keranjang.csv tidak ditemukan.")
        pilihan(nama)
        return

    while True:
        print("\n╔═══════════════PILIHAN════════════════╗")
        print("║   [Y] Checkout                       ║")
        print("║   [N] Kembali ke menu utama          ║")        
        print("╚══════════════════════════════════════╝")
        pil = input("\nPilihan anda: ")
        
        if pil.lower() == "y":
            checkout(nama)
            break
        elif pil.lower() == "n":
            pilihan(nama)
            break
        else:
            print("Pilihan tidak valid! Silakan coba lagi.")

def checkout(nama):
    while True:
        print("\n[Enter] Kembali ke menu utama")
        id_input = input("Masukkan ID yang ingin di-checkout: ")
        if id_input == "":
            pilihan(nama)
            return

        qty_input = input("Masukkan jumlah barang yang ingin di-checkout: ")

        try:
            id = int(id_input)
            qty = int(qty_input)
        except ValueError:
            print("ID dan jumlah harus berupa angka. Silakan coba lagi.")
            continue

        timed_product = get_timed_product(id)
        if timed_product:
            if qty > timed_product["stok"]:
                print(f"Stok tidak mencukupi. Stok tersedia: {timed_product['stok']}")
                return
        else:
            try:
                with open("kue.csv", mode="r", newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    kue_data = {row["id"]: row for row in reader}

                if str(id) not in kue_data:
                    print("ID kue tidak ditemukan.")
                    continue

            except FileNotFoundError:
                print("File kue.csv tidak ditemukan.")
                return

        try:
            with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                akun_data = []
                user_vouchers = None
                user_role = None
                for row in reader:
                    if row["nama"] == nama:
                        saldo = int(float(row["saldo"]))
                        user_vouchers = eval(row["voucher"])
                        user_role = row["role"]
                    akun_data.append(row)

        except FileNotFoundError:
            print("File akun.csv tidak ditemukan.")
            return

        try:
            with open("keranjang.csv", mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                keranjang_baru = []
                item_found = False
                voucher_used = None 

                for row in reader:
                    if row["nama"] == nama and str(row["id kue"]) == str(id):
                        item_found = True
                        jumlah_keranjang = int(row["jumlah"])

                        if qty > jumlah_keranjang:
                            print(f"Jumlah checkout tidak boleh melebihi jumlah di keranjang ({jumlah_keranjang}).")
                            return

                        total_harga = int(row["harga"]) * qty

                        if user_role == "vip":
                            vip_diskon = total_harga * 0.05
                            total_harga -= vip_diskon
                            print(f"\nDiskon VIP (5%): Rp {vip_diskon:,}")
                        
                        print(f"\nTotal setelah diskon VIP: Rp {total_harga:,}")

                        if saldo < total_harga:
                            print(f"Saldo tidak mencukupi. Total: Rp {total_harga:,}")
                            return

                        if row["jenis"] == "Timed Product":
                            timed_product = get_timed_product(id)
                            if not timed_product or qty > timed_product["stok"]:
                                print(f"Stok tidak mencukupi atau produk tidak tersedia pada jam ini.")
                                return
                        else:

                            stok_tersedia = int(kue_data[str(id)]["stok"])
                            if qty > stok_tersedia:
                                print(f"Stok tidak mencukupi. Stok tersedia: {stok_tersedia}")
                                return

                        if user_vouchers:
                            print("\nVoucher tersedia:", user_vouchers)
                            print("\n[Y] Pakai Voucher")
                            print("[N] Tidak Pakai")
                            print("[ENTER] Kembali ke menu utama")
                            konfirmasi = input("Pilihan anda: ").lower()

                            if konfirmasi == "y":
                                voucher = input("Masukkan voucher (diskon 5/diskon 10): ").lower()
                                if voucher in user_vouchers:
                                    voucher_diskon = total_harga * (0.05 if voucher == "diskon 5" else 0.10)
                                    total_harga -= voucher_diskon
                                    voucher_used = voucher
                                    print(f"\nDiskon voucher berhasil digunakan!")
                                    print(f"Diskon voucher: Rp {voucher_diskon:,}")
                                    print(f"Total setelah semua diskon: Rp {total_harga:,}")
                                else:
                                    print("Voucher tidak valid!")
                                    return

                            elif konfirmasi == "n":
                                pass
                            elif konfirmasi == "":
                                print("Kembali ke menu utama...")
                                pilihan(nama)
                                return
                            else:
                                print("Pilihan tidak valid!")
                                return

                        sisa_jumlah = jumlah_keranjang - qty
                        if sisa_jumlah > 0:
                            row["jumlah"] = str(sisa_jumlah)
                            keranjang_baru.append(row)
                    else:
                        keranjang_baru.append(row)

                if not item_found:
                    print("Item tidak ditemukan di keranjang.")
                    return

        except FileNotFoundError:
            print("File keranjang.csv tidak ditemukan.")
            return

        try:
            with open("akun.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["nama", "password", "role", "saldo", "voucher", "akun"])
                writer.writeheader()
                for row in akun_data:
                    if row["nama"] == nama:
                        row["saldo"] = str(float(saldo - total_harga))
                        if voucher_used:
                            current_vouchers = eval(row["voucher"])
                            current_vouchers.remove(voucher_used)
                            row["voucher"] = str(current_vouchers)
                    writer.writerow(row)
        except FileNotFoundError:
            print("Gagal update saldo.")
            return

        if not timed_product:
            try:
                with open("kue.csv", mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["id", "nama", "harga", "stok", "jenis"])
                    writer.writeheader()
                    for id_kue, row in kue_data.items():
                        if id_kue == str(id):
                            row["stok"] = str(int(row["stok"]) - qty)
                        writer.writerow(row)
            except FileNotFoundError:
                print("Gagal update stok.")
                return

        try:
            with open("keranjang.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["nama", "id kue", "nama kue", "jumlah", "harga", "jenis"])
                writer.writeheader()
                writer.writerows(keranjang_baru)
        except FileNotFoundError:
            print("Gagal update keranjang.")
            return

        print("\nCheckout berhasil!")
        print(f"Sisa saldo: Rp {format_nominal(saldo - total_harga)}")
        input("Tekan [Enter] untuk kembali ke menu...")
        pilihan(nama)
        return

def menu_beli(nama):
	clear()
	print(pyfiglet.figlet_format("MENU BELI", font="slant"))
	print("╔══════════════════════════════════════╗")
	print("║                KATALOG               ║")
	print("╠══════════════════════════════════════╣")
	print("║  1] SEMUA PRODUK                     ║")
	print("║  2] BROWNIES                         ║")
	print("║  3] PASTRY                           ║")
	print("║  4] BOLU                             ║")
	print("║  5] PREMIUM PRODUCT                  ║")
	print("║  6] TIMED PRODUCT                    ║")
	print("║  0] KEMBALI                          ║")
	print("╚══════════════════════════════════════╝")
	pil = input("Masukan pilihan: ")
	if pil == "1":
		clear()
		lihat_semua()
		beli(nama)
	elif pil == "2":
		clear()
		lihat_brownies()
		beli(nama)
	elif pil == "3":
		clear()
		lihat_pastry()
		beli(nama)
	elif pil == "4":
		clear()
		lihat_bolu()
		beli(nama)
	elif pil == "5":
		clear()
		lihat_premium()
		beli(nama)
	elif pil == "6":
		clear()
		lihat_timed(nama)
		beli(nama)
	elif pil == "0":
		pilihan(nama)
	else:
		print("Pilihan tidak valid")
		menu_beli()

def lihat_akun(nama):
    clear()
    print(pyfiglet.figlet_format("ACCOUNT INFO", font='slant'))

    try:
        with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            user_data = None
            for row in reader:
                if row["nama"] == nama:
                    user_data = row
                    break

            if user_data:
                badge = "👑 VIP Member" if user_data['role'] == "vip" else "⭐ Regular Member"

                print("╔════════════ Account Details ════════════╗")
                print("║                                         ║")
                print(f"║  👤 Username: {nama:<24} ║")
                print(f"║  🎖️ Status: {badge:<25} ║")
                print("║                                         ║")
                print("╚═════════════════════════════════════════╝")

                print("\n╔════════════ Balance Info ═══════════════╗")
                print("║                                         ║")
                print(f"║  💰 Current Balance:                    ║")
                print(f"║     {format_nominal(float(user_data['saldo'])):<35}║")
                print("║                                         ║")
                print("╚═════════════════════════════════════════╝")

                vouchers = eval(user_data['voucher'])
                print("\n╔════════════ Your Vouchers ══════════════╗")
                print("║                                         ║")
                if vouchers:
                    for voucher in vouchers:
                        print(f"║  🎫 {voucher:<35} ║")
                else:
                    print("║  No vouchers available                  ║")
                print("║                                         ║")
                print("╚═════════════════════════════════════════╝")

                print("\n╔════════════ Member Benefits ════════════╗")
                print("║                                         ║")
                if user_data['role'] == "vip":
                    print("║  ✨ Automatic 5% discount on all items  ║")
                    print("║  ✨ Exclusive monthly vouchers          ║")
                    print("║  ✨ Priority customer service           ║")
                    print("║  ✨ Special birthday treats             ║")
                else:
                    print("║  ⭐ Access to regular promotions        ║")
                    print("║  ⭐ Voucher rewards                     ║")
                    print("║  ⭐ Upgrade to VIP for more benefits!   ║")
                print("║                                         ║")
                print("╚═════════════════════════════════════════╝")

                print("\n╔════════════════ Menu ═══════════════════╗")
                print("║                                         ║")
                print("║  [Enter] Back to Main Menu              ║")
                if user_data['role'] != "vip":
                    print("║  [U] Upgrade to VIP                     ║")
                print("║                                         ║")
                print("╚═════════════════════════════════════════╝")

                while True:
                    pil = input("\nPilihan anda: ").lower()
                    if pil == "":
                        pilihan(nama)
                        break
                    elif pil == "u" and user_data['role'] != "vip":
                        upgrade(nama)
                        break
                    else:
                        print("Pilihan tidak valid!")
            else:
                print(" Akun tidak ditemukan!")
                input("Tekan Enter untuk kembali...")
                pilihan(nama)

    except FileNotFoundError:
        print("File akun.csv tidak ditemukan!")
        input("Tekan Enter untuk kembali...")
        pilihan(nama)

def upgrade(nama):
    clear()
    print("\n╔═════════ VIP Benefits ════════════╗")
    print("║  • Automatic 5% discount          ║")
    print("║  • Exclusive monthly vouchers     ║")
    print("║  • Priority custom orders         ║")
    print("║  • Birthday special treats        ║")
    print("╚═══════════════════════════════════╝")
    print("\n╔═════════ VIP Benefits ════════════╗")
    print("║          HANYA DENGAN 50000       ║")
    print("╚═══════════════════════════════════╝")

    print("Apakah anda ingin mengupgrade member")
    print("[Y] Upgrade")
    print("[N] Kembali")
    pil = input("Masukan pilihan: ").lower()
    if pil == "y":
        with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data_akun = list(reader) 
            
        for row in data_akun:
            if row["nama"] == nama:
                if float(row["saldo"]) > 50000:
                    row["saldo"] = str(float(row["saldo"]) - 50000)
                    row["role"] = "vip"
                else:
                        print("Saldo anda tidak cukup, Anda akan diarahkan ke menu...")
                        time.sleep(3)
                        pilihan(nama)

        with open("akun.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["nama", "password", "role", "saldo", "voucher", "akun"])
            writer.writeheader()
            writer.writerows(data_akun)  
            
        print("Akun anda berhasil di upgrade, role anda sekarang adalah vip!")
        print("Kembali ke menu vip...")
        time.sleep(3)
        pilihan(nama)
    
    elif pil == "n":
        pilihan(nama)

def event(nama):
    clear()
    print(pyfiglet.figlet_format("SPECIAL EVENT", font='slant'))
    print("╔════════════════ SPECIAL EVENT ═══════════════╗")
    print("║                                              ║")
    print("║            🎉 BAGI BAGI VOUCHER 🎉          ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")

    print("\n╔══════════════ Available Vouchers ═════════════╗")
    print("║                                               ║")
    print("║  [1] 🎫 Voucher Diskon 5%                     ║")
    print("║  [2] 🎫 Voucher Diskon 10%                    ║")
    print("║  [0] Kembali ke Menu Utama                    ║")
    print("║                                               ║")
    print("╚═══════════════════════════════════════════════╝")

    while True:
        choice = input("\n🎯 Pilih voucher (0-2): ")

        if choice == "0":
            print("\nKembali ke menu utama...")
            time.sleep(1)
            pilihan(nama)
            return

        if choice not in ["1", "2"]:
            print("Pilihan tidak valid! Silakan coba lagi.")
            continue

        try:
            with open("akun.csv", mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                accounts = list(reader)
                user_found = False

                for account in accounts:
                    if account["nama"] == nama:
                        user_found = True
                        current_vouchers = eval(account["voucher"])
                        
                        new_voucher = "diskon 5" if choice == "1" else "diskon 10"
                        current_vouchers.append(new_voucher)
                        account["voucher"] = str(current_vouchers)

                        with open("akun.csv", mode="w", newline="", encoding="utf-8") as outfile:
                            writer = csv.DictWriter(outfile, fieldnames=["nama", "password", "role", "saldo", "voucher", "akun"])
                            writer.writeheader()
                            writer.writerows(accounts)

                        clear()
                        print("\n╔════════════════════════════════════════╗")
                        print("║        ✨ VOUCHER TERTAMBAH! ✨        ║")
                        print("╠════════════════════════════════════════╣")

                        print("\n[Y] Ambil Voucher Lagi")
                        print("[N] Kembali ke Menu")
                        
                        while True:
                            again = input("\nPilihan anda: ").lower()
                            if again == "y":
                                event(nama)
                                return
                            elif again == "n":
                                print("\nKembali ke menu utama...")
                                time.sleep(1)
                                pilihan(nama)
                                return
                            else:
                                print("Pilihan tidak valid!")

                if not user_found:
                    print("User tidak ditemukan!")
                    return

        except FileNotFoundError:
            print("Error: File akun.csv tidak ditemukan!")
            return
        except Exception as e:
            print(f"Error: {str(e)}")
            return

def menu_biasa(nama):
	clear()
	print(pyfiglet.figlet_format("MENU", font="slant"))
	print("╔══════════════════════════════════════╗")
	print("║            SELAMAT DATANG            ║")
	print("╠══════════════════════════════════════╣")
	print("║  1] BELI PRODUK                      ║")
	print("║  2] TOPUP SALDO                      ║")
	print("║  3] LIHAT KERANJANG                  ║")
	print("║  4] EVENT                            ║")
	print("║  5] LIHAT AKUN                       ║")
	print("║  6] UPGRADE MEMBER                   ║")
	print("║  0] LOGOUT                           ║")
	print("╚══════════════════════════════════════╝")
	while True:
		pil = input("Masukan Pilihan: ")
		if pil == "1": 
			menu_beli(nama)
		elif pil == "2":
			topup(nama)
		elif pil == "3":
			lihat_keranjang(nama)
		elif pil == "4":
			event(nama)
		elif pil == "5":
			lihat_akun(nama)
		elif pil == "6":
			upgrade(nama)
		elif pil == "0":
			menu_login()
		else:
			print("Pilihan tidak valid. ")
			continue

def menu_vip(nama):
	clear()
	print(pyfiglet.figlet_format("MENU", font="slant"))
	print("╔══════════════════════════════════════╗")
	print("║            SELAMAT DATANG            ║")
	print("╠══════════════════════════════════════╣")
	print("║  1] BELI PRODUK                      ║")
	print("║  2] TOPUP SALDO                      ║")
	print("║  3] LIHAT KERANJANG                  ║")
	print("║  4] EVENT                            ║")
	print("║  5] LIHAT AKUN                       ║")
	print("║  0] LOGOUT                           ║")
	print("╚══════════════════════════════════════╝")
	while True:
		pil = input("Masukan Pilihan: ")
		if pil == "1": 
			menu_beli(nama)
		elif pil == "2":
			topup(nama)
		elif pil == "3":
			lihat_keranjang(nama)
		elif pil == "4":
			event(nama)
		elif pil == "5":
			lihat_akun(nama)
		elif pil == "0":
			menu_login()
		else:
			print("Pilihan tidak valid. ")
			continue

def menu_login():
    clear()
    print(pyfiglet.figlet_format("BAKER'S DIARY", font='slant'))
    print("═" * 50)
    print("            .-'`'-.")
    print("         .-'  _,=a_ '-.")
    print("        ( _, '       \\ )")
    print("         \\__, `    -==)")
    print("          \\'`.  ;')")
    print("           \|_ _,'")
    print("           /  `\\")
    print("          /    ;")
    print("         /  :  \\")
    print("        /    :  \\")
    print("       /     ;   \\")
    print("      /      :    \\")
    print("     /       :     \\")
    print("    /        ;      \\")
    print("   /                 \\")
    print("═" * 50)
    
    print("\n╔════════════ About Us ═════════════╗")
    print("║  Welcome to Baker's Diary!        ║")
    print("║  Your Daily Happiness Bakery      ║")
    print("║                                   ║")
    print("║  • Fresh baked goods daily        ║")
    print("║  • Premium quality ingredients    ║")
    print("║  • Artisanal breads & pastries    ║")
    print("║  • Custom cake orders             ║")
    print("╚═══════════════════════════════════╝")

    print("\n╔═════════ VIP Benefits ════════════╗")
    print("║  • Automatic 5% discount          ║")
    print("║  • Exclusive monthly vouchers     ║")
    print("║  • Priority custom orders         ║")
    print("║  • Birthday special treats        ║")
    print("╚═══════════════════════════════════╝")

    print("\n╔═════════════ Menu ════════════════╗")
    print("║  [1] Register                     ║")
    print("║  [2] Login                        ║")
    print("║  [3] Exit                         ║")
    print("╚═══════════════════════════════════╝")
    
    while True:
        try:
            pil = input("\nMasukan pilihan: ")
            if pil == "1":
                print("\nMengarahkan ke halaman registrasi...")
                time.sleep(1)
                register()
            elif pil == "2":
                print("\nMengarahkan ke halaman login...")
                time.sleep(1)
                login()
            elif pil == "3":
                clear()
                print(pyfiglet.figlet_format("THANK YOU!", font='slant'))
                print("╔═══════════════════════════════════╗")
                print("║   Thank you for visiting          ║")
                print("║       Baker's Diary!              ║")
                print("║                                   ║")
                print("║     We hope to see you again      ║")
                print("║          soon! 🍰 🥖 🍪           ║")
                print("╚═══════════════════════════════════╝")
                time.sleep(2)
                exit()
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

menu_login()