# LightMesh-server

Serveur Flask pour la configuration et le controle des lampes. Utilisé entre autres par l'appli android.
Le principe est d'utiliser un module ESP via USB pour faire le pont avec le réseau maillé de tous les autres ESP.
On communique avec l'ESP en serial, qui envoie bêtement le json donné en broadcast sur le réseau maillé. Aucune verification du contenu n'est faite ici.

Un seul point d'entrée `@app.route('/lightsend', methods=["POST"])`
- va balancer le contenu de `send` dans le port série et tentera de réinitialiser le port usb en cas de soucis. On attend un objet JSON et retourne un JSON avec un 'message'

# Installation

doit être placé dans le répertoire home d'un linux, raspberry, ...
- `/home/*USER*/lights/xyz.sh`

Nécessite python 3, ainsi que flask (module python à importer via pip)

Ajouter les droits d'executions via un `chmod +x` 

Cas spécifique pour `resetUsb32.sh` qui devra être lancé en sudo par l'appli. Pour éviter le mot de passe root, on peut passer par un `sudo visudo` et rajouter la ligne 
- `*USER* ALL=(ALL) NOPASSWD: /home/*USER*/lights/resetUsbEsp32.sh` (remplacer les *USER*)
- Il faudra bien faire attention aux droits sur ce fichier, pour des raisons évidentes. Pour ma part, je l'ai `chown root:root` avec droit d'exec uniquement.


Le démarrage se fait avec `startserverlight.sh`, peut être configuré au démarrage avec `crontab -e`. C'est optionnel mais j'utilise screen pour avoir quand même accès à la console:
- `@reboot /usr/bin/screen -dmS lights sh /home/*USER*/lights/startserverlight.sh`

# Configuration

Quelques choses à changer potentiellement :
Vérifier le vendor ID et product ID de l'ESP utilisé avec `lsusb`. Par défaut c'est `1a86:55d4` avec un doux nom de `QinHeng Electronics USB Single Serial`. Si ça ne correspond pas, changer les ID dans `resetUsbEsp32.sh`.

Lancer le script `findUsb.sh`, si le nom est différent de `/dev/ttyACM0`, il faudra le changer dans le script `rest_light.py`

Par défaut, le serveur se met sur le port 5005, modifiable à la fin de `rest_light.py`

# Extra

`lightSend.py` permet de balancer des commandes sans passer par le serveur. Il prend en paramètre du JSON formatté

exemple de JSON valides à envoyer :
- `{}` -> aucun changement, on s'en sert de ping pour avoir l'état actuel dans la réponse
- `{"onoff": true}` -> explicite
- `{"color": {"0":7078093, "1":56540}}` -> change la couleur principale et secondaire
- `{"zone": 5, "color": ...}` -> applique les changements pour les zones 1 et 3 (c'est un bitfield - 00000101)
- `{"effect": 3}` -> change l'effet
