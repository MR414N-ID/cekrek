#!/usr/bin/env python3
# lang: Python 3, file: cekrekening.py, target: Termux/Android
# API: https://cekrekening-api.belibayar.online/api/v1/account-inquiry

import sys
import json
import time
import os

try:
    import requests
except ImportError:
    print("Install dulu: pip install requests")
    sys.exit(1)

# ─────────────────────────────────────────────
#  WARNA ANSI
# ─────────────────────────────────────────────
R  = "\033[0m"
BD = "\033[1m"
DM = "\033[2m"

BLK = "\033[30m"
RED = "\033[31m"
GRN = "\033[32m"
YLW = "\033[33m"
BLU = "\033[34m"
MGN = "\033[35m"
CYN = "\033[36m"
WHT = "\033[37m"

BBLK = "\033[90m"
BRED = "\033[91m"
BGRN = "\033[92m"
BYLW = "\033[93m"
BBLU = "\033[94m"
BMGN = "\033[95m"
BCYN = "\033[96m"
BWHT = "\033[97m"

BG_BLK  = "\033[40m"
BG_RED  = "\033[41m"
BG_GRN  = "\033[42m"
BG_YLW  = "\033[43m"
BG_BLU  = "\033[44m"
BG_MGN  = "\033[45m"
BG_CYN  = "\033[46m"
BG_BBLK = "\033[100m"
BG_BRED = "\033[101m"
BG_BGRN = "\033[102m"
BG_BBLU = "\033[104m"
BG_BMGN = "\033[105m"
BG_BCYN = "\033[106m"

def clr(): os.system("clear")

# ─────────────────────────────────────────────
#  BEBEK LINUX ASCII ART
# ─────────────────────────────────────────────
DUCK = f"""
{BYLW}         __
{BYLW}        /  \\{BWHT}__
{BYLW}       /   /{BYLW}  \\
{BYLW}      / oo {BWHT}\\___/
{BYLW}     /  || {BWHT}
{BYLW}    /___||
{BYLW}   (  ({BWHT}``{BYLW})
{BYLW}    \\__//{R}"""

# ─────────────────────────────────────────────
#  BANNER UTAMA
# ─────────────────────────────────────────────
def banner():
    clr()
    w = 56
    line = f"{BBLK}{'━' * w}{R}"

    duck_lines = DUCK.strip('\n').split('\n')

    title_art = [
        f"{BMGN}{BD} ███╗   ███╗██████╗ ██╗  ██╗ ██╗██╗  ██╗{R}",
        f"{BMGN}{BD} ████╗ ████║██╔══██╗██║  ██║███║██║  ██║{R}",
        f"{BCYN}{BD} ██╔████╔██║██████╔╝███████║╚██║███████║{R}",
        f"{BCYN}{BD} ██║╚██╔╝██║██╔══██╗╚════██║ ██║╚════██║{R}",
        f"{BBLU}{BD} ██║ ╚═╝ ██║██║  ██║     ██║ ██║     ██║{R}",
        f"{BBLU}{BD} ╚═╝     ╚═╝╚═╝  ╚═╝     ╚═╝ ╚═╝     ╚═╝{R}",
        f"",
        f"  {BBLK}┤{R} {BYLW}{BD}N{R}{BWHT}{BD}− {R}{BYLW}{BD}I{R}{BWHT}{BD}D{R}  {BBLK}├{R}  {DM}{BWHT}by {BMGN}Bebek Linux{R}",
    ]

    print()
    print(f"  {line}")
    print()

    # Bebek di kiri, title di kanan (berdampingan)
    max_rows = max(len(duck_lines), len(title_art))
    for i in range(max_rows):
        dl = duck_lines[i] if i < len(duck_lines) else ""
        tl = title_art[i] if i < len(title_art) else ""
        print(f"  {dl:<20}{tl}")

    print()
    print(f"  {line}")
    print(f"  {BBLK}  {BG_BBLK}{BWHT}{BD}  CEK REKENING BANK & e-WALLET INDONESIA  {R}")
    print(f"  {line}")
    print(f"  {DM}{BWHT}  API  : cekrekening-api.belibayar.online{R}")
    print(f"  {DM}{BWHT}  Tool : cekrekening.py v1.0{R}")
    print(f"  {line}")
    print()

