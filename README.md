# vaulttranslate-ct2
Private, on-device document translation for enterprise. Translate DOCX, PPTX, XLSX, PDF, MD, and TXT with formatting preserved. No cloud, no data leakage—powered by CTranslate2 for fast CPU inference.

## CLI (skeleton)
Run a dry-run request preview with:

```bash
vaulttranslate translate \
  --input ./document.txt \
  --output ./document.fr.txt \
  --source en \
  --target fr \
  --dry-run
```

Run without `--dry-run` to execute the local pipeline (`txt`, `md`, `docx`) and write output:

```bash
vaulttranslate translate \
  --input ./document.txt \
  --output ./document.fr.txt \
  --source en \
  --target fr
```
