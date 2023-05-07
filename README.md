### About

#### Yo, have you heard about SteamGAU?
Short for SteamCMD Games Auto-Updater

It's a sweet little tool that helps you update your SteamCMD games on your Windows OS without any hassle. I made it when I was bored, and there weren't any good tools around that did the job (afaik). It's just a simple Python script packaged as a Windows application, and it updates your SteamCMD servers for you every morning at 4:00 am.

So you can chill and relax, knowing your games are always up to date.

### Make it happen!

#### Make it go brrrrr

1. First, you'll need to download the latest release of SteamGAU and save it anywhere on your PC. Then, run the SteamGAU.exe file.
2. Once you've done that, two new .json files will be created in the same directory where you saved SteamGAU.exe.
3. Open up the steamcmd.json file and insert your login information, along with the directory where your game is installed on your PC, and the game code for the game you want to update:
<pre>
{
    "logon": "anonymous",
    "install_dir": "put_your_install_dir_here", <-- Put your CSGO install_dir like D:\Games\CSGO
    "app_id": "740" <-- This is the Steam Game Code, 740 = CSGO
}
</pre>
4. Next, open up the servers.json file and enter your server data, such as the server name and directory, launch parameters, your Steam account code (which you can get from https://steamcommunity.com/dev/managegameservers), and the port number:
<pre>
{
    "name": "Server Name Goes Here",
    "server_dir": "D:\\example\\folder",
    "launch_parameters": "-game csgo -console -usercon -maxplayers_override 16 -tickrate 128 +game_type 0 +game_mode 1 +mapgroup mg_active +map de_mirage +ip 192.168.0.214 +net_pub",
    "set_steam_account": "<CODE-GOES-HERE>", <-- visit https://steamcommunity.com/dev/managegameservers to get it
    "port": "27015"
} <-- put a comma sign here in case you have multiple servers!!!
</pre>
5. Make sure to double-check that all your information is correct! Then, just re-run the SteamGAU.exe file and you're good to go.

### Will this run on reboot?

This sweet little app will automatically create a shortcut inside your Startup folder when you run it. This means that you can sleep soundly knowing that your games will always be up-to-date when you wake up. Just set it and forget it!This app upon running creates a shortcut inside your Startup folder, so you can sleep as deep as I'm right now!