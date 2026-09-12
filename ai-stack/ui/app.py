# -*- coding: utf-8 -*-
"""デモ用Web UI — 依存ゼロ(標準ライブラリのみ)、localhost専用

  .venv/Scripts/python ui/app.py  →  http://127.0.0.1:7877

二段式:
  POST /prepare : 脱敏 + 類似先例検索(ローカル層のみ、即時)
  POST /draft   : LLM起草 + 構造検査(クラウド層、~1分)
デモの見せ方: ①生の要件書 ②「クラウドに渡るのはこれだけ」③先例 ④ドラフト ⑤監査
"""
import json
import logging
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from masking.masker import Masker            # noqa: E402
from rag.retriever import BM25Index          # noqa: E402
from llm.providers import get_provider       # noqa: E402
from evalkit.structure_check import check    # noqa: E402
from pipeline.drafting import build_prompt, build_references   # noqa: E402

PORT = 7877
MAX_BODY_BYTES = 2 * 1024 * 1024   # 入力上限。無制限だとローカルでもメモリ枯渇させられる

log = logging.getLogger("ui")
_masker = Masker(str(ROOT / "masking" / "entities.json"))
_index = BM25Index()
_index.add_dir(str(ROOT / "demo_data" / "past_projects"), "**/design_*.md")
_demo_rfp = (ROOT / "demo_data" / "incoming" / "new_rfp.md").read_text(encoding="utf-8")

