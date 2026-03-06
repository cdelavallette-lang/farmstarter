# Deploying to Netlify - Step by Step Guide

Your site is ready to deploy to **santapualafarm.netlify.app**!

## Step-by-Step Instructions

### Step 1: Sign Up for Netlify (Free)
1. Go to https://www.netlify.com/
2. Click "Sign up" (top right)
3. Choose "Sign up with GitHub" (easiest option)
4. Authorize Netlify to access your GitHub account

### Step 2: Create New Site
1. Once logged in, click **"Add new site"** → **"Import an existing project"**
2. Click **"Deploy with GitHub"**
3. Search for and select your repository: **`farmstarter`**
4. Configure build settings:
   - **Branch to deploy:** `master`
   - **Publish directory:** `docs`
   - **Build command:** (leave empty)
5. Click **"Deploy site"**

### Step 3: Change Site Name
1. After deployment, go to **Site settings**
2. Click **"Change site name"** (under Site details)
3. Enter: **`santapualafarm`**
4. Click **Save**

### Step 4: Done! 🎉
Your site will be live at:
**https://santapualafarm.netlify.app/**

## Benefits of Netlify

✅ **Auto-Deploy** - Every git push automatically updates your site  
✅ **Free HTTPS** - Secure by default  
✅ **Fast CDN** - Loads quickly worldwide  
✅ **No Server Maintenance** - Netlify handles everything  
✅ **$0 Forever** - Free tier includes everything you need  

## Alternative: Deploy via CLI (Advanced)

If you prefer command line:

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from project directory
cd /opt/FarmGrowth
netlify deploy --prod --dir=docs --site-name=santapualafarm
```

## Troubleshooting

**Q: "Site name already taken"**  
A: Try `santapuala-farm` or `santa-puala-farm` instead

**Q: "Build failed"**  
A: Make sure publish directory is set to `docs` not `public`

**Q: "404 errors on page refresh"**  
A: Already configured in netlify.toml file (redirects enabled)

## Share Your Site

Once deployed, share this link with family:
**https://santapualafarm.netlify.app/**

No login required! Anyone can view it.
