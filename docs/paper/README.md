# CSEB Paper Compilation

To compile `cseb_paper.md` to PDF using Pandoc:

```bash
pandoc cseb_paper.md -o cseb_paper.pdf --pdf-engine=xelatex --citeproc --bibliography=references.bib
```
