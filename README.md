# Vampire Dice for Discord

This is a Discord Bot for playing Vampire: The Masquerade 5e. It allows you to roll dice pools and calculates your successes.

## How to install

Open the link in your browser and follow the instructions:

- [Install Vampire Dice Discord Bot](https://discord.com/api/oauth2/authorize?client_id=784904882154504243&permissions=350272&scope=bot)

Create 7 Custom Emoji that will be used by the bot to represent the dice

- On your Discord Server, Open the "Server Settings"
- Open the "Emoji" section
- Use the "Upload Emoji" button
- The emoji need to be named as follows:
  - regularcritical, regularsuccess, regularfailure, hungercritical, hungersuccess, hungerfailure, hungerbeastial

You are free to use the custom emjoi images I've created in this project

- [Custom Vampire Dice Images](./emoji/emoji.zip)
- When you upload these images they should default to the correct names

<img src="./images/discord-settings-emoji.png?raw=true" width="800">

---

## Commands

### Pool Command

Syntax:

```
/pool <number of dice in pool> <number of hunger dice>
```

Roll a dice pool, suppling the total number of dice in the pool and how many of those dice are hunger dice.

Example:

```
# Roll a dice pool of 7 dice, 3 of which are hunger dice
/pool 7 3
```

### Rouse Command

Syntax:

```
/rouse
```

Roll a rouse check. This a convience command that always creates a dice pool of 1 regular die and no hunger die.

Example:

```
/rouse
```

### Will Command

Syntax:

```
/will
```

This command will find the last `pool` command you executed and re-roll up to 3 failed regular dice. The new result will then be displayed.

Example:

```
/will
```

---

### Visual Examples

<img src="./images/vampire-dice.png?raw=true" width="500" />