# ─────────────────────────────────────────────
#  DAFTAR BANK
# ─────────────────────────────────────────────
BANKS = {
    # ─── Bank Nasional Besar ───
    "bca":    "Bank Central Asia (BCA)",
    "bni":    "BNI (Bank Negara Indonesia)",
    "bri":    "Bank Rakyat Indonesia (BRI)",
    "mandiri":"Bank Mandiri",
    "btn":    "BTN",
    "bsm":    "BSI (Bank Syariah Indonesia)",
    "cimb":   "CIMB Niaga & Syariah",
    "danamon":"Bank Danamon & Syariah",
    "permata":"Permata Bank",

    # ─── Bank Digital ───
    "royal":  "Blu/BCA Digital",
    "artos":  "Jago/Artos",
    "yudha_bakti": "Neo Commerce/Yudha Bhakti",
    "kesejahteraan_ekonomi": "SeaBank",
    "super_bank": "Superbank",
    "krom":   "Krom Bank",
    "hana":   "LINE Bank/KEB Hana",
    "mnc_internasional": "Motion/MNC Bank",

    # ─── Bank Lain ───
    "panin":  "Panin Bank",
    "mega":   "Bank Mega",
    "ocbc":   "Bank OCBC NISP",
    "dbs":    "DBS Indonesia",
    "uob":    "TMRW/UOB",
    "maybank":"Maybank Indonesia",
    "bukopin":"Wokee/Bukopin",
    "muamalat":"Muamalat",
    "btpn":   "BTPN",
    "sinarmas":"Bank Sinarmas",
    "maspion":"Bank Maspion",
    "hsbc":   "HSBC Indonesia",
    "icbc":   "ICBC Indonesia",
    "citibank":"Citibank",
    "commonwealth":"Commonwealth Bank",

    # ─── Bank Daerah ───
    "bjb":    "BJB",
    "dki":    "Bank DKI",
    "jawa_tengah": "Bank Jateng",
    "jawa_timur":  "Bank Jatim",
    "aceh":   "Bank Aceh Syariah",
    "sumut":  "Bank Sumut",
    "sumsel_dan_babel": "Bank Sumsel Babel",
    "riau_dan_kepri": "Bank Riau Kepri",
    "sulselbar": "Bank Sulselbar",
    "bali":   "BPD Bali",
    "bengkulu":"Bank Bengkulu",
    "lampung":"Bank Lampung",
    "papua":  "Bank Papua",
    "maluku": "Bank Maluku",
    "jambi":  "Bank Jambi",
    "kalimantan_barat": "Bank Kalbar",
    "kalimantan_selatan": "Bank Kalsel",
    "kalimantan_tengah":  "Bank Kalteng",
    "kalimantan_timur":   "Bank Kaltimtara",
    "daerah_istimewa":    "Bank BPD DIY",
    "banten": "BPD Banten",
    "sumatera_barat": "Bank Nagari",

    # ─── e-Wallet ───
    "ovo":      "OVO",
    "dana":     "DANA",
    "linkaja":  "LinkAja",
    "gopay":    "GoPay",
    "shopeepay":"ShopeePay",
}

# grup untuk tampilan menu
BANK_GROUPS = {
    f"{BD}{BYLW}[ BANK NASIONAL BESAR ]{R}": [
        "bca","bni","bri","mandiri","btn","bsm","cimb","danamon","permata"
    ],
    f"{BD}{BCYN}[ BANK DIGITAL ]{R}": [
        "royal","artos","yudha_bakti","kesejahteraan_ekonomi",
        "super_bank","krom","hana","mnc_internasional"
    ],
    f"{BD}{BGRN}[ BANK LAINNYA ]{R}": [
        "panin","mega","ocbc","dbs","uob","maybank","bukopin",
        "muamalat","btpn","sinarmas","maspion","hsbc","icbc",
        "citibank","commonwealth"
    ],
    f"{BD}{BMGN}[ BANK DAERAH ]{R}": [
        "bjb","dki","jawa_tengah","jawa_timur","aceh","sumut",
        "sumsel_dan_babel","riau_dan_kepri","sulselbar","bali",
        "bengkulu","lampung","papua","maluku","jambi",
        "kalimantan_barat","kalimantan_selatan","kalimantan_tengah",
        "kalimantan_timur","daerah_istimewa","banten","sumatera_barat"
    ],
    f"{BD}{BBLU}[ e-WALLET ]{R}": [
        "ovo","dana","linkaja","gopay","shopeepay"
    ],
}

# ─────────────────────────────────────────────
#  MENU PILIH BANK
# ─────────────────────────────────────────────
def show_bank_menu():
    banner()
    print(f"  {BD}{BWHT}PILIH BANK / e-WALLET{R}\n")

    idx = 1
    idx_map = {}

    for group_label, keys in BANK_GROUPS.items():
        print(f"  {group_label}")
        cols = 2
        items = [(k, BANKS[k]) for k in keys if k in BANKS]
        for i in range(0, len(items), cols):
            row = items[i:i+cols]
            line_str = ""
            for k, name in row:
                num_str = f"{BBLK}[{BYLW}{BD}{idx:>3}{R}{BBLK}]{R}"
                entry   = f"{num_str} {BWHT}{name:<30}{R}"
                line_str += f"  {entry}"
                idx_map[idx] = k
                idx += 1
            print(line_str)
        print()

    print(f"  {BBLK}{'─' * 54}{R}")
    print(f"  {BBLK}[{R}{BYLW}{BD}  0{R}{BBLK}]{R} {WHT}Ketik kode bank langsung (manual){R}")
    print(f"  {BBLK}[{R}{BRED}{BD}  q{R}{BBLK}]{R} {WHT}Keluar{R}")
    print(f"  {BBLK}{'─' * 54}{R}\n")

    return idx_map

