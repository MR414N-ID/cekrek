#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════╗
║       CEK REKENING - Cek Nama Rekening Bank/e-Wallet      ║
║              Indonesia  🏦  powered by netovas.com        ║
╚═══════════════════════════════════════════════════════════╝
  Jalankan: python3 cekrekening.py
"""

import sys
import json
import time
import threading
import http.client
import urllib.parse

# ═══════════════════════ KONFIGURASI ════════════════════════════════════════
API_HOST   = "netovas.com"
API_PATH   = "/api/cekrek/v1/account-inquiry"
TIMEOUT    = 15

# ═══════════════════════ WARNA ANSI ══════════════════════════════════════════
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

def clr(text, *codes):
    return "".join(codes) + str(text) + C.RESET

def clear_screen():
    print("\033[2J\033[H", end="")

# ═══════════════════════ DATA BANK & E-WALLET ════════════════════════════════
BANKS = [
    ("harda",                      "Allo Bank / Bank Harda Internasional"),
    ("anz",                        "ANZ Indonesia"),
    ("aceh",                       "Bank Aceh Syariah"),
    ("aladin",                     "Bank Aladin Syariah"),
    ("amar",                       "Bank Amar Indonesia"),
    ("antardaerah",                "Bank Antardaerah"),
    ("artha",                      "Bank Artha Graha Internasional"),
    ("bengkulu",                   "Bank Bengkulu"),
    ("daerah_istimewa",            "Bank BPD DIY"),
    ("daerah_istimewa_syr",        "Bank BPD DIY Syariah"),
    ("btpn_syr",                   "Bank BTPN Syariah"),
    ("bukopin_syr",                "Bank Bukopin Syariah"),
    ("bumi_arta",                  "Bank Bumi Arta"),
    ("capital",                    "Bank Capital Indonesia"),
    ("bca",                        "Bank Central Asia (BCA)"),
    ("ccb",                        "Bank China Construction Bank Indonesia"),
    ("cnb",                        "Bank CNB (Centratama Nasional Bank)"),
    ("danamon",                    "Bank Danamon & Danamon Syariah"),
    ("dinar",                      "Bank Dinar Indonesia"),
    ("dki",                        "Bank DKI"),
    ("dki_syr",                    "Bank DKI Syariah"),
    ("ganesha",                    "Bank Ganesha"),
    ("agris",                      "Bank IBK Indonesia"),
    ("ina_perdana",                "Bank Ina Perdana"),
    ("index_selindo",              "Bank Index Selindo"),
    ("artos_syr",                  "Bank Jago Syariah"),
    ("jambi",                      "Bank Jambi"),
    ("jambi_syr",                  "Bank Jambi Syariah"),
    ("jasa_jakarta",               "Bank Jasa Jakarta"),
    ("jawa_tengah",                "Bank Jateng"),
    ("jawa_tengah_syr",            "Bank Jateng Syariah"),
    ("jawa_timur",                 "Bank Jatim"),
    ("jawa_timur_syr",             "Bank Jatim Syariah"),
    ("kalimantan_barat",           "Bank Kalbar"),
    ("kalimantan_barat_syr",       "Bank Kalbar Syariah"),
    ("kalimantan_selatan",         "Bank Kalsel"),
    ("kalimantan_selatan_syr",     "Bank Kalsel Syariah"),
    ("kalimantan_tengah",          "Bank Kalteng"),
    ("kalimantan_timur_syr",       "Bank Kaltim Syariah"),
    ("kalimantan_timur",           "Bank Kaltimtara"),
    ("lampung",                    "Bank Lampung"),
    ("maluku",                     "Bank Maluku"),
    ("mandiri",                    "Bank Mandiri"),
    ("mantap",                     "Bank MANTAP (Mandiri Taspen)"),
    ("maspion",                    "Bank Maspion Indonesia"),
    ("mayapada",                   "Bank Mayapada"),
    ("mayora",                     "Bank Mayora Indonesia"),
    ("mega",                       "Bank Mega"),
    ("mega_syr",                   "Bank Mega Syariah"),
    ("mestika_dharma",             "Bank Mestika Dharma"),
    ("mizuho",                     "Bank Mizuho Indonesia"),
    ("mas",                        "Bank Multi Arta Sentosa (Bank MAS)"),
    ("mutiara",                    "Bank Mutiara"),
    ("sumatera_barat",             "Bank Nagari"),
    ("sumatera_barat_syr",         "Bank Nagari Syariah"),
    ("nusa_tenggara_barat",        "Bank NTB Syariah"),
    ("nusa_tenggara_timur",        "Bank NTT"),
    ("nusantara_parahyangan",      "Bank Nusantara Parahyangan"),
    ("ocbc",                       "Bank OCBC NISP"),
    ("ocbc_syr",                   "Bank OCBC NISP Syariah"),
    ("america_na",                 "Bank of America NA"),
    ("boc",                        "Bank of China (Hong Kong) Limited"),
    ("india",                      "Bank of India Indonesia"),
    ("tokyo",                      "Bank of Tokyo Mitsubishi UFJ"),
    ("papua",                      "Bank Papua"),
    ("prima",                      "Bank Prima Master"),
    ("bri",                        "Bank Rakyat Indonesia (BRI)"),
    ("riau_dan_kepri",             "Bank Riau Kepri"),
    ("sahabat_sampoerna",          "Bank Sahabat Sampoerna"),
    ("shinhan",                    "Bank Shinhan Indonesia"),
    ("sinarmas",                   "Bank Sinarmas"),
    ("sinarmas_syr",               "Bank Sinarmas Syariah"),
    ("sulselbar",                  "Bank Sulselbar"),
    ("sulselbar_syr",              "Bank Sulselbar Syariah"),
    ("sulawesi",                   "Bank Sulteng"),
    ("sulawesi_tenggara",          "Bank Sultra"),
    ("sulut",                      "Bank SulutGo"),
    ("sumsel_dan_babel",           "Bank Sumsel Babel"),
    ("sumsel_dan_babel_syr",       "Bank Sumsel Babel Syariah"),
    ("sumut",                      "Bank Sumut"),
    ("sumut_syr",                  "Bank Sumut Syariah"),
    ("resona_perdania",            "Bank Resona Perdania"),
    ("victoria_internasional",     "Bank Victoria International"),
    ("victoria_syr",               "Bank Victoria Syariah"),
    ("woori",                      "Bank Woori Saudara"),
    ("bca_syr",                    "BCA Syariah"),
    ("bjb",                        "BJB"),
    ("bjb_syr",                    "BJB Syariah"),
    ("royal",                      "Blu / BCA Digital"),
    ("bni",                        "BNI (Bank Negara Indonesia)"),
    ("bnp_paribas",                "BNP Paribas Indonesia"),
    ("bali",                       "BPD Bali"),
    ("banten",                     "BPD Banten"),
    ("eka",                        "BPR EKA (Bank Eka)"),
    ("agroniaga",                  "BRI Agroniaga"),
    ("bsm",                        "BSI (Bank Syariah Indonesia)"),
    ("btn",                        "BTN"),
    ("btn_syr",                    "BTN Syariah"),
    ("tabungan_pensiunan_nasional", "BTPN"),
    ("cimb",                       "CIMB Niaga & CIMB Niaga Syariah"),
    ("citibank",                   "Citibank"),
    ("commonwealth",               "Commonwealth Bank"),
    ("chinatrust",                 "CTBC (Chinatrust) Indonesia"),
    ("dbs",                        "DBS Indonesia"),
    ("hsbc",                       "HSBC Indonesia"),
    ("icbc",                       "ICBC Indonesia"),
    ("artos",                      "Jago / Artos"),
    ("hana",                       "LINE Bank / KEB Hana"),
    ("bii",                        "Maybank Indonesia"),
    ("bii_syr",                    "Maybank Syariah"),
    ("mnc_internasional",          "Motion / MNC Bank"),
    ("muamalat",                   "Muamalat"),
    ("yudha_bakti",                "Neo Commerce / Yudha Bhakti"),
    ("nationalnobu",               "Nobu (Nationalnobu) Bank"),
    ("panin",                      "Panin Bank"),
    ("panin_syr",                  "Panin Dubai Syariah"),
    ("permata",                    "Permata"),
    ("permata_syr",                "Permata Syariah"),
    ("qnb_kesawan",                "QNB Indonesia"),
    ("rabobank",                   "Rabobank International Indonesia"),
    ("sbi_indonesia",              "SBI Indonesia"),
    ("kesejahteraan_ekonomi",      "Seabank / Bank BKE"),
    ("standard_chartered",         "Standard Chartered Bank"),
    ("super_bank",                 "Superbank"),
    ("uob",                        "TMRW / UOB"),
    ("bukopin",                    "Wokee / Bukopin"),
    ("krom",                       "Krom Bank Indonesia"),
]

EWALLETS = [
    ("ovo",       "OVO"),
    ("dana",      "DANA"),
    ("linkaja",   "LinkAja"),
    ("gopay",     "GoPay"),
    ("shopeepay", "ShopeePay"),
]

ALL_OPTIONS = BANKS + EWALLETS
CODE_MAP    = {code: nama for code, nama in ALL_OPTIONS}

# ═══════════════════════ BANNER ═══════════════════════════════════════════════
def print_banner():
    print(f"""
{clr("╔══════════════════════════════════════════════════════════╗", C.CYAN, C.BOLD)}
{clr("║", C.CYAN, C.BOLD)}  {clr("💳  CEK REKENING", C.MAGENTA, C.BOLD)}  {clr("─  Cek Nama Rekening Bank / e-Wallet", C.WHITE)}  {clr("║", C.CYAN, C.BOLD)}
{clr("║", C.CYAN, C.BOLD)}  {clr("🇮🇩  Bank & e-Wallet Indonesia  ─  powered by netovas.com", C.YELLOW)}  {clr("║", C.CYAN, C.BOLD)}
{clr("╚══════════════════════════════════════════════════════════╝", C.CYAN, C.BOLD)}
  {clr("Ketik", C.DIM)} {clr("'list'", C.CYAN)} {clr("→ lihat semua bank | ", C.DIM)}{clr("'contoh'", C.YELLOW)} {clr("→ format input | ", C.DIM)}{clr("'exit'", C.RED)} {clr("→ keluar", C.DIM)}
