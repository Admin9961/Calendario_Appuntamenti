import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox, simpledialog
import ctypes
import threading
import time
import os
import sys

def mostra_finestra():
    root.deiconify()

def nascondi_finestra():
    root.iconify()

def chiudi_finestra(event):
    nascondi_finestra()
    root.protocol("WM_DELETE_WINDOW", mostra_finestra)

def prenota_appuntamento():
    data_selezionata = cal.get_date()
    ora_selezionata = time_entry.get()

    data_ora_selezionate = f"{data_selezionata} {ora_selezionata}"

    descrizione = simpledialog.askstring("Descrivi Appuntamento", "Inserisci la descrizione dell'appuntamento:")
    if descrizione:
        messagebox.showinfo("Descrizione", f"Descrizione dell'appuntamento: {descrizione}")
        salva_appuntamento(data_ora_selezionate, descrizione)

def get_script_directory():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def get_next_appointment_number(script_directory):
    appointment_files = [f for f in os.listdir(script_directory) if f.startswith("APPUNTAMENTO_")]
    return len(appointment_files) + 1

def salva_appuntamento(data_ora, descrizione):
    script_directory = get_script_directory()
    next_appointment_number = get_next_appointment_number(script_directory)
    file_path = os.path.join(script_directory, f"APPUNTAMENTO_{next_appointment_number}.txt")

    with open(file_path, "w") as file:
        file.write(f"Appuntamento prenotato per: {data_ora}\n")
        file.write(f"Descrizione: {descrizione}\n")

def avvia_processo_in_background():
    global shutdown_event
    shutdown_event = threading.Event()
    background_thread = threading.Thread(target=processo_background)
    background_thread.daemon = True
    background_thread.start()

def processo_background():
    while not shutdown_event.is_set():
        print("Icona in background")
        time.sleep(5)

def on_notify(icon_id, msg_id, data):
    if msg_id == 1:
        mostra_finestra()
    elif msg_id == 2:
        nascondi_finestra()
    elif msg_id == 3:
        prenota_appuntamento()
    elif msg_id == 4:
        avvia_processo_in_background()

def create_tray_icon(window_handle):
    class NOTIFYICONDATAW(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_uint),
            ("hWnd", ctypes.c_void_p),
            ("uID", ctypes.c_uint),
            ("uFlags", ctypes.c_uint),
            ("uCallbackMessage", ctypes.c_uint),
            ("hIcon", ctypes.c_void_p),
            ("szTip", ctypes.c_wchar * 128),
        ]

    nid = NOTIFYICONDATAW()
    nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
    nid.hWnd = window_handle
    nid.uID = 1
    nid.uFlags = 0x00000001 | 0x00000002 | 0x00000004
    nid.uCallbackMessage = 0
    nid.hIcon = ctypes.windll.user32.LoadIconW(0, ctypes.c_uint(32512))
    nid.szTip = "Calendario Prenotazioni"
    ctypes.windll.shell32.Shell_NotifyIconW(0, ctypes.byref(nid))

def destroy_tray_icon(window_handle):
    icon_id = 1
    nid = (
        window_handle,
        icon_id
    )
    ctypes.windll.shell32.Shell_NotifyIconW(2, nid)

def on_menu_command(command_id):
    if command_id == 1:
        mostra_finestra()
    elif command_id == 2:
        nascondi_finestra()
    elif command_id == 3:
        prenota_appuntamento()
    elif command_id == 4:
        avvia_processo_in_background()

def descrivi_appuntamento():
    descrizione = simpledialog.askstring("Descrivi Appuntamento", "Inserisci la descrizione dell'appuntamento:")
    if descrizione:
        messagebox.showinfo("Descrizione", f"Descrizione dell'appuntamento: {descrizione}")
        salva_appuntamento(cal.get_date(), descrizione)

root = tk.Tk()
root.title("Calendario Prenotazioni")
root.geometry("800x600")

cal = Calendar(root, selectmode="day", year=2024, month=1, day=6, locale='it_IT')
cal.pack(padx=10, pady=10)

time_entry_label = tk.Label(root, text="Indica la data nella griglia, inserisci l'ora e i minuti (es. 17.20) e prenota!")
time_entry_label.pack(padx=10, pady=5)

time_entry = tk.Entry(root)
time_entry.pack(padx=10, pady=10)

prenota_button = tk.Button(root, text="Prenota Appuntamento", command=prenota_appuntamento)
prenota_button.pack(pady=10)

firma_label = tk.Label(root, text="Software generato da Christopher Zonta © Tutti i diritti riservati 😎")
firma_label.pack()

window_handle = root.winfo_id()
create_tray_icon(window_handle)

menu = (
    ("Mostra Finestra", 1),
    ("Nascondi Finestra", 2),
    ("Prenota Appuntamento", 3),
    ("Avvia Processo in Background", 4),
)
ctypes.windll.user32.InsertMenuW(ctypes.c_int(0), ctypes.c_uint(-1), ctypes.c_uint(0x00000400), ctypes.c_uint(1), ctypes.c_wchar_p("Menu"))
for item, command_id in menu:
    ctypes.windll.user32.InsertMenuW(ctypes.c_int(0), ctypes.c_uint(-1), ctypes.c_uint(0x00000000), ctypes.c_uint(command_id), ctypes.c_wchar_p(item))

callback_type = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_int)
callback = callback_type(on_menu_command)
ctypes.windll.user32.SetMenuDefaultItem(ctypes.c_int(0), ctypes.c_uint(1), ctypes.c_uint(0))
ctypes.windll.user32.SetMenuInfo(ctypes.c_int(0), ctypes.pointer(ctypes.c_int(1)))

callback_type = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p)
callback = callback_type(on_notify)
ctypes.windll.user32.WNDPROC = callback
root.bind("<Destroy>", chiudi_finestra)

root.mainloop()