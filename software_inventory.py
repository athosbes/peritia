import os
import subprocess
import csv
import hashlib
from datetime import datetime
import winreg
import wmi

def get_machine_uuid():
    """Obtém o UUID da máquina usando WMI."""
    c = wmi.WMI()
    for item in c.Win32_ComputerSystemProduct():
        return item.UUID
    return "Unknown"

def get_mac_address():
    """Obtém o endereço MAC da primeira interface de rede usando WMI."""
    c = wmi.WMI()
    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        return interface.MACAddress
    return "Unknown"

# Obtendo identificadores únicos
machine_uuid = get_machine_uuid()
mac_address = get_mac_address().replace(":", "").replace("-", "")  # Remove caracteres indesejados
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(os.getcwd(), f"software_inventory_{machine_uuid}_{mac_address}_{timestamp}")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def run_command(command):
    """Executa um comando e retorna sua saída."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return None

def get_wmic_data():
    """Obtém dados de softwares instalados usando WMIC e salva em CSV."""
    command = 'wmic product get /format:csv'
    output = run_command(command)
    output_path = os.path.join(output_dir, "wmic_products.csv")
    
    # Processa a saída do WMIC para CSV
    with open(output_path, 'w') as file:
        file.write(output)

    # Limpar linhas em branco do arquivo CSV
    with open(output_path, 'r') as file:
        lines = [line for line in file if line.strip()]
    
    with open(output_path, 'w') as file:
        file.writelines(lines)
    
    return output_path

def get_winget_data():
    """Obtém dados de softwares instalados usando Winget e salva em CSV."""
    command = 'winget list --nowarn --ignore-warnings '
    output = run_command(command)
    output_path = os.path.join(output_dir, "winget_list.csv")
    
    # Processa a saída do Winget para CSV
    with open(output_path, 'w') as file:
        file.write(output)
    
    return output_path

def get_installed_software_from_registry():
    """Obtém dados de softwares instalados a partir do registro do Windows e salva em CSV."""
    software_list = []
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    for reg_path in reg_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    subkey_path = f"{reg_path}\\{subkey_name}"
                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as subkey:
                            software_data = {
                                key: winreg.QueryValueEx(subkey, key)[0] if key in [winreg.EnumValue(subkey, j)[0] for j in range(winreg.QueryInfoKey(subkey)[1])] else 'N/A'
                                for key in ['DisplayName', 'InstallDate', 'Publisher', 'DisplayVersion', 'UninstallString', 'QuietUninstallString', 'InstallLocation']
                            }
                            # Convertendo data para formato padrão
                            software_data['InstallDate'] = datetime.strptime(software_data['InstallDate'], '%Y%m%d').strftime('%Y-%m-%d') if software_data['InstallDate'].isdigit() else 'N/A'
                            software_list.append(software_data)
                    except OSError as e:
                        print(f"Erro ao acessar subchave: {e}")
        except OSError as e:
            print(f"Erro ao acessar chave do registro: {e}")

    output_path = os.path.join(output_dir, "installed_software.csv")
    keys = software_list[0].keys() if software_list else []
    
    with open(output_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(software_list)
    
    return output_path

def save_hashes(file_paths):
    """Gera e salva os hashes de todos os arquivos."""
    hashes = {}
    for file_path in file_paths:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        hashes[file_path] = sha256.hexdigest()
    
    hash_file_path = os.path.join(output_dir, "file_hashes.csv")
    with open(hash_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Path', 'SHA-256 Hash'])
        for file_path, file_hash in hashes.items():
            writer.writerow([file_path, file_hash])
    
    return hash_file_path

# Execução das funções
wmic_csv = get_wmic_data()
winget_csv = get_winget_data()
registry_csv = get_installed_software_from_registry()

files = [wmic_csv, winget_csv, registry_csv]
hashes_csv = save_hashes(files)

print(f"Dados salvos em: {output_dir}")
print(f"Hashes salvos em: {hashes_csv}")