# ─────────────────────────────────────────────
#  SPINNER
# ─────────────────────────────────────────────
def spinner_msg(msg: str, duration: float = 1.6):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {BCYN}{frames[i % len(frames)]}{R} {BWHT}{msg}{R}   ")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()

# ─────────────────────────────────────────────
#  CEK REKENING
# ─────────────────────────────────────────────
API_URL = "https://cekrekening-api.belibayar.online/api/v1/account-inquiry"

def cek_rekening(bank_code: str, nomor: str):
    try:
        spinner_msg("Menghubungi server ...")
        resp = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json={"account_bank": bank_code, "account_number": nomor},
            timeout=15,
        )
        return resp.json(), resp.status_code
    except requests.exceptions.ConnectionError:
        return {"message": "Tidak ada koneksi internet"}, 0
    except requests.exceptions.Timeout:
        return {"message": "Request timeout — coba lagi"}, 0
    except Exception as e:
        return {"message": str(e)}, 0

def show_result(result: dict, status_code: int, bank_name: str, nomor: str):
    w = 56
    line = f"  {BBLK}{'━' * w}{R}"
    print(line)
    if status_code == 200 and result.get("data"):
        holder = result["data"].get("account_holder", "TIDAK DITEMUKAN")
        print(f"\n  {BG_BGRN}{BLK}{BD}  ✔  REKENING DITEMUKAN  {R}\n")
        print(f"  {BBLK}Bank    :{R} {BWHT}{BD}{bank_name}{R}")
        print(f"  {BBLK}Nomor   :{R} {BWHT}{BD}{nomor}{R}")
        print(f"  {BBLK}Pemilik :{R} {BGRN}{BD}{holder}{R}\n")
    else:
        msg = result.get("message", "Rekening tidak ditemukan")
        print(f"\n  {BG_BRED}{BLK}{BD}  ✖  GAGAL / TIDAK DITEMUKAN  {R}\n")
        print(f"  {BBLK}Bank    :{R} {BWHT}{BD}{bank_name}{R}")
        print(f"  {BBLK}Nomor   :{R} {BWHT}{BD}{nomor}{R}")
        print(f"  {BBLK}Pesan   :{R} {BRED}{BD}{msg}{R}\n")
    print(line)

# ─────────────────────────────────────────────
#  LOOP UTAMA
# ─────────────────────────────────────────────
def prompt(text: str) -> str:
    return input(f"  {BCYN}❯{R} {BWHT}{text}{R} ").strip()

def main():
    while True:
        idx_map = show_bank_menu()

        raw = prompt("Nomor / kode bank (0=manual, q=keluar):")
        if raw.lower() == "q":
            print(f"\n  {BYLW}Sampai jumpa!{R}\n")
            break

        if raw == "0":
            # input manual
            clr()
            banner()
            print(f"  {BD}{BWHT}INPUT MANUAL{R}\n")
            bank_code = prompt("Kode bank (contoh: bca, bri, ovo):").lower()
            bank_name = BANKS.get(bank_code, bank_code.upper())
        elif raw.isdigit() and int(raw) in idx_map:
            bank_code = idx_map[int(raw)]
            bank_name = BANKS[bank_code]
        else:
            # coba langsung sebagai kode bank
            bank_code = raw.lower()
            bank_name = BANKS.get(bank_code, bank_code.upper())
            if bank_code not in BANKS:
                print(f"\n  {BRED}Kode tidak dikenali: {raw}{R}\n")
                input(f"  {BBLK}Tekan Enter untuk kembali ...{R}")
                continue

        clr()
        banner()
        print(f"  {BD}{BWHT}DETAIL PENCARIAN{R}\n")
        print(f"  {BBLK}Bank :{R} {BYLW}{BD}{bank_name}{R}")

        nomor = prompt("Nomor rekening:")
        if not nomor:
            print(f"\n  {BRED}Nomor rekening wajib diisi.{R}\n")
            input(f"  {BBLK}Tekan Enter ...{R}")
            continue

        print()
        result, status = cek_rekening(bank_code, nomor)
        show_result(result, status, bank_name, nomor)

        print()
        again = prompt("Cek lagi? (y/n):").lower()
        if again != "y":
            print(f"\n  {BYLW}Sampai jumpa!{R}\n")
            break

if __name__ == "__main__":
    main()
