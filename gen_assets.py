#!/usr/bin/env python
"""png/ と plist/ の一覧を assets.js に書き出す。

もとの index.php が PHP (ls + gzencode) でやっていた事をビルド時に済ませておく。
png/ や plist/ にファイルを足したら、このスクリプトを実行しなおすこと:

    python gen_assets.py
"""
import base64, glob, gzip, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

png_gz_b64 = {}
for path in sorted(glob.glob("png/*.png")):
    raw = open(path, "rb").read()
    packed = gzip.compress(raw, 6, mtime=0)          # plist の textureImageData と同じ形式
    assert gzip.decompress(packed) == raw            # 往復チェック
    png_gz_b64[os.path.basename(path)[:-4]] = base64.b64encode(packed).decode()

plists = sorted(os.path.basename(p) for p in glob.glob("plist/*.plist") + glob.glob("plist/*.p2dx_json"))
assert png_gz_b64 and plists, "png/ か plist/ が空"

with io.open("assets.js", "w", encoding="utf-8", newline="\n") as f:
    f.write("// gen_assets.py が生成 - 手で編集しない\n")
    f.write("var PLISTS = %s;\n" % json.dumps(plists, indent=0).replace("\n", ""))
    f.write("var PNG_GZ_B64 = %s;\n" % json.dumps(png_gz_b64, indent=1))

print("assets.js: %d textures, %d templates" % (len(png_gz_b64), len(plists)))