HTML = """<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<title>AI設計書ドラフト作成 — デモ</title>
<style>
 :root { --navy:#1a2b4a; --acc:#2f6fed; --ok:#1a7f4e; --warn:#b3261e; --bg:#f6f7fa; }
 * { box-sizing:border-box; }
 body { font-family:"Yu Gothic UI","Hiragino Sans",Meiryo,sans-serif; margin:0; background:var(--bg); color:#222; }
 header { background:var(--navy); color:#fff; padding:14px 28px; display:flex; align-items:baseline; gap:14px; }
 header h1 { font-size:18px; margin:0; font-weight:600; }
 header span { font-size:12px; opacity:.75; }
 main { max-width:1180px; margin:22px auto; padding:0 20px; }
 .card { background:#fff; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,.08); padding:18px 22px; margin-bottom:18px; }
 .card h2 { font-size:14px; margin:0 0 10px; color:var(--navy); display:flex; align-items:center; gap:8px; }
 .step { display:inline-flex; align-items:center; justify-content:center; width:22px; height:22px; border-radius:50%; background:var(--acc); color:#fff; font-size:12px; }
 textarea { width:100%; height:200px; font:13px/1.6 Consolas,monospace; border:1px solid #ccd3e0; border-radius:6px; padding:10px; }
 .row { display:flex; gap:16px; flex-wrap:wrap; }
 .row > div { flex:1 1 440px; min-width:0; }
 .pane { border:1px solid #e3e7ef; border-radius:6px; padding:12px; height:280px; overflow:auto; font:12.5px/1.7 Consolas,monospace; white-space:pre-wrap; background:#fbfcfe; }
 .pane.ok-border { border-color:var(--ok); background:#f4faf6; }
 mark { background:#ffe9a8; border-radius:3px; padding:0 3px; }
 button { background:var(--acc); color:#fff; border:0; border-radius:6px; padding:10px 22px; font-size:14px; cursor:pointer; }
 button:disabled { background:#9db3d8; cursor:wait; }
 button.ghost { background:#fff; color:var(--acc); border:1px solid var(--acc); }
 select { padding:8px; border-radius:6px; border:1px solid #ccd3e0; }
 .refs .ref { border-left:3px solid var(--acc); padding:6px 12px; margin:8px 0; background:#f4f7fd; border-radius:0 6px 6px 0; }
 .refs .ref b { font-size:13px; }
 .badge { display:inline-block; font-size:11px; padding:2px 10px; border-radius:10px; margin-left:8px; }
 .badge.pass { background:#e2f3e9; color:var(--ok); }
 .badge.fail { background:#fbe5e3; color:var(--warn); }
 #draft { font:14px/1.8 "Yu Gothic UI",sans-serif; }
 #draft h1 { font-size:19px; border-bottom:2px solid var(--navy); padding-bottom:6px; }
 #draft h2 { font-size:15px; color:var(--navy); border-left:4px solid var(--acc); padding-left:8px; margin-top:22px; }
 #draft table { border-collapse:collapse; width:100%; font-size:12.5px; }
 #draft th,#draft td { border:1px solid #d5dae4; padding:5px 9px; text-align:left; }
 #draft th { background:#eef2f9; }
 #draft mark { background:#fff3bf; }
 .kv { font-size:12.5px; } .kv td { padding:3px 10px 3px 0; vertical-align:top; }
 .spin { display:inline-block; width:14px; height:14px; border:2px solid #fff; border-top-color:transparent; border-radius:50%; animation:r 0.8s linear infinite; vertical-align:-2px; margin-right:8px; }
 @keyframes r { to { transform:rotate(360deg);} }
 .hidden { display:none; }
 .note { font-size:11.5px; color:#667; }
</style></head><body>
<header><h1>設計書ドラフト自動作成</h1><span>機密は社外に出ません — onewonder AI導入デモ</span></header>
<main>
 <div class="card">
  <h2><span class="step">1</span>お客様の要件書（機密情報を含む"生"の文書）</h2>
  <textarea id="rfp"></textarea>
  <div style="margin-top:10px; display:flex; gap:12px; align-items:center;">
   <button class="ghost" onclick="loadDemo()">デモ要件書を読み込む</button>
   <select id="provider"><option value="claude-cli">Claude(本物)</option><option value="stub">スタブ(オフライン)</option></select>
   <button id="goBtn" onclick="prepare()">▶ 実行</button>
   <span class="note">実行しても、この画面の下で「何が社外に渡るか」を確認できます</span>
  </div>
 </div>

 <div class="card hidden" id="cardMask">
  <h2><span class="step">2</span>社内AIによる機密マスキング — <u>クラウドに渡るのは右側だけ</u></h2>
  <div class="row">
   <div><div class="note">原文（社内に留まる）</div><div class="pane" id="orig"></div></div>
   <div><div class="note">送信される内容（伏せ字済み）</div><div class="pane ok-border" id="masked"></div></div>
  </div>
  <table class="kv" id="mapTable"></table>
 </div>

 <div class="card hidden" id="cardRefs">
  <h2><span class="step">3</span>社内の過去案件から類似先例を検索（社内AIが参照資料を準備）</h2>
  <div class="refs" id="refs"></div>
  <div style="margin-top:12px"><button id="draftBtn" onclick="draft()">▶ この内容でクラウドAIに起草させる</button>
  <span class="note" id="draftNote"></span></div>
 </div>

 <div class="card hidden" id="cardDraft">
  <h2><span class="step">4</span>設計書ドラフト<span id="qcBadge"></span><span class="note" id="elapsed" style="margin-left:10px"></span></h2>
  <div id="draft"></div>
 </div>

 <div class="card hidden" id="cardAudit">
  <h2><span class="step">5</span>監査証跡（誰が・何を・どこへ・どう検査したか）</h2>
  <div class="pane" id="audit" style="height:170px"></div>
 </div>
</main>
<script>
let PREP = null;
const $ = id => document.getElementById(id);
function esc(s){ return s.replace(/&/g,"&amp;").replace(/</g,"&lt;"); }
function hi(s){ // 伏せ字ラベルをハイライト
  return esc(s).replace(/(\\[(?:EMAIL|PHONE|MONEY|POSTAL|URL)\\]|[A-N]社|担当者[甲乙丙丁戊己庚辛])/g, "<mark>$1</mark>");
}
function loadDemo(){ fetch("/demo").then(r=>r.text()).then(t=>{ $("rfp").value = t; }); }
async function prepare(){
  const text = $("rfp").value.trim(); if(!text) return alert("要件書を入力してください");
  $("goBtn").disabled = true;
  const r = await fetch("/prepare", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({text})});
  PREP = await r.json();
  $("orig").textContent = text;
  $("masked").innerHTML = hi(PREP.masked);
  let rows = "<tr><td class='note'>置換対応表（社内にのみ保存）:</td></tr>";
  for(const [k,v] of Object.entries(PREP.mapping)) rows += `<tr><td>${esc(k)}</td><td>→ <mark>${esc(v)}</mark></td></tr>`;
  $("mapTable").innerHTML = rows;
  $("refs").innerHTML = PREP.refs.map(x=>`<div class="ref"><b>${esc(x.title)}</b> <span class="note">(類似度 ${x.score})</span><br><span class="note">${esc(x.snippet)}…</span></div>`).join("") || "<i>先例なし</i>";
  ["cardMask","cardRefs"].forEach(id=>$(id).classList.remove("hidden"));
  ["cardDraft","cardAudit"].forEach(id=>$(id).classList.add("hidden"));
  $("goBtn").disabled = false;
  $("cardMask").scrollIntoView({behavior:"smooth"});
}
async function draft(){
  const btn = $("draftBtn"); btn.disabled = true;
  const prov = $("provider").value;
  btn.innerHTML = '<span class="spin"></span>起草中…' + (prov==="stub" ? "" : "（約1分）");
  const r = await fetch("/draft", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({masked: PREP.masked, mapping: PREP.mapping, provider: prov})});
  const d = await r.json();
  btn.disabled = false; btn.textContent = "▶ この内容でクラウドAIに起草させる";
  if(d.error){ return alert(d.error); }
  $("draft").innerHTML = md(d.draft);
  $("qcBadge").innerHTML = d.qc.ok ? '<span class="badge pass">構造検査 PASS</span>'
    : '<span class="badge fail">要修正 ' + d.qc.findings.length + '件</span>';
  $("elapsed").textContent = `${d.elapsed}秒 / provider=${d.provider}`;
  $("audit").textContent = JSON.stringify(d.audit, null, 2);
  ["cardDraft","cardAudit"].forEach(id=>$(id).classList.remove("hidden"));
  $("cardDraft").scrollIntoView({behavior:"smooth"});
}
function md(src){ // 最小Markdownレンダラ(見出し/表/リスト/強調/罫線)
  const lines = src.split("\\n"); let out = [], tbl = null;
  const flush = () => { if(tbl){ out.push("<table>"+tbl.map((r,i)=>"<tr>"+r.map(c=>i===0?`<th>${c}</th>`:`<td>${c}</td>`).join("")+"</tr>").join("")+"</table>"); tbl=null; } };
  for(const raw of lines){
    const l = raw.trimEnd();
    if(/^\\|/.test(l)){ const cells = l.replace(/^\\||\\|$/g,"").split("|").map(c=>inline(c.trim()));
      if(/^[-:\\s|]+$/.test(l.replace(/\\|/g,""))) continue; (tbl = tbl||[]).push(cells); continue; }
    flush();
    if(/^#{1,3}\\s/.test(l)){ const n = l.match(/^#+/)[0].length; out.push(`<h${n}>${inline(l.replace(/^#+\\s*/,""))}</h${n}>`); }
    else if(/^---+$/.test(l)) out.push("<hr>");
    else if(/^[-*]\\s/.test(l)) out.push(`<li>${inline(l.slice(2))}</li>`);
    else if(l) out.push(`<p>${inline(l)}</p>`);
  }
  flush(); return out.join("");
  function inline(s){ return esc(s).replace(/\\*\\*(.+?)\\*\\*/g,"<b>$1</b>")
    .replace(/(【要確認[^】]*】)/g,"<mark>$1</mark>"); }
}
loadDemo();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/demo":
            body = _demo_rfp.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict | None:
        """リクエストボディを検証して読む。不正なら 400 を返して None。"""
        raw_len = self.headers.get("Content-Length", "0")
        try:
            n = int(raw_len)
        except ValueError:
            self._json({"error": "Content-Length が不正です"}, 400)
            return None
        if n < 0 or n > MAX_BODY_BYTES:
            self._json({"error": f"リクエストが大きすぎます (上限 {MAX_BODY_BYTES} bytes)"}, 413)
            return None
        try:
            req = json.loads(self.rfile.read(n).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json({"error": "JSON として解析できません"}, 400)
            return None
        if not isinstance(req, dict):
            self._json({"error": "JSON オブジェクトを渡してください"}, 400)
            return None
        return req

    def _require_text(self, req: dict, key: str) -> str | None:
        val = req.get(key)
        if not isinstance(val, str) or not val.strip():
            self._json({"error": f"'{key}' に文字列が必要です"}, 400)
            return None
        return val

    def do_POST(self):
        req = self._read_json()
        if req is None:
            return
        if self.path == "/prepare":
            text = self._require_text(req, "text")
            if text is None:
                return
            masked, mapping = _masker.mask(text)
            hits = _index.search(masked, k=2)
            # スニペットも脱敏する。画面に出るだけでも実名は見せない
            snippets = []
            for h in hits:
                masked_ref, _ = _masker.mask(h["text"][:400], dict(mapping))
                snippets.append({"title": h["title"], "score": h["score"],
                                 "snippet": masked_ref[:110].replace("\n", " ")})
            self._json({"masked": masked, "mapping": mapping, "refs": snippets})
            return
        if self.path == "/draft":
            masked_req = self._require_text(req, "masked")
            if masked_req is None:
                return
            mapping = req.get("mapping")
            if not isinstance(mapping, dict):
                mapping = {}
            t0 = time.time()
            hits = _index.search(masked_req, k=2)
            # 先例文書も脱敏してからプロンプトへ。生テキストを渡すと実名が出境する
            refs_text, mapping = build_references(hits, _masker, dict(mapping))
            try:
                provider = get_provider(req.get("provider", "stub"))
                draft = provider.complete(build_prompt(masked_req, refs_text))
            except Exception:
                # 例外詳細はサーバ側ログのみ。パスや環境情報をクライアントに返さない
                log.exception("LLM 呼び出しに失敗")
                self._json({"error": "LLM呼び出しに失敗しました。サーバログを確認してください。"}, 502)
                return
            qc = check(draft, known_real_names=list(mapping))
            elapsed = round(time.time() - t0, 1)
            self._json({
                "draft": draft, "qc": qc, "elapsed": elapsed, "provider": provider.name,
                "audit": {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "provider": provider.name,
                    "masked_entities": mapping,   # 先例文書側の実体も監査対象に含める
                    "references_used": [h["title"] for h in hits],
                    "qc": qc,
                    "elapsed_sec": elapsed,
                },
            })
            return
        self._json({"error": "not found"}, 404)

    def log_message(self, *a):  # 静かに
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    print(f"demo UI: http://127.0.0.1:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
