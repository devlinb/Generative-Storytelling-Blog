# Generative Storytelling Blog

A Hugo-powered blog exploring AI storytelling, LLMs, and software engineering.

## Prerequisites

- Docker and Docker Compose installed
- Traefik reverse proxy running with an external `traefik` network
- Hugo (for rebuilding the site after content changes)

## Building the Site

This is a Hugo static site. After making content changes, rebuild the site:

```bash
hugo
```

This generates the static HTML/CSS/JS in the `public/` directory.

## Docker Deployment

Deploy the blog behind Traefik:

```bash
docker-compose up -d
```

The docker-compose.yml file configures:
- nginx:alpine container to serve the static files from `public/`
- Custom nginx.conf to handle the `/blog/` path
- Traefik labels for routing to `www.generativestorytelling.ai/blog/`

## Configuration

### Hugo Configuration (hugo.toml)

The site is configured with:
- `baseURL = 'https://www.generativestorytelling.ai/blog/'`
- Theme: terminal (included as git submodule)

### Traefik Configuration

Routing is configured via Docker Compose labels:
- **Host**: `www.generativestorytelling.ai`
- **PathPrefix**: `/blog`
- **Entry point**: `websecure` (HTTPS)
- **Priority**: 0 (between Arcadia projects and homepage fallback)
- **TLS**: Enabled and managed by Traefik

## Adding New Blog Posts

1. Create a new post:
   ```bash
   hugo new posts/my-new-post.md
   ```

2. Edit the post in `content/posts/my-new-post.md`

3. Rebuild the site:
   ```bash
   hugo
   ```

4. Restart the container to serve the updated content:
   ```bash
   docker-compose restart
   ```

## Local Development

Run Hugo's built-in development server:

```bash
hugo server -D
```

This serves the site at `http://localhost:1313` with live reload enabled.

## Theme

This site uses the [Hugo Terminal theme](https://github.com/panr/hugo-theme-terminal) installed as a git submodule in `themes/terminal`.