""")

# ═══════════════════════ SPINNER ════════════════════════════════════════════
class Spinner:
    FRAMES = ["⠋","⠙","⠸","⢰","⣠","⣄","⡆","⠇"]
    def __init__(self, msg="Memeriksa"):
        self.msg     = msg
        self._stop   = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        i = 0
        while not self._stop.is_set():
            frame = clr(self.FRAMES[i % len(self.FRAMES)], C.CYAN, C.BOLD)
            sys.stdout.write(f"\r  {frame}  {clr(self.msg+'...', C.YELLOW)}   ")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def start(self): self._thread.start()
    def stop(self):
        self._stop.set()
        self._thread.join()
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()

# ═══════════════════════ TAMPIL DAFTAR ═══════════════════════════════════════
def show_list(query=""):
    query = query.strip().lower()
    print(f"\n{clr('  ═══ DAFTAR BANK ═══', C.CYAN, C.BOLD)}")
    for i, (code, name) in enumerate(BANKS, 1):
        if query and query not in name.lower() and query not in code.lower():
            continue
        print(f"  {clr(f'{i:>3}.', C.DIM)} {clr(f'[{code}]', C.CYAN)}  {name}")

    print(f"\n{clr('  ═══ E-WALLET ═══', C.MAGENTA, C.BOLD)}")
    for i, (code, name) in enumerate(EWALLETS, 1):
        if query and query not in name.lower() and query not in code.lower():
            continue
        print(f"  {clr(f'{i:>3}.', C.DIM)} {clr(f'[{code}]', C.MAGENTA)}  {name}")

    print(f"\n  {clr('Total:', C.DIM)} {clr(str(len(BANKS)), C.CYAN)} bank + {clr(str(len(EWALLETS)), C.MAGENTA)} e-wallet\n")

# ═══════════════════════ CONTOH FORMAT ═══════════════════════════════════════
def show_format_examples():
    ex = [
        ("Bank Mandiri",  "mandiri",   "1234567890",   "Nomor rekening"),
        ("BCA",           "bca",       "1234567890",   "Nomor rekening"),
        ("BNI",           "bni",       "0987654321",   "Nomor rekening"),
        ("BRI",           "bri",       "123456789012", "Nomor rekening"),
        ("BSI",           "bsm",       "7123456789",   "Nomor rekening"),
        ("OVO",           "ovo",       "08123456789",  "Nomor HP"),
        ("DANA",          "dana",      "08123456789",  "Nomor HP"),
        ("GoPay",         "gopay",     "08123456789",  "Nomor HP"),
        ("ShopeePay",     "shopeepay", "08123456789",  "Nomor HP"),
        ("LinkAja",       "linkaja",   "08123456789",  "Nomor HP"),
    ]
    print(f"\n{clr('  ═══ CONTOH FORMAT INPUT ═══', C.YELLOW, C.BOLD)}\n")
    print(f"  {'Bank/e-Wallet':<14} {'Kode':<20} {'Nomor':<18} {'Keterangan'}")
    print(f"  {'─'*14}  {'─'*20}  {'─'*18}  {'─'*15}")
    for nama, kode, nomor, ket in ex:
        print(f"  {clr(nama, C.WHITE):<23} {clr(kode, C.CYAN):<29} {clr(nomor, C.GREEN):<18} {clr(ket, C.DIM)}")
    print(f"""
  {clr('Catatan:', C.YELLOW, C.BOLD)}
  • Bank      → masukkan {clr('nomor rekening', C.GREEN)} (10–16 digit)
  • e-Wallet  → masukkan {clr('nomor HP', C.GREEN)} format 08xx atau 628xx
