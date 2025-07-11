# Icon Troubleshooting

## If your icon isn't showing up in the toolbar:

### 1. Check you have the icon files:
Make sure these files exist in your extension folder:
- `icon.png` (48x48, main icon)
- `icon-16.png` (16x16, optional)
- `icon-32.png` (32x32, optional)

### 2. Generate the icons:
1. Open `/home/james/mh/extension/bootstrap_icon.html`
2. Click "📥 Download 48x48 (Main)" to get `icon.png`
3. Save it directly in the extension folder

### 3. Reload the extension:
**Firefox:**
- Go to `about:debugging#/runtime/this-firefox`
- Find your extension
- Click "Reload" button

**Chrome/Edge:**
- Go to `chrome://extensions/`
- Find your extension
- Click the reload icon (🔄)

### 4. Check browser console:
1. Go to the extensions page
2. Click "Inspect views: background page" (Chrome) or similar
3. Look for any error messages about missing icon files

### 5. Try a simple icon:
If still not working, try this simple fallback:

Create a simple `icon.png`:
1. Open any image editor
2. Create a 48x48 pixel image
3. Fill it with green color
4. Save as `icon.png` in the extension folder

### 6. Clear browser cache:
Sometimes browsers cache extension data:
- Restart your browser completely
- Or try in an incognito/private window

### 7. File names are case-sensitive:
Make sure the file names match exactly:
- `icon.png` (not `Icon.png` or `ICON.PNG`)
- `icon-16.png` (not `icon_16.png`)

## Still not working?
Try updating the manifest to use just one simple icon:

```json
"browser_action": {
  "default_title": "Add to Favorites",
  "default_icon": "icon.png"
}
```
