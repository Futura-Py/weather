# extra-hooks/hook-DIP_module.py
from PyInstaller.utils.hooks import collect_data_files

datas: list[tuple[str, str]] = collect_data_files("sv_ttk")