import os

media_dir = '_media'
files = os.listdir(media_dir)
media_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'))]
media_files.sort()

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>_ct-AVATAR Gallery</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; background: #121212; color: #fff; display: none; }
        #password-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: #1e1e1e; }
        #password-screen h2 { margin-bottom: 20px; font-weight: 300; }
        #gallery-screen { padding: 20px; max-width: 1200px; margin: 0 auto; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }
        .card { background: #2c2c2c; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        img, video { width: 100%; height: auto; display: block; border-bottom: 2px solid #444; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; flex-wrap: wrap; gap: 20px; }
        .header h1 { margin: 0; font-weight: 300; letter-spacing: 1px; }
        button { padding: 12px 20px; background: #0d6efd; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: background 0.2s; }
        button:hover { background: #0b5ed7; }
        .qr-code { text-align: center; margin-bottom: 30px; background: #1e1e1e; padding: 20px; border-radius: 12px; display: inline-block; }
        .qr-code img { max-width: 150px; margin: 0 auto; border-radius: 8px; }
        .qr-code p { margin-top: 0; color: #aaa; }
        input[type="password"] { padding: 12px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #444; background: #333; color: white; font-size: 16px; outline: none; text-align: center; }
        input[type="password"]:focus { border-color: #0d6efd; }
    </style>
</head>
<body>

<div id="password-screen">
    <h2>Secure Gallery Access</h2>
    <input type="password" id="pw-input" placeholder="Enter Password" onkeypress="if(event.key === 'Enter') checkPassword()">
    <button onclick="checkPassword()">Unlock</button>
</div>

<div id="gallery-screen" style="display:none;">
    <div class="header">
        <h1>_ct-AVATAR Gallery</h1>
        <div>
            <input type="file" id="file-import" multiple accept="image/*,video/*" style="display:none;" onchange="importLocalFiles(event)">
            <button onclick="document.getElementById('file-import').click()">Import Media (Preview)</button>
        </div>
    </div>
    <div style="text-align: center;">
        <div class="qr-code">
            <p>Scan to view on mobile:</p>
            <img src="_media/qrcode.png" alt="QR Code">
        </div>
    </div>
    <div class="grid" id="media-grid">
        {MEDIA_HTML}
    </div>
</div>

<script>
    document.body.style.display = 'block';
    
    function checkPassword() {
        if (document.getElementById('pw-input').value === 'Meatheads') {
            document.getElementById('password-screen').style.display = 'none';
            document.getElementById('gallery-screen').style.display = 'block';
        } else {
            alert('Incorrect password. Access denied.');
            document.getElementById('pw-input').value = '';
        }
    }
    
    function importLocalFiles(event) {
        const files = event.target.files;
        if (files.length === 0) return;
        
        const grid = document.getElementById('media-grid');
        for (let file of files) {
            const url = URL.createObjectURL(file);
            const card = document.createElement('div');
            card.className = 'card';
            if (file.type.startsWith('video/')) {
                card.innerHTML = `<video src="${url}" controls autoplay loop muted playsinline></video>`;
            } else {
                card.innerHTML = `<img src="${url}">`;
            }
            grid.insertBefore(card, grid.firstChild);
        }
        
        // Brief delay to allow rendering before alert
        setTimeout(() => {
            alert("Media added to preview! \\n\\nTo save these permanently to the live site:\\n1. Save files to the '_media' folder.\\n2. Run 'python update_gallery.py'.\\n3. Push to GitHub.");
        }, 100);
    }
</script>
</body>
</html>
"""

media_html = ""
for f in media_files:
    if f == 'qrcode.png': continue
    if f.lower().endswith('.mp4'):
        media_html += f'<div class="card"><video src="_media/{f}" controls loop muted playsinline></video></div>\n'
    else:
        media_html += f'<div class="card"><img src="_media/{f}" loading="lazy" alt="{f}"></div>\n'

html_content = html_template.replace('{MEDIA_HTML}', media_html)

with open('index.html', 'w') as f:
    f.write(html_content)

print(f"index.html updated successfully with {len(media_files)-1} media files.")
