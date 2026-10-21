# Web app

`index.html` is the whole front end (HTML, CSS and JavaScript in one file). It is hosted on
S3 + CloudFront and loaded full screen by the Android shell in `../android`.

## Files the page expects next to `index.html`

The avatar clips are `.webm` videos. Put them in the same folder as `index.html`
(copy them from your S3 bucket; GitHub rejects single files over 100 MB, use Git LFS if one is larger):

```
remote_intro.webm  idle1.webm      listen1.webm   listen2.webm   features.webm
search.webm        apps.webm       rearrange.webm wifi.webm      display.webm
restart.webm       buffering.webm  profiles.webm  subtitles.webm remote.webm
voicesearch.webm   parental_a.webm parental_b.webm
```

`features.webm` is the looping "talking" motion shown while Amazon Polly speaks an answer.

## Backend address

Copy `config.example.json` to `config.json` and put your Lambda Function URL in it
(see `../backend/DEPLOY.md`). Without a `config.json` the page still works: the
tutorial chips play their recorded clips and typed questions use the local keyword matcher.

## Run locally

```
cd web
python -m http.server 8000
```

Open http://localhost:8000/ . Add `?debug` to the address to see backend error details under each answer.

## Remote control keys (browser)

| Fire TV remote | Keyboard |
|---|---|
| Up / Down / Left / Right | Arrow keys |
| Select | Enter or Space |
| Back | Esc or Backspace |
| Menu (three lines) | F1 or the Menu key |
