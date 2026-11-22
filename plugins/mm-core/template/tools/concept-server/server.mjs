import http from 'node:http';
import fs from 'node:fs/promises';
import { createReadStream } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..', '..');
const outDir = path.join(root, '.agent-output');
const conceptsDir = path.join(outDir, 'concepts');
const decisionsDir = path.join(outDir, 'decisions');
const publicDir = path.join(here, 'public');
const port = Number(process.env.PORT || 5090);
const host = '127.0.0.1';
const idPattern = /^[A-Za-z0-9_-]{1,80}$/;
const imagePattern = /\.(png|jpe?g|webp|gif)$/i;
const mime = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8' };

async function readJson(file, fallback = null) {
  try { return JSON.parse(await fs.readFile(file, 'utf8')); } catch { return fallback; }
}

async function listGallery() {
  let days = [];
  try { days = (await fs.readdir(conceptsDir, { withFileTypes: true })).filter(d => d.isDirectory()).map(d => d.name).sort().reverse(); } catch { return []; }
  const result = [];
  for (const day of days) {
    const files = (await fs.readdir(path.join(conceptsDir, day))).filter(f => imagePattern.test(f));
    const items = [];
    for (const f of files) {
      const stat = await fs.stat(path.join(conceptsDir, day, f));
      const base = f.replace(/\.[^.]+$/, '');
      const meta = await readJson(path.join(conceptsDir, day, base + '.json'), {});
      items.push({ name: base, url: `/files/concepts/${day}/${encodeURIComponent(f)}`, prompt: meta.prompt || '', model: meta.model || '', mtime: Math.round(stat.mtimeMs) });
    }
    items.sort((a, b) => b.mtime - a.mtime);
    if (items.length) result.push({ day, items });
  }
  return result;
}

async function listDecisions() {
  let files = [];
  try { files = await fs.readdir(decisionsDir); } catch { return []; }
  const out = [];
  for (const f of files.filter(f => f.endsWith('.json') && !f.endsWith('.choice.json'))) {
    const d = await readJson(path.join(decisionsDir, f));
    if (!d || !idPattern.test(String(d.id || ''))) continue;
    d.choice = await readJson(path.join(decisionsDir, d.id + '.choice.json'));
    d.options = (d.options || []).map(o => ({ ...o, imageUrl: o.image ? '/files/' + o.image.split('/').map(encodeURIComponent).join('/') : null }));
    out.push(d);
  }
  out.sort((a, b) => String(b.created || '').localeCompare(String(a.created || '')));
  return out;
}

function send(res, status, body, type = 'application/json; charset=utf-8') {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
  res.end(typeof body === 'string' || Buffer.isBuffer(body) ? body : JSON.stringify(body));
}

async function serveFile(res, base, rel) {
  const full = path.resolve(base, rel);
  if (!full.startsWith(base + path.sep)) return send(res, 403, { error: 'forbidden' });
  const ext = path.extname(full).toLowerCase();
  if (!mime[ext]) return send(res, 404, { error: 'not found' });
  try {
    const stat = await fs.stat(full);
    if (!stat.isFile()) return send(res, 404, { error: 'not found' });
    res.writeHead(200, { 'Content-Type': mime[ext], 'Content-Length': stat.size, 'Cache-Control': 'no-cache', 'X-Content-Type-Options': 'nosniff' });
    createReadStream(full).pipe(res);
  } catch { send(res, 404, { error: 'not found' }); }
}

function readBody(req, limit = 65536) {
  return new Promise((resolve, reject) => {
    let size = 0; const chunks = [];
    req.on('data', c => { size += c.length; if (size > limit) { reject(new Error('too large')); req.destroy(); } else chunks.push(c); });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

function hostAllowed(req) {
  const allowed = [`localhost:${port}`, `127.0.0.1:${port}`];
  if (!allowed.includes(req.headers.host || '')) return false;
  const origin = req.headers.origin;
  return !origin || allowed.some(a => origin === `http://${a}`);
}

const server = http.createServer(async (req, res) => {
  if (!hostAllowed(req)) return send(res, 403, { error: 'forbidden host' });
  const url = new URL(req.url, `http://${req.headers.host}`);
  const p = decodeURIComponent(url.pathname);
  try {
    if (req.method === 'GET' && p === '/api/ping') return send(res, 200, { ok: true });
    if (req.method === 'GET' && p === '/api/state') return send(res, 200, { gallery: await listGallery(), decisions: await listDecisions() });
    const m = p.match(/^\/api\/decisions\/([^/]+)\/choice$/);
    if (req.method === 'POST' && m) {
      const id = m[1];
      if (!idPattern.test(id)) return send(res, 400, { error: 'bad id' });
      const decision = await readJson(path.join(decisionsDir, id + '.json'));
      if (!decision) return send(res, 404, { error: 'decision not found' });
      const body = JSON.parse(await readBody(req));
      if (!(decision.options || []).some(o => o.id === body.optionId)) return send(res, 400, { error: 'bad option' });
      const choice = { decisionId: id, optionId: String(body.optionId), note: String(body.note || '').slice(0, 2000), chosenAt: new Date().toISOString() };
      await fs.writeFile(path.join(decisionsDir, id + '.choice.json'), JSON.stringify(choice, null, 2), 'utf8');
      return send(res, 200, choice);
    }
    if (req.method === 'GET' && p.startsWith('/files/')) {
      const rel = p.slice('/files/'.length);
      const top = rel.split('/')[0];
      if (!['concepts', 'decisions'].includes(top) || !imagePattern.test(rel)) return send(res, 404, { error: 'not found' });
      return serveFile(res, outDir, rel);
    }
    if (req.method === 'GET' && (p === '/' || p === '/index.html')) return serveFile(res, publicDir, 'index.html');
    return send(res, 404, { error: 'not found' });
  } catch (e) {
    return send(res, 500, { error: String(e.message || e) });
  }
});

server.listen(port, host, () => console.log(`concept server http://localhost:${port}/`));
