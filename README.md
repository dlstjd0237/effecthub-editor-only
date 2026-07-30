# Particle2dx — Editor Only

*English · [한국어](README_KR.md)*

An offline build of the [EffectHub](http://www.effecthub.com) source with **nothing but the particle
editor** left. Design particles for cocos2d-x / Cocos2d-JS / CoronaSDK (`.plist`, `.json`) in the
browser and download them straight away.

No database, no PHP, no login, no server API. A static file server is all it takes.

![screenshot](thumbnail.png)

## Run it

```sh
python -m http.server 8000      # or: npx serve -l 8000
```

Then open <http://localhost:8000> in Chrome / Edge / Firefox.

> Opening `index.html` directly (`file://`) does not work: the templates in `particle/` and `plist/`
> are read over XHR, which the browser blocks on file URLs. Any static server will do.

## Using it

| Panel | What it does |
|---|---|
| **Color&Shape** | Texture picker, start/end colour, size, blend mode |
| **Motion** | Gravity/Radius mode, lifetime, emission rate, angle, speed, gravity |
| **Template** | 41 built-in presets (hover to preview) |
| **Export** | Save to a file (see below) |
| **Background** | Background colour, drag & drop background/foreground PNGs |

Drop a `.plist` / `.json` / `.alljson` file onto the canvas to load it.
Drop a PNG onto `DropPNG` to use it as the particle texture.

Shortcuts: `Alt+C/M/T/E` switch panels, `Alt+←→` rotate, `Alt+↑↓` scale, `Alt+A` add emitter,
`Alt+1~9` select/hide an emitter, `Alt+D` duplicate, `Alt+S` snapshot, `Alt+P` save plist.

### Export panel

| Button | You get |
|---|---|
| cocos icon (PNG Contained) | `.plist` — single file, texture embedded as gzip+base64 |
| cocos icon + `particle_texture.png` | `.plist` plus the PNG separately |
| corona icon + `particle_texture.png` | CoronaSDK `.json` plus the PNG |
| AllJson | every emitter in one file (`.alljson`, this editor only) |

The `filename` field becomes the name of the saved file.

## Layout

```
index.html      the whole editor UI
myApp.js        editor logic (cocos2d-html5 scene)
main.js         cocos2d bootstrap
cocos2d.js      engine config
assets.js       png/ and plist/ listings + gzip+base64 of each texture  <- generated
gen_assets.py   generates assets.js
png/            built-in textures
plist/          built-in presets
particle/       plist / corona json templates
res/            guide images
```

Added a file to `png/` or `plist/`? Regenerate the listings:

```sh
python gen_assets.py
```

## What changed from the original

PHP used to produce the file listings, the gzipped textures and the download headers, and saving
went to an EffectHub account (a database). All of it is now done by the browser, so no server is
needed.

- file listing (`ls`) → `assets.js`, generated at build time
- PNG gzip (`gzencode`) → built-in textures are prebaked into `assets.js`, dropped PNGs use `CompressionStream`
- downloads (`Content-Disposition`) → `Blob` + `<a download>`
- uploads → there are none; `URL.createObjectURL` keeps the file inside the page
- removed: community features, login, cloud save, the Flash editor, UEditor, the CodeIgniter app

## License

The editor is a fork of [particle2dx](https://github.com/mash76/particle2dx) (MIT); the engine is
cocos2d-html5 (MIT). See `LICENSE`.
