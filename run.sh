#! /bin/bash

while true; do
    git -C /home/paloma/LeCroissantBot pull origin master
    python3 /home/paloma/LeCroissantBot/bot.py
    sleep 1
done
