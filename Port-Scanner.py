# ============================================
# Port Scanner Tool with Professional Banner
# Authors: Arash
# Description: Terminal-based Port Scanner with ASCII banner, colored output, threading, service detection, and result logging
# ابزار اسکنر پورت با پایتون
# شامل بنر ASCII، رنگی بودن خروجی، Threading، شناسایی سرویس‌ها و ذخیره نتایج
# ============================================

import socket
import threading
import time
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
# راه‌اندازی colorama برای پشتیبانی از رنگ‌ها در ترمینال
init(autoreset=True)

# Dictionary of common ports and their services
# دیکشنری پورت‌های رایج و سرویس‌های مربوطه
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
}

# Global variables
# متغیرهای عمومی
results = []
lock = threading.Lock()  # For thread-safe operations / برای عملیات thread-safe

# Function to scan each port
# تابع اسکن هر پورت
def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ایجاد سوکت / Create socket
        sock.settimeout(1)  # زمان انتظار ۱ ثانیه / Timeout = 1 second
        res = sock.connect_ex((target, port))  # تلاش اتصال به پورت / Try connecting to port
        sock.close()  # بستن سوکت / Close socket
        if res == 0:
            with lock:  # قفل برای جلوگیری از تداخل / Lock for thread-safety
                results.append(port)  # اضافه کردن پورت باز / Append open port
    except:
        pass  # نادیده گرفتن خطاها / Ignore errors

# Function to display the ASCII banner and info
# تابع نمایش بنر ASCII و اطلاعات
def display_banner():
    banner = f"""
{Fore.RED}
#                                                                                                                    
#    @@@@@@@    @@@@@@   @@@@@@@   @@@@@@@      @@@@@@    @@@@@@@   @@@@@@   @@@  @@@  @@@  @@@  @@@@@@@@  @@@@@@@   
#    @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@     @@@@@@@   @@@@@@@@  @@@@@@@@  @@@@ @@@  @@@@ @@@  @@@@@@@@  @@@@@@@@  
#    @@!  @@@  @@!  @@@  @@!  @@@    @@!       !@@       !@@       @@!  @@@  @@!@!@@@  @@!@!@@@  @@!       @@!  @@@  
#    !@!  @!@  !@!  @!@  !@!  @!@    !@!       !@!       !@!       !@!  @!@  !@!!@!@!  !@!!@!@!  !@!       !@!  @!@  
#    @!@@!@!   @!@  !@!  @!@!!@!     @!!       !!@@!!    !@!       @!@!@!@!  @!@ !!@!  @!@ !!@!  @!!!:!    @!@!!@!   
#    !!@!!!    !@!  !!!  !!@!@!      !!!        !!@!!!   !!!       !!!@!!!!  !@!  !!!  !@!  !!!  !!!!!:    !!@!@!    
#    !!:       !!:  !!!  !!: :!!     !!:            !:!  :!!       !!:  !!!  !!:  !!!  !!:  !!!  !!:       !!: :!!   
#    :!:       :!:  !:!  :!:  !:!    :!:           !:!   :!:       :!:  !:!  :!:  !:!  :!:  !:!  :!:       :!:  !:!  
#     ::       ::::: ::  ::   :::     ::       :::: ::    ::: :::  ::   :::   ::   ::   ::   ::   :: ::::  ::   :::  
#     :         : :  :    :   : :     :        :: : :     :: :: :   :   : :  ::    :   ::    :   : :: ::    :   : :  
#                                                                                                                    
"""
    print(banner)  # نمایش بنر ASCII / Show ASCII banner
    print(Fore.CYAN + "Creator: ARASH-SAVAK")  # نام سازنده / Author
    print(Fore.YELLOW + "Website: a-darkmountain.github.io/wizard-website/")  # لینک وبسایت / Website
    print(Fore.MAGENTA + "GitHub: a-darkmountain")  # لینک گیت‌هاب / GitHub
    print(Style.RESET_ALL)
    print(Fore.BLUE + "="*60 + "\n")  # خط جداکننده / Separator line

# Main scanner function
# تابع اصلی اسکنر
def port_scanner():
    display_banner()  # نمایش بنر / Show banner
    # Get target and port range / گرفتن هدف و بازه پورت
    target = input("[*] Enter IP or domain: ").strip()
    start_port = int(input("[*] Enter start port: "))
    end_port = int(input("[*] Enter end port: "))

    print(f"\n[*] Starting scan on {target} from port {start_port} to {end_port} ...\n")
    start_time = time.time()  # شروع زمان / Start timer

    # Create and start threads / ساخت و اجرای تردها
    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    # Wait for all threads to finish / منتظر ماندن برای اتمام همه تردها
    for t in threads:
        t.join()

    end_time = time.time()  # پایان زمان / End timer
    duration = end_time - start_time
    results.sort()  # مرتب‌سازی پورت‌های باز / Sort open ports

    # Display results / نمایش نتایج
    if results:
        print(Fore.GREEN + "[+] Open ports found:\n")
        for port in results:
            service = COMMON_PORTS.get(port, "Unknown")  # پیدا کردن سرویس / Get service name
            print(Fore.GREEN + f"Port {port} is open | Service: {service}")
    else:
        print(Fore.RED + "[-] No open ports found.")  # اگر پورتی باز نبود / No ports open

    # Summary / خلاصه
    print(Fore.CYAN + f"\n[*] Total open ports: {len(results)}")
    print(Fore.CYAN + f"[*] Scan duration: {duration:.2f} seconds")

    # Save results to file / ذخیره نتایج در فایل
    with open("result.txt", "w", encoding="utf-8") as f:
        if results:
            f.write("Open ports:\n")
            for port in results:
                service = COMMON_PORTS.get(port, "Unknown")
                f.write(f"{port} - {service}\n")
        else:
            f.write("No open ports found.\n")
        f.write(f"\nScan duration: {duration:.2f} seconds\n")

    print(Fore.BLUE + "\n[+] Results saved in result.txt")  # پیام ذخیره / Save message

# Run the program
# اجرای برنامه
if __name__ == "__main__":
    port_scanner()

payan = input()  # توقف برای بستن برنامه توسط کاربر / Pause before exit
