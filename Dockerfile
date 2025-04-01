# Utilisation de l'image officielle httpd (Apache) basée sur Alpine 
FROM httpd:alpine 
# Installation de git pour cloner le dépôt GitHub 
RUN apk add git 
# Clonage du dépôt GitHub dans un répertoire temporaire 
RUN git clone https://github.com/ton-compte-github/nom-depot.git 
# Copier les fichiers du projet web vers la racine de du serveur web apache 
RUN cp -r /tmp/nom-depot/* /usr/local/apache2/htdocs/ 
# Ajout d'une configuration personnalisée pour Apache 
RUN echo "ServerName localhost" >> /usr/local/apache2/conf/httpd.conf