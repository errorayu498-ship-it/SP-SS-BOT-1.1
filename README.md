# 📖 SS Role Bot — Complete Setup Guide
# Bot Programmed By: SUBHAN | SARAIKI PLAY
# ═══════════════════════════════════════════════════════════════════

## 🤖 Bot Features
- Members send screenshot in SS channel → Bot gives them a special role
- If someone chats (no screenshot) → Message deleted + warning sent
- /notify command → Beautiful embed with YouTube subscribe button
- Role duplicate check → Already has role? Bot tells them
- Full error handling + logging

---

## ─── STEP 1: Discord Developer Portal Setup ─────────────────────

1. Go to: https://discord.com/developers/applications
2. Click "New Application" → Name it (e.g. SARAIKI PLAY Bot)
3. Go to "Bot" tab → Click "Add Bot"
4. Under "Privileged Gateway Intents" → Enable ALL 3:
   ✅ Presence Intent
   ✅ Server Members Intent
   ✅ Message Content Intent
5. Copy your BOT TOKEN (click "Reset Token") → Save it

---

## ─── STEP 2: Invite Bot to Server ──────────────────────────────

1. Go to "OAuth2" → "URL Generator"
2. Select Scopes: ✅ bot  ✅ applications.commands
3. Select Bot Permissions:
   ✅ Manage Roles
   ✅ Read Messages/View Channels
   ✅ Send Messages
   ✅ Manage Messages
   ✅ Embed Links
   ✅ Attach Files
   ✅ Read Message History
4. Copy the generated URL → Paste in browser → Invite to your server

⚠️  IMPORTANT: Bot role must be ABOVE the role you want to give!
   Go to Server Settings → Roles → Drag bot role above SS role

---

## ─── STEP 3: Get IDs ────────────────────────────────────────────

Enable Developer Mode:
  Discord Settings → Advanced → Developer Mode ✅

Get IDs (Right-click → Copy ID):
  - Server ID (Guild ID):   Right-click server icon → Copy Server ID
  - Channel ID:             Right-click SS channel → Copy Channel ID
  - Role ID:                Server Settings → Roles → Right-click role → Copy Role ID

---

## ─── STEP 4: Configure .env File ───────────────────────────────

Copy .env.example to .env and fill in your values:

  DISCORD_TOKEN=your_actual_bot_token
  GUILD_ID=your_server_id
  SS_CHANNEL_ID=your_ss_channel_id
  ROLE_ID=your_special_role_id
  YOUTUBE_LINK=https://youtube.com/@YourChannel

---

## ─── STEP 5: Local Testing (Optional) ──────────────────────────

Install Python 3.11+ then:

  pip install -r requirements.txt
  python bot.py

Check console for: "Bot is online: YourBot#1234"

---

## ─── STEP 6: Deploy on Railway ──────────────────────────────────

1. Go to: https://railway.app → Sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
   OR: "New Project" → "Empty Service" → Connect GitHub
3. Upload your bot files (push to GitHub first):

   git init
   git add .
   git commit -m "SS Role Bot"
   git branch -M main
   git remote add origin https://github.com/YourUsername/ss-role-bot.git
   git push -u origin main

4. In Railway dashboard → Your Service → "Variables" tab:
   Add these environment variables ONE BY ONE:
   
   DISCORD_TOKEN   = your_bot_token
   GUILD_ID        = your_guild_id
   SS_CHANNEL_ID   = your_channel_id
   ROLE_ID         = your_role_id
   YOUTUBE_LINK    = https://youtube.com/@YourChannel

5. Railway will auto-detect Python and deploy!
6. Go to "Deployments" tab → Watch logs → Should see "Bot is online"

⚠️  DO NOT add .env file to GitHub! It's in .gitignore for safety.

---

## ─── STEP 7: Sync Slash Commands ────────────────────────────────

After first deployment, the /notify command syncs automatically.
If it doesn't appear, wait 1-2 minutes then restart the Railway service.

---

## ─── How Bot Works ──────────────────────────────────────────────

📸 SS Channel Flow:
  Member sends screenshot → Bot verifies → Gives role + beautiful message
  Member sends text only  → Bot deletes it + sends warning (8 sec auto-delete)
  Member already has role → Bot tells them they're already verified

/notify Command:
  Admin uses /notify → Bot sends embed with Subscribe button
  Requires "Manage Messages" permission to use

---

## ─── File Structure ─────────────────────────────────────────────

ss_role_bot/
├── bot.py           ← Main bot file
├── requirements.txt ← Python dependencies
├── Procfile         ← Railway deployment config
├── runtime.txt      ← Python version for Railway
├── .env.example     ← Example environment variables (SAFE to share)
├── .env             ← Your actual secrets (NEVER share/upload this!)
└── .gitignore       ← Prevents .env from going to GitHub

---

## ─── Troubleshooting ────────────────────────────────────────────

❌ "Role not found" error
   → Check ROLE_ID is correct
   → Make sure bot is in the same server

❌ "Missing permissions" error  
   → Bot role must be above the SS role in server settings
   → Re-invite bot with correct permissions

❌ /notify command not showing
   → Wait 1-2 minutes after bot starts
   → Check GUILD_ID is correct in .env
   → Restart Railway deployment

❌ Bot not responding to screenshots
   → Check SS_CHANNEL_ID is correct
   → Enable Message Content Intent in Developer Portal

---

## Programmed By: SUBHAN | SARAIKI PLAY 🎬
