import logging
from telethon import TelegramClient, events

# Informations API Telegram
api_id = 312117193
api_hash = "VOTRE_API_HASH"

# Initialisation du client
client = TelegramClient("session_serveur", api_id, api_hash)

logging.basicConfig(level=logging.INFO)

# Sources à surveiller
SOURCES = [
    "Soumaila Sidibe CLM",
    "Cisse Movie",
    "Abou N'baye",
    "Diarra Movie",
    "Badial Movie",
    "Mamadou Movie",
    "TRADUCTEUR COULIBALY 💯",
    "Traduction Vieux Diarra",
    "Soul Movie",
]

# Destinations
DESTINATION_1 = "BAMANAKAN"
DESTINATION_2 = "Cisse Movie"

compteurs_fichiers = {}


@client.on(events.NewMessage(chats=SOURCES))
async def transfer_file(event):
    expediteur = event.chat_id

    nom_expediteur = (
        getattr(event.chat, "title", None)
        or getattr(event.chat, "username", None)
        or "Contact"
    )

    if expediteur not in compteurs_fichiers:
        compteurs_fichiers[expediteur] = 0

    # Vérification vidéo uniquement
    if event.video or (
        event.document
        and event.document.mime_type
        and event.document.mime_type.startswith("video/")
    ):
        taille_mo = event.file.size / (1024 * 1024)
        nom_fichier = event.file.name or "Film"

        if taille_mo >= 20:
            if compteurs_fichiers[expediteur] < 100:
                compteurs_fichiers[expediteur] += 1

                print(
                    f"[{nom_expediteur}] Film valide "
                    f"n°{compteurs_fichiers[expediteur]}/100 détecté : "
                    f"{nom_fichier} ({taille_mo:.2f} Mo)"
                )

                await client.send_message(DESTINATION_1, event.message)
                await client.send_message(DESTINATION_2, event.message)

            else:
                print(f"[{nom_expediteur}] Limite de 100 films atteinte.")
        else:
            print(f"[{nom_expediteur}] Film trop petit ({taille_mo:.2f} Mo).")

    elif event.media:
        print(f"[{nom_expediteur}] Média ignoré.")


print("L'assistant indépendant est prêt et actif !")

client.start()
client.run_until_disconnected()
