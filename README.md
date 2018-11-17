# Shitty Number Bot

## What
A twitter bot using the account @EivindsShitBot. If a user sends a tweet in the format "@EivindsShitBot \<Integer\>", it'll reply with a fun fact from http://numbersapi.com/

## Usage
Build with `docker build -t numbertwitterbot .` and run with `docker run -itd --restart unless-stopped --name numbertwitterbot numbertwitterbot`