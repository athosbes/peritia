import subprocess
import time
import os
import pyautogui
import pygetwindow as gw

def open_add_remove_programs():
    """Abre a janela 'Desinstalar Programas' ou 'Aplicativos e Recursos' no Windows."""
    # try:
    #     subprocess.run('control appwiz.cpl', shell=True, check=True)  # Tenta abrir o painel de controle
    # except subprocess.CalledProcessError:
    #     print("Falha ao abrir o 'Desinstalar Programas'. Tentando abrir 'Aplicativos e Recursos'.")
    #     subprocess.run('start ms-settings:appsfeatures', shell=True, check=True)  # Alternativa para Windows 10/11
    
    try:
        subprocess.run('control appwiz.cpl', shell=True, check=True)  # Tenta abrir o painel de controle
    except subprocess.CalledProcessError:
        pass  # Ignora o erro e continua
    # try:
    #     subprocess.run('start ms-settings:appsfeatures', shell=True, check=True)  # Alternativa para Windows 10/11
    # except subprocess.CalledProcessError:
    #     pass  # Ignora o erro e continua

def capture_screenshot(output_dir, file_name):
    """Captura uma screenshot da tela inteira e salva no diretório de saída."""
    screenshot = pyautogui.screenshot()
    screenshot_path = os.path.join(output_dir, file_name)
    screenshot.save(screenshot_path)
    return screenshot_path

def scroll_and_capture(window_title, output_dir, screenshot_prefix, scroll_amount=200, capture_delay=0.9, max_screenshots=20):
    """Rola a janela e captura a tela de cada parte visível."""
    # Encontre a janela "Desinstalar Programas" pelo título
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
    except IndexError:
        print("Janela não encontrada!")
        return
    
    # Maximize a janela (se necessário)
    if not window.isMaximized:
        window.maximize()

    # Rola para o in cio da janela
    pyautogui.scroll(10000000)

    # Aguarde algum tempo antes de iniciar
    time.sleep(capture_delay)

    # Defina a posição inicial para rolar
    screenshot_counter = 1
    while True:
        # Captura a tela da janela atual
        screenshot_file = f"{screenshot_prefix}_{screenshot_counter}.png"
        capture_screenshot(output_dir, screenshot_file)
        print(f"Captura de tela salva: {screenshot_file}")

        # Aguarde algum tempo antes de rolar
        time.sleep(capture_delay)

        # Role a janela usando pyautogui
        pyautogui.scroll(-scroll_amount)  # Rolagem para baixo

        # Aumenta o contador de captura de tela
        screenshot_counter += 1

        # Verifique se o número máximo de capturas foi alcançado
        if screenshot_counter > max_screenshots:  # Ajuste conforme necessário
            print("Número máximo de capturas alcançado.")
            break

def main():
    # Defina o título da janela, o diretório de saída e o prefixo para os screenshots
    window_title = "Programas e Recursos"  # O título pode variar, então ajuste conforme necessário
    output_dir = os.path.join(os.getcwd(), "screenshots")
    screenshot_prefix = "uninstall_programs"

    print("Salvando na pasta:", output_dir)

    # Verifique se o diretório de saída existe, senão, crie-o
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Abra a janela "Desinstalar Programas"
    print("Abrindo a janela 'Desinstalar Programas' ou 'Aplicativos e Recursos'...")
    open_add_remove_programs()

    # Aguarde alguns segundos para a janela carregar
    time.sleep(3)

    # Rolar a janela e capturar as imagens
    print("Iniciando a captura de tela...")
    scroll_and_capture(window_title, output_dir, screenshot_prefix)

if __name__ == "__main__":
    main()