""")

# ═══════════════════════ CALL API ════════════════════════════════════════════
def cek_rekening(account_bank: str, account_number: str):
    payload = urllib.parse.urlencode({
        "account_bank":   account_bank,
        "account_number": account_number,
    })
    headers = {
        "Content-Type":   "application/x-www-form-urlencoded",
        "Content-Length": str(len(payload)),
    }
    try:
        conn = http.client.HTTPSConnection(API_HOST, timeout=TIMEOUT)
        conn.request("POST", API_PATH, payload, headers)
        res  = conn.getresponse()
        body = res.read().decode("utf-8")
        conn.close()
    except OSError as e:
        return None, f"❌  Tidak ada koneksi internet: {e}"
    except Exception as e:
        return None, f"⚠️  Error: {e}"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None, f"⚠️  Respons tidak valid dari server."

    # Sukses
    if res.status == 200:
        holder = (
            data.get("data", {}).get("account_holder")
            or data.get("account_holder")
            or data.get("name")
            or data.get("nama")
        )
        if holder:
            return holder, None
        return None, "⚠️  Rekening ditemukan tapi nama kosong."
    else:
        msg = (
            data.get("message")
            or data.get("error")
            or data.get("msg")
            or f"HTTP {res.status}"
        )
        return None, f"❌  {msg}"

# ═══════════════════════ TAMPIL HASIL ════════════════════════════════════════
def print_result_ok(bank_code, account_number, holder_name):
    bank_name = CODE_MAP.get(bank_code, bank_code.upper())
    print(f"""
{clr("  ┌──────────────────────────────────────────────────────┐", C.GREEN)}
{clr("  │", C.GREEN)} {clr("✅  REKENING DITEMUKAN!", C.GREEN, C.BOLD):<63}{clr("│", C.GREEN)}
{clr("  │", C.GREEN)}                                                       {clr("│", C.GREEN)}
{clr("  │", C.GREEN)}  🎉 Nama Pemilik : {clr(holder_name, C.GREEN, C.BOLD):<43}{clr("│", C.GREEN)}
{clr("  │", C.GREEN)}  🏦 Bank/e-Wallet: {clr(bank_name, C.CYAN):<43}{clr("│", C.GREEN)}
{clr("  │", C.GREEN)}  🔢 No. Rekening : {clr(account_number, C.YELLOW):<43}{clr("│", C.GREEN)}
{clr("  │", C.GREEN)}                                                       {clr("│", C.GREEN)}
{clr("  └──────────────────────────────────────────────────────┘", C.GREEN)}
""")

def print_result_err(msg):
    print(f"""
{clr("  ┌──────────────────────────────────────────────────────┐", C.RED)}
{clr("  │", C.RED)} {clr("❌  REKENING TIDAK DITEMUKAN / ERROR", C.RED, C.BOLD):<63}{clr("│", C.RED)}
{clr("  │", C.RED)}                                                       {clr("│", C.RED)}
{clr("  │", C.RED)}  {clr(str(msg), C.YELLOW):<61}{clr("│", C.RED)}
{clr("  │", C.RED)}                                                       {clr("│", C.RED)}
{clr("  └──────────────────────────────────────────────────────┘", C.RED)}
""")

# ═══════════════════════ INPUT ════════════════════════════════════════════════
def prompt(label, color=C.CYAN):
    try:
        return input(f"  {clr('›', color, C.BOLD)} {clr(label, C.WHITE)}: ").strip()
    except (KeyboardInterrupt, EOFError):
        return "exit"

# ═══════════════════════ MAIN ════════════════════════════════════════════════
def main():
    clear_screen()
    print_banner()

    while True:
        print(clr("  ─────────────────────────────────────────────────", C.DIM))
        print(f"  {clr('list', C.CYAN)} | {clr('cari <nama>', C.CYAN)} | {clr('contoh', C.YELLOW)} | {clr('clear', C.DIM)} | {clr('exit', C.RED)}")
        print(clr("  ─────────────────────────────────────────────────\n", C.DIM))

        bank_input = prompt("Kode Bank / e-Wallet")
        cmd = bank_input.lower()

        if cmd in ("exit", "quit", "q"):
            print(f"\n  {clr('Sampai jumpa! 👋', C.MAGENTA, C.BOLD)}\n")
            break

        if cmd in ("clear", "cls"):
            clear_screen()
            print_banner()
            continue

        if cmd == "list":
            show_list()
            continue

        if cmd.startswith("cari ") or cmd.startswith("search "):
            show_list(query=bank_input.split(" ", 1)[1])
            continue

        if cmd in ("contoh", "format", "help", "?"):
            show_format_examples()
            continue

        if not bank_input:
            print(f"  {clr('⚠  Kode bank tidak boleh kosong!', C.YELLOW)}\n")
            continue

        if bank_input not in CODE_MAP:
            suggestions = [
                f"{clr(c, C.CYAN)} ({n})"
                for c, n in ALL_OPTIONS
                if bank_input.lower() in c.lower() or bank_input.lower() in n.lower()
            ]
            if suggestions:
                print(f"  {clr('⚠  Mungkin maksudmu:', C.YELLOW)}")
                for s in suggestions[:5]:
                    print(f"     → {s}")
            else:
                print(f"  {clr('⚠  Kode tidak dikenal.', C.YELLOW)} Ketik {clr('list', C.CYAN)} untuk melihat semua kode.")
            print()
            continue

        acc_num = prompt("No. Rekening / No. HP")

        if acc_num.lower() in ("exit", "quit", "q"):
            print(f"\n  {clr('Sampai jumpa! 👋', C.MAGENTA, C.BOLD)}\n")
            break

        if not acc_num:
            print(f"  {clr('⚠  Nomor tidak boleh kosong!', C.YELLOW)}\n")
            continue

        if not acc_num.isdigit():
            print(f"  {clr('⚠  Nomor harus berupa angka.', C.YELLOW)}\n")
            continue

        bank_name = CODE_MAP[bank_input]
        spinner = Spinner(f"Mengecek {bank_name}")
        spinner.start()
        holder, err = cek_rekening(bank_input, acc_num)
        spinner.stop()

        if holder:
            print_result_ok(bank_input, acc_num, holder)
        else:
            print_result_err(err or "Rekening tidak ditemukan.")

        again = prompt("Cek rekening lain? (y/n)", color=C.YELLOW)
        if again.lower() not in ("y", "ya", "yes"):
            print(f"\n  {clr('Sampai jumpa! 👋', C.MAGENTA, C.BOLD)}\n")
            break
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {clr('Dibatalkan. Sampai jumpa! 👋', C.MAGENTA, C.BOLD)}\n")
        sys.exit(0)
