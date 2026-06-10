#!/usr/bin/env python3
"""更换 assets 背景图或修改 clinic-info.txt 后运行，同步内嵌数据。"""
import os, base64, json, struct

CLINIC_KEYS = {'诊所名称': 'name', '联系电话': 'phone', '诊所地址': 'address'}

def read_clinic_info(path='clinic-info.txt'):
    info = {}
    if not os.path.exists(path):
        return info
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            field = CLINIC_KEYS.get(key.strip())
            if field:
                info[field] = value.strip()
    return info

def write_clinic_info_js(info, path='clinic-info.js'):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('window.CLINIC_INFO=')
        json.dump(info, f, ensure_ascii=False)
        f.write(';\n')

def image_size(data, ext):
    if ext == '.png' and data[:8] == b'\x89PNG\r\n\x1a\n':
        w, h = struct.unpack('>II', data[16:24])
        return int(w), int(h)
    if ext in ('.jpg', '.jpeg'):
        i = 2
        while i < len(data) - 1:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack('>HH', data[i + 5:i + 9])
                return int(w), int(h)
            if marker in (0xD8, 0xD9):
                i += 2
                continue
            length = struct.unpack('>H', data[i + 2:i + 4])[0]
            i += 2 + length
    return 0, 0

embed = {}
for fn in sorted(os.listdir('assets')):
    if not fn.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        continue
    path = f'assets/{fn}'
    with open(path, 'rb') as f:
        raw = f.read()
    ext = os.path.splitext(fn)[1].lower()
    mime = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
    w, h = image_size(raw, ext)
    embed[path] = {
        'dataUrl': f'data:{mime};base64,{base64.b64encode(raw).decode()}',
        'w': w,
        'h': h,
    }

with open('assets-embed.js', 'w', encoding='utf-8') as f:
    f.write('window.EMBEDDED_ASSETS=')
    json.dump(embed, f, ensure_ascii=False)
    f.write(';\n')

clinic_info = read_clinic_info()
write_clinic_info_js(clinic_info)
print(f'已更新 assets-embed.js（{len(embed)} 张图）')
print(f'已更新 clinic-info.js（{clinic_info.get("name", "")}）')
