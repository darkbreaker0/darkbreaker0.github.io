# darkbreaker0.github.io

Personal academic website of **Dr. Tien-Chen Lin** — cytoskeletal neurobiology and the mechanobiology of brain development.

Live site: https://darkbreaker0.github.io

## Built with
- [Jekyll](https://jekyllrb.com/) + Jekyll Scholar, on a customized fork of the
  [academic-website-template](https://github.com/sbryngelson/academic-website-template).
- Deployed automatically by GitHub Actions on every push to the `source` branch.

## Local development
```bash
bundle install
bundle exec jekyll serve   # then open http://localhost:4000
```

## Editing content
- Identity, links, accent colour, navigation: `_config.yml`
- Profile (education, honours, mentees): `_data/pi.yml`, `_data/awards.yml`, `_data/people.yml`
- News: `_data/news.yml`
- Publications: `assets/ref.bib`
- Pages: `_pages/*.md`
