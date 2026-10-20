# Hashnode migration

Imported all 15 published articles listed in the Meandering Thoughts sitemap,
with 10 local images. The five existing Markdown posts were retained.

Each imported article is a leaf bundle at `content/posts/<original-slug>/index.md`.
Front matter preserves the title, original slug, publication timestamp, last
modification timestamp, author, tags, description, and original source URL.
Cover and inline images are stored alongside the post. Links between migrated
articles now target `/blog/posts/<slug>/`. Existing articles retain their routes.

The source was each public article's `.md` endpoint, with metadata from the
public HTML. No API credentials or subscription were used. Hashnode alignment
hints were removed, duplicate title headings removed, and legacy HTML footnotes
converted to Markdown footnotes. Drafts and private content are outside this export.

`hashnode-migration.json` records source URLs and original-to-local image mappings.
`scripts/import_hashnode.py` contains the importer. Run it from the repository
root with Python 3; it requires network access, caches raw responses in
`/tmp/meandering-hashnode-export`, and refuses to overwrite existing post bundles.
It is an import tool, not a synchronization job.

Validation completed:

- Hugo build succeeded with no duplicate-path or omitted-HTML warnings.
- All 15 article output pages and their canonical URLs were checked.
- Every rendered article image resolved locally; all 10 downloaded images decoded.
- All four rewritten article links and every article fragment link resolved.
- Existing Hugo configuration/template deprecation warnings remain.

The migration does not publish the site or set redirects on Hashnode. The
existing deployment process should build Hugo from source; the tracked `public/`
output was not regenerated. Old Hashnode URLs still require source-side redirects
or updated canonical URLs if supported by the account.
