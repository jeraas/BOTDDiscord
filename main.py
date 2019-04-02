import discord
import asyncio
import requests
import re
from random import choice

jogando = False

client = discord.Client()

@client.event
async def on_ready():
    print('Ready')

@client.event
async def on_message(message):
    if message.content.split()[0] == 'j;site':
        try:
            site = message.content.split()[1]
            find = re.findall(r'http', site)
            if not find:
                site = 'http://' + site
        except Exception as e:
            await client.send_message(message.channel, 'Erro: {}'.format(e))
            return
        req = requests.get(site)
        if int(req.status_code) == 200:
            await client.send_message(message.channel, 'Código 200, site no ar.')
        else:
            await client.send_message(message.channel, 'Código {}'.format(str(req.status_code)))
    if message.content.split()[0] == 'j;forca':
        global jogando
        if jogando == False:
            jogando = True
            await client.send_message(message.channel, 'Jogo iniciado!')
            palavras = 'canguru amazonas maça comer dormir caçar arvore geladeira celular computador notebook ventilador python pera laranja limao boi vaca tigre onça peixe amor amar leao norte sul leste oeste tabua teclado mesa game jogo mouse pendrive tecla adesivo'.split()
            palavra = choice(palavras)
            palavraOcultada = []
            letrasUsadas = []
            vidas = 5

            for letra in palavra:
                palavraOcultada.append('- ')

            embed = discord.Embed(title="Jogo da Forca", color=0x5314d3)
            embed.add_field(name='Palavra: ', value="".join(palavraOcultada), inline=False)
            embed.add_field(name='Vidas restantes: ', value='❤' * vidas, inline=False)

            await client.send_message(message.channel, embed=embed)
            while vidas > 0:
                palpite = await client.wait_for_message(channel=message.channel, author=None, timeout=None)


                i = 0
                if palpite:
                    if palpite.content.split()[0] == 'j;forca' and jogando == True:
                        await client.send_message(message.channel, 'Outro jogo em andamento!')
                    elif palpite.content.split()[0] == 'j;sair' and jogando == True:
                        jogando = False
                        await client.send_message(message.channel, 'Saindo...')
                        break
                    else:
                        if palpite.content == palavra:
                            await client.send_message(message.channel, 'Você venceu o jogo!')
                            jogando = False
                            return
                        if palpite.content[0] in letrasUsadas:
                            await client.send_message(message.channel, 'Você já usou essa letra.')
                            continue
                        letrasUsadas.append(palpite.content[0])
                        achou = False
                        for letra in palavra:
                            if palpite.content == palavra:
                                jogando = False
                                await client.send_message(message.channel, 'Você venceu o jogo!')
                                return
                            if palpite.content[0] == letra:
                                palavraOcultada[i] = palpite.content[0]
                                achou = True
                            i = i + 1
                        if achou == False:
                            vidas = vidas - 1
                        if "".join(palavraOcultada) == palavra:
                            await client.send_message(message.channel, 'Parabéns, você ganhou o jogo.')
                            jogando = False
                            break
                        if vidas == 0:
                            await client.send_message(message.channel, 'Você perdeu todas as vidas! A palavra era: {}'.format(palavra))
                            jogando = False
                            break
                        embed = discord.Embed(title="Jogo da Forca", color=0x5314d3)
                        embed.add_field(name='Palavra: ', value="".join(palavraOcultada), inline=False)
                        embed.add_field(name='Letras usadas: ', value="".join(letrasUsadas), inline=False)
                        embed.add_field(name='Vidas restantes: ', value='❤' * vidas, inline=False)
                        await client.send_message(message.channel, embed=embed)

client.run('NTYyMDUxMTYwODY5OTYxNzMx.XKFKIg.-onhsJN3jZA_MJqOakxwyiMKo3A')