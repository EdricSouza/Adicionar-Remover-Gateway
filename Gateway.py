import subprocess
import wmi
import pyautogui

gateway = None
interface = "Ethernet"

# Função construtora de comandos no PowerShell
def commmand_subprocess(command):
    try:
        retorno = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        return retorno
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e.stderr}")
        return e

# Recolher o Gateway do próprio computador
def capturar_gateway():
    try:
        wmi_obj = wmi.WMI()
        wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
        wmi_out = wmi_obj.query(wmi_sql)

        if wmi_out and wmi_out[0].DefaultIPGateway:
            return wmi_out[0].DefaultIPGateway[0]
    except Exception as e:
        print(f"Erro ao obter o gateway: {e}")
    return None

gateway = capturar_gateway()
print(f"Gateway atual: {gateway}")

# Adiciona/Remove Gateway com base na obtenção dos mesmos
if not gateway:
    try:
        command = 'route add 0.0.0.0 mask 0.0.0.0 192.168.0.1'
        retorno = commmand_subprocess(f"powershell.exe -Command \"{command}\"")
        print(f"Saída: {retorno.stdout}")

        if retorno.returncode != 0:
            raise Exception("Erro na execução da função")

        print("Gateway adicionado. Você pode negativar, pressione Enter para fechar o programa...")
        input()
    except Exception as e:
        print(f"Não foi possível executar a função, erro: {e}")

else:
    try:
        command = 'route delete 0.0.0.0 mask 0.0.0.0 192.168.0.1'
        retorno = commmand_subprocess(f"powershell.exe -Command \"{command}\"")
        print(f"Saída: {retorno.stdout}")

        if retorno.returncode != 0:
            raise Exception("Erro na execução da função")

        print("Gateway removido. Acesso permitido às pastas, pressione Enter para fechar o programa...")
        input()
    except Exception as e:
        print(f"Não foi possível executar a função, erro: {e}")