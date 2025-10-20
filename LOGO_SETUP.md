# GreenLink Logo Setup Instructions

## Steps to Add Your Logo

### 1. Save the Logo Image
Save your GreenLink logo (the green square with "gl" and leaf design) to:
```
e:\campuslink-working\static\images\greenlink-logo.png
```

### 2. Image Requirements
- **Format**: PNG with transparent background (recommended) or JPG
- **Recommended Size**: 200x200px to 400x400px
- **File Name**: `greenlink-logo.png` (exactly as shown)

### 3. What's Already Done ✅
- ✅ Navbar updated to use logo image instead of emoji
- ✅ CSS styling added (40px height, maintains aspect ratio)
- ✅ Favicon updated to use the logo
- ✅ Changes committed and pushed to GitHub

### 4. Where the Logo Appears
The logo will be displayed in:
1. **Navbar** - Top left corner next to "GreenLink" text
2. **Browser Tab** - As the favicon/icon in the browser tab
3. Scales properly on mobile and desktop

### 5. Alternative: Use Different File Name
If you want to use a different file name, update these files:

**templates/base.html** (Line ~47):
```html
<img src="{% static 'images/YOUR-LOGO-NAME.png' %}" alt="GreenLink" class="brand-logo">
```

**templates/base.html** (Line ~8-9):
```html
<link rel="icon" type="image/png" href="{% static 'images/YOUR-LOGO-NAME.png' %}">
```

### 6. Verify It Works
After adding the logo file:
1. Refresh your browser (Ctrl + F5 for hard refresh)
2. Check the navbar - logo should appear next to "GreenLink"
3. Check the browser tab - logo should appear as favicon
4. If not showing, clear browser cache or restart Django server

### 7. Current Logo Styling
```css
.brand-logo {
    height: 40px;          /* Fixed height */
    width: auto;           /* Maintains aspect ratio */
    object-fit: contain;   /* Scales properly */
}
```

To adjust the size, edit `static/css/aesthetic_theme.css` and change the `height` value.

## Troubleshooting

**Logo not showing?**
- Make sure file is named exactly: `greenlink-logo.png`
- Check file is in: `static/images/` folder
- Run: `python manage.py collectstatic` (if needed)
- Clear browser cache: Ctrl + Shift + Delete
- Hard refresh: Ctrl + F5

**Logo too big/small?**
- Edit `height: 40px` in `.brand-logo` CSS class
- Recommended range: 30px to 50px

**Want to use SVG instead?**
- Save as `greenlink-logo.svg`
- Change `type="image/png"` to `type="image/svg+xml"` in base.html
