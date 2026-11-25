export default {
  async fetch(req) {
    const url = new URL(req.url);
    const path = url.pathname === "/" ? "/index.html" : url.pathname;
    const res = await fetch("https://dryaaron.github.io/shelfmark" + path + url.search, { cf: { cacheTtl: 600, cacheEverything: true } });
    return new Response(res.body, res);
  },
};
