import asyncio
import threading
import os
import time
import json
from colorama import Fore, Back, Style, init
import discord
from discord.ext import commands

init(autoreset=True)

VERSION = 'V1 '
users = 1
raids_feitos = 0
bots_online = 1
criadores = 1

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.json")

TEMAS = {
    "azul": {"fore": Fore.BLUE, "back": Back.WHITE},
    "verde": {"fore": Fore.GREEN, "back": Back.BLACK},
    "vermelho": {"fore": Fore.RED, "back": Back.WHITE},
    "roxo": {"fore": Fore.MAGENTA, "back": Back.BLACK},
    "padrao": {"fore": Fore.WHITE, "back": Back.BLUE}
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def atualizar_titulo():
    while True:
        os.system(f"title VaiXourar │ Users: {users} │ Raids: {raids_feitos} │ Bots: {bots_online} │ Criador: Garotinn / {criadores}")
        time.sleep(2)

threading.Thread(target=atualizar_titulo, daemon=True).start()

def load_data():
    if not os.path.exists(USERS_FILE):
        return {"usuarios": {}}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

INFZRNAL_ART_RAW = """
##   ##    ###     ######  ###  ##   #####   ##   ##  ######     ###    ######
##   ##   ## ##      ##    ###  ##  ### ###  ##   ##   ##  ##   ## ##    ##  ##
##   ##  ##   ##     ##     #####   ##   ##  ##   ##   ##  ##  ##   ##   ##  ##
 ## ##   ##   ##     ##      ###    ##   ##  ##   ##   #####   ##   ##   #####
 ## ##   #######     ##     #####   ##   ##  ##   ##   ## ##   #######   ## ##
  ###    ##   ##     ##    ##  ###  ### ###  ##   ##   ## ##   ##   ##   ## ##
  ###    ##   ##   ######  ##  ###   #####    #####   #### ##  ##   ##  #### ##

╔═════╩══════════════════╦═════════════════════════╦══════════════════╩═════╗  
╩ (1)< Excluir Canais      (6) < Criar Canal        (11) < Spam Test        ╩   
  (2)< Listar Perms        (7) < Webhooks Info      (12) < Check Updates      
  (3)< Auditoria Logs      (8) < Banner Grab        (13) < Banir Todos        
  (4)< Roles Críticos      (9) < Créditos           (14) < Mudar Nome Server 
╦ (5)< Mudar Nome Membros  (10)< Enviar DM Todos                            ╦
╚═════╦══════════════════╩═════════════════════════╩══════════════════╦═════╝  
                      (15) < Exit
"""

def print_ascii(tema):
    term_width = os.get_terminal_size().columns
    fore = TEMAS[tema]["fore"]
    print("\n".join(fore + line.center(term_width) for line in INFZRNAL_ART_RAW.splitlines()))

def custom_prompt(user: str = "user", tema: str = "padrao") -> str:
    deco = f"{TEMAS[tema]['fore']}{Style.BRIGHT}-@VaiXourar{Style.RESET_ALL}"
    return f"{Fore.WHITE}{TEMAS[tema]['back']}{user}{Style.RESET_ALL}/ {deco}: "

# --- Semáforos ---
semaphore_channels = asyncio.Semaphore(50)
semaphore_spam = asyncio.Semaphore(50)

# --- Funções Discord ---
async def safe_delete_channel(ch):
    async with semaphore_channels:
        try:
            await ch.delete()
        except:
            pass

async def excluir_canais(guild):
    global raids_feitos
    print(Fore.CYAN + "[!] Excluindo canais...")
    tasks = [safe_delete_channel(ch) for ch in guild.channels]
    await asyncio.gather(*tasks)
    raids_feitos += 1
    print(Fore.BLUE + "Todos os canais deletados!")
    input("ENTER para voltar...")

async def safe_create_channel(guild, name):
    async with semaphore_channels:
        try:
            return await guild.create_text_channel(name)
        except:
            return None

async def criar_canais(guild, name, amount):
    try:
        amount = int(amount)
    except:
        amount = 50
    print(Fore.CYAN + f"[!] Criando {amount} canais '{name}'...")
    tasks = [safe_create_channel(guild, name) for _ in range(amount)]
    await asyncio.gather(*tasks)
    print(Fore.BLUE + "Canais criados!")

async def spam_all(guild, msg, total):
    channels = [ch for ch in guild.text_channels]
    if not channels:
        print(Fore.RED + "Nenhum canal para spam!")
        return
    per_channel = max(1, total // len(channels))
    tasks = [ch.send(msg) for ch in channels for _ in range(per_channel)]
    await asyncio.gather(*tasks)
    print(Fore.BLUE + "Spam concluído!")

async def banir_todos(guild):
    print(Fore.CYAN + "[!] Banindo todos os membros...")
    members = [m for m in guild.members if not m.bot and m.id != guild.owner_id]
    tasks = [m.ban(reason="VaiXourar") for m in members]
    await asyncio.gather(*tasks)
    print(Fore.BLUE + "Banimento completo!")

async def mudar_nome_server(guild, novo_nome):
    try:
        await guild.edit(name=novo_nome)
        print(Fore.GREEN + f"Nome do servidor alterado para {novo_nome}")
    except:
        print(Fore.RED + "Erro ao mudar o nome do servidor.")
    input("ENTER para voltar...")

async def enviar_dm_todos(guild, mensagem):
    print(Fore.CYAN + "[!] Enviando DMs para todos os membros...")
    enviados = 0
    falhas = 0
    for member in guild.members:
        if member.bot:
            continue
        try:
            await member.send(mensagem)
            enviados += 1
        except:
            falhas += 1
    print(Fore.GREEN + f"✅ DMs enviadas: {enviados}, Falhas: {falhas}")
    input("ENTER para voltar...")

async def mudar_nome_membros(guild, novo_nome):
    print(Fore.CYAN + "[!] Mudando nick de todos os membros...")
    alterados = 0
    falhas = 0
    for member in guild.members:
        if member.bot or member == guild.owner:
            continue
        try:
            await member.edit(nick=novo_nome)
            alterados += 1
        except:
            falhas += 1
    print(Fore.GREEN + f"✅ Nomes alterados: {alterados}, Falhas: {falhas}")
    input("ENTER para voltar...")

async def listar_permissoes(guild):
    print(Fore.CYAN + "[!] Listando permissões dos membros...")
    for member in guild.members:
        print(f"{member}: {member.guild_permissions}")
    input("ENTER para voltar...")

async def auditoria_logs(guild):
    print(Fore.CYAN + "[!] Mostrando auditoria logs...")
    async for entry in guild.audit_logs(limit=10):
        print(f"{entry.user} -> {entry.action} -> {entry.target}")
    input("ENTER para voltar...")

async def roles_criticos(guild):
    print(Fore.CYAN + "[!] Listando roles críticos...")
    for role in guild.roles:
        if role.permissions.administrator or role.permissions.manage_guild:
            print(f"{role.name} - {role.permissions}")
    input("ENTER para voltar...")

async def webhooks_info(guild):
    print(Fore.CYAN + "[!] Listando Webhooks...")
    for channel in guild.text_channels:
        hooks = await channel.webhooks()
        for hook in hooks:
            print(f"{channel.name}: {hook.name} - {hook.url}")
    input("ENTER para voltar...")

async def banner_grab(guild):
    print(Fore.CYAN + "[!] Banner do servidor:")
    if guild.banner:
        print(guild.banner.url)
    else:
        print("Sem banner.")
    input("ENTER para voltar...")

async def check_updates():
    print(Fore.CYAN + "[!] Check Updates...")
    print("Nenhuma atualização disponível.")
    input("ENTER para voltar...")

# --- Painel ---
async def painel_menu(bot, guild_id, user_name, tema):
    guild = discord.utils.get(bot.guilds, id=int(guild_id))
    if not guild:
        print(Fore.RED + "[ERRO] Servidor não encontrado.")
        return

    while True:
        clear()
        print_ascii(tema)
        print(Fore.BLUE + f"\nServidor: {guild.name} ({guild.member_count} membros)")
        escolha = input(custom_prompt(user_name, tema)).strip()

        if escolha == "1":
            await excluir_canais(guild)
        elif escolha == "2":
            await listar_permissoes(guild)
        elif escolha == "3":
            await auditoria_logs(guild)
        elif escolha == "4":
            await roles_criticos(guild)
        elif escolha == "5":
            novo_nome = input("Novo nick para todos: ").strip()
            await mudar_nome_membros(guild, novo_nome)
        elif escolha == "6":
            name = input("Nome do canal: ").strip()
            amount = input("Quantidade: ").strip()
            await criar_canais(guild, name, amount)
        elif escolha == "7":
            await webhooks_info(guild)
        elif escolha == "8":
            await banner_grab(guild)
        elif escolha == "9":
            print(Fore.BLUE + "Créditos: Black-")
            input("ENTER para voltar...")
        elif escolha == "10":
            msg = input("Mensagem para todos: ").strip()
            await enviar_dm_todos(guild, msg)
        elif escolha == "11":
            msg = input("Mensagem de spam: ").strip()
            total = int(input("Quantidade total: "))
            await spam_all(guild, msg, total)
        elif escolha == "12":
            await check_updates()
        elif escolha == "13":
            await banir_todos(guild)
        elif escolha == "14":
            novo_nome = input("Novo nome do servidor: ").strip()
            await mudar_nome_server(guild, novo_nome)
        elif escolha == "15":
            print(Fore.BLUE + "Saindo do painel...")
            await bot.close()
            break
        else:
            print(Fore.RED + "Opção inválida!")
            time.sleep(1)

# --- Funções de perfil e tela inicial ---
def perfil_menu(usuario, user_data):
    while True:
        clear()
        tema = user_data.get("tema", "padrao")
        print(Fore.BLUE + f"=== Perfil: {usuario} ===\n")
        print("1) Cadastrar novo bot")
        print("2) Usar bot cadastrado")
        print("3) Remover bot")
        print("4) Ver perfil / estatísticas")
        print("5) Mudar tema")
        print("6) Voltar à tela inicial\n")
        choice = input(Fore.CYAN + "Escolha uma opção: ").strip()

        if choice == "1":
            token = input("Token do bot: ").strip()
            bot_name = input("Nome do bot: ").strip()
            guild_name = input("Nome do servidor: ").strip()
            guild_id = input("ID do servidor: ").strip()
            user_data["bots"].append({
                "token": token,
                "user_name": bot_name,
                "guild_name": guild_name,
                "guild_id": guild_id
            })
            save_data(data)
            print(Fore.GREEN + "Bot cadastrado com sucesso!")
            time.sleep(1)
        elif choice == "2":
            if not user_data["bots"]:
                print(Fore.RED + "Nenhum bot cadastrado!")
                time.sleep(2)
                continue
            for i, b in enumerate(user_data["bots"]):
                print(f"{i+1}) {b['user_name']} - {b['guild_name']} (ID: {b['guild_id']})")
            idx = int(input("Escolha um bot para usar: ")) - 1
            if 0 <= idx < len(user_data["bots"]):
                bot_data = user_data["bots"][idx]
                start_bot(bot_data["token"], usuario, bot_data["guild_id"], tema)
                break
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
        elif choice == "3":
            if not user_data["bots"]:
                print(Fore.RED + "Nenhum bot para remover!")
                time.sleep(2)
                continue
            for i, b in enumerate(user_data["bots"]):
                print(f"{i+1}) {b['user_name']} - {b['guild_name']} (ID: {b['guild_id']})")
            idx = int(input("Escolha um bot para remover: ")) - 1
            if 0 <= idx < len(user_data["bots"]):
                removed = user_data["bots"].pop(idx)
                save_data(data)
                print(Fore.GREEN + f"Bot {removed['user_name']} removido!")
                time.sleep(1)
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
        elif choice == "4":
            stats = user_data.get("stats", {"raids_feitos":0, "canais_criados":0})
            print(Fore.CYAN + f"\n=== Estatísticas de {usuario} ===")
            print(Fore.BLUE + f"Raids realizados: {stats['raids_feitos']}")
            print(Fore.BLUE + f"Canais criados/excluídos: {stats['canais_criados']}")
            print(Fore.BLUE + f"Bots cadastrados: {len(user_data['bots'])}")
            input("ENTER para voltar...")
        elif choice == "5":
            print("\nTemas disponíveis:")
            for t in TEMAS:
                print(f"- {t}")
            novo_tema = input("Escolha o tema: ").strip().lower()
            if novo_tema in TEMAS:
                user_data["tema"] = novo_tema
                save_data(data)
                print(Fore.GREEN + "Tema atualizado!")
                time.sleep(1)
            else:
                print(Fore.RED + "Tema inválido!")
                time.sleep(1)
        elif choice == "6":
            break
        else:
            print(Fore.RED + "Opção inválida!")
            time.sleep(1)

def tela_inicial():
    while True:
        clear()
        print(Fore.BLUE + "=== VaiXourar BOT MANAGER ===\n")
        print("1) Criar perfil")
        print("2) Usar perfil existente")
        print("3) Alterar tema de um perfil\n")
        choice = input(Fore.CYAN + "Escolha uma opção: ").strip()

        if choice == "1":
            usuario = input("Digite seu nome: ").strip()
            if usuario in data["usuarios"]:
                print(Fore.RED + "Perfil já existe!")
                time.sleep(2)
                continue
            print("\nTemas disponíveis:")
            for t in TEMAS:
                print(f"- {t}")
            tema = input("Escolha um tema: ").strip().lower()
            if tema not in TEMAS:
                tema = "padrao"
            data["usuarios"][usuario] = {"bots": [], "stats": {"raids_feitos":0, "canais_criados":0}, "tema": tema}
            save_data(data)
            perfil_menu(usuario, data["usuarios"][usuario])
        elif choice == "2":
            if not data["usuarios"]:
                print(Fore.RED + "Nenhum perfil cadastrado!")
                time.sleep(2)
                continue
            for i, u in enumerate(data["usuarios"].keys()):
                print(f"({i+1}) {u}")
            idx = int(input("Escolha um perfil: ")) - 1
            usuarios_list = list(data["usuarios"].keys())
            if 0 <= idx < len(usuarios_list):
                usuario = usuarios_list[idx]
                perfil_menu(usuario, data["usuarios"][usuario])
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
        elif choice == "3":
            if not data["usuarios"]:
                print(Fore.RED + "Nenhum perfil cadastrado!")
                time.sleep(2)
                continue
            for i, u in enumerate(data["usuarios"].keys()):
                print(f"{i+1}) {u}")
            idx = int(input("Escolha um perfil para mudar o tema: ")) - 1
            usuarios_list = list(data["usuarios"].keys())
            if 0 <= idx < len(usuarios_list):
                usuario = usuarios_list[idx]
                print("\nTemas disponíveis:")
                for t in TEMAS:
                    print(f"- {t}")
                novo_tema = input("Escolha o novo tema: ").strip().lower()
                if novo_tema in TEMAS:
                    data["usuarios"][usuario]["tema"] = novo_tema
                    save_data(data)
                    print(Fore.GREEN + f"Tema do perfil {usuario} atualizado!")
                else:
                    print(Fore.RED + "Tema inválido!")
                time.sleep(1)
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
        else:
            print(Fore.RED + "Opção inválida!")
            time.sleep(1)

def start_bot(token, user_name, guild_id, tema):
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        clear()
        await painel_menu(bot, guild_id, user_name, tema)

    bot.run(token)

if __name__ == "__main__":
    data = load_data()
    tela_inicial()
