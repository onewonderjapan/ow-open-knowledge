# -*- coding: utf-8 -*-
"""日本語ビジネス文書のPII/機密マスキング（薄切片版）

方針:
  レイヤ0: 正規化（NFKC）— 全角/半角の表記揺れを潰す
  レイヤ1: 辞書 + custom（既知の顧客企業名・人名 → config/entities.json）
  レイヤ2: パターン（「株式会社X」「X株式会社」「X様/氏」）
  レイヤ3: 正規表現（電話/メール/郵便番号/金額/URL）
一貫性: 同一実体は文書全体で同一の伏せ字（田中商事→A社）にマッピングし、
        逆引き表(mapping)を返す。復元・監査に使う。

制限(薄切片): 辞書外の人名は「様/氏/さん」が付く場合のみ検出。
             本格版は GiNZA(NER) を重ねる予定 → docs/PITFALLS.md 参照。

設計上の前提: 過剰マスクは許容し、漏れは許容しない。判断が曖昧な場合は伏せる側に倒す。
トレードオフ: NFKC により全角括弧・全角英数は半角化される（`（新規）`→`(新規)`）。
             全角のまま素通りする漏れを防ぐことを優先した結果。→ PITFALLS.md 12
"""
import json
import re
import unicodedata
from pathlib import Path

# ダッシュ類: NFKC では統一されないものがある（− U+2212 / ‐ U+2010 / ‑ U+2011 /
# – U+2013 / — U+2014 / ― U+2015 / ー U+30FC）。
# 全文置換はしない: U+30FC は「フロー」等の長音符でもあり、置換すると日本語が壊れる。
# 数字に挟まれた区切り位置に限って許容する。
_DASH = "-\u2212\u2010\u2011\u2013\u2014\u2015\u30fc"

# 電話: 区切りあり(ダッシュ類/空白) / 括弧 / 区切りなし連番 の3形態。前後が数字なら誤検出なので除外
_PHONE_RE = re.compile(
    rf"(?<!\d)(?:"
    rf"0\d{{1,4}}[{_DASH}\s]\d{{1,4}}[{_DASH}\s]\d{{3,4}}"   # 03-1234-5678 / 03 1234 5678
    rf"|0\d{{1,4}}\(\d{{1,4}}\)\d{{3,4}}"                    # 03(1234)5678
    rf"|0\d{{9,10}}"                                         # 0312345678
    rf")(?!\d)"
)
# メール: ドットなしドメイン(社内ホスト名)も標識情報なので拾う
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*")

_RULES = [
    ("URL",    re.compile(r"https?://[^\s　]+")),   # URL内のメール/電話を巻き込まないよう先に処理
    ("EMAIL",  _EMAIL_RE),
    ("POSTAL", re.compile(rf"〒\s?\d{{3}}[{_DASH}]?\d{{4}}")),
    ("PHONE",  _PHONE_RE),
    ("MONEY",  re.compile(r"(?:[0-9,]+|[一二三四五六七八九十百千]+)(?:億|万)?円")),
]

# 質検層(evalkit)が「マスク漏れ」を判定するときに使う。生成者と同じ規則を共有することで
# 検査者が生成者より緩くなる（漏れを見逃す）事故を防ぐ。
LEAK_PATTERNS = [("PHONE", _PHONE_RE), ("EMAIL", _EMAIL_RE)]

# 法人格: 辞書実体と一体で消化する（「株式会社田中商事」→「B社」。「株式会社B社」を残さない）
_LEGAL_FORMS = ("株式会社", "有限会社", "合同会社", "合資会社", "合名会社")
_LEGAL_ALT = "|".join(_LEGAL_FORMS)

# 会社名: 法人格が前後に付く固有名 (辞書に無いものはこのパターンで拾う)
_COMPANY_PAT = re.compile(
    rf"(?:{_LEGAL_ALT})[一-龥ァ-ヶa-zA-Z0-9]{{2,12}}|[一-龥ァ-ヶa-zA-Z]{{2,12}}(?:{_LEGAL_ALT})"
)
# 人名: 「◯◯様」「◯◯氏」「◯◯さん」+ 役職 (2-4文字の漢字)
_HONORIFICS = ("様", "氏", "さん")
_TITLES = ("部長", "課長", "社長")
_PERSON_PAT = re.compile(
    rf"([一-龥]{{2,4}})({'|'.join(_HONORIFICS + _TITLES)})"
)
# 役職の直前に来ても人名ではない組織語（「人事部長」を人名扱いしないため）
_ORG_WORDS = frozenset(
    "人事 営業 総務 経理 開発 製造 品質 法務 広報 財務 企画 購買 情報 技術 管理 事業 研究 調達 物流 監査 経営".split()
)
# 生成済みラベル（A社 / AA社 / 担当者01）。再マスク・二重マスクを防ぐ
_COMPANY_LABEL_RE = re.compile(r"[A-Z]{1,3}社")
_PERSON_LABEL_RE = re.compile(r"担当者\d{2,}")
_LABEL_RE = re.compile(rf"{_COMPANY_LABEL_RE.pattern}|{_PERSON_LABEL_RE.pattern}")


def normalize(text: str) -> str:
    """全角/半角の表記揺れを潰す。マスキング前に必ず通す。

    ダッシュ類はここでは触らない（長音符 U+30FC を巻き込んで日本語を壊すため）。
    区切り文字の揺れは各正規表現側で _DASH として吸収する。
    """
    return unicodedata.normalize("NFKC", text)


def company_label(n: int) -> str:
    """0→A社, 25→Z社, 26→AA社 … 上限なし。先頭14件は旧実装(A社〜N社)と同じ順序。"""
    s = ""
    while True:
        s = chr(ord("A") + n % 26) + s
        n = n // 26 - 1
        if n < 0:
            return f"{s}社"


class Masker:
    """entities.json(コミット可・架空) と entities.local.json(gitignore・実名) をマージして読む。
    custom: {実語: 伏せ字} の直接指定（地名・製品名・拠点名など種別が合わないもの用）。"""

    def __init__(self, entities_path: str | None = None):
        self.dict_companies: list[str] = []
        self.dict_persons: list[str] = []
        self.custom: dict[str, str] = {}
        paths = []
        if entities_path:
            p = Path(entities_path)
            paths = [p, p.with_name("entities.local.json")]
        for p in paths:
            if p.exists():
                d = json.loads(p.read_text(encoding="utf-8"))
                self.dict_companies += d.get("companies", [])
                self.dict_persons += d.get("persons", [])
                self.custom.update(d.get("custom", {}))
        self._build_dict_pattern()

    def _build_dict_pattern(self) -> None:
        """辞書 + custom を1本の正規表現に畳む。

        逐次 str.replace() だと短い実体が長い実体の内部を先に食い潰す（例: custom「田中」が
        「田中商事」の照合を壊す）。最長一致優先の単一パスにすることで取りこぼしを防ぐ。
        """
        self._kinds: dict[str, str] = {}
        for name in self.custom:
            self._kinds[normalize(name)] = "custom"
        for name in self.dict_companies:
            self._kinds[normalize(name)] = "company"
        for name in self.dict_persons:
            self._kinds[normalize(name)] = "person"
        self._custom_norm = {normalize(k): v for k, v in self.custom.items()}

        alts = []
        for name in sorted(self._kinds, key=len, reverse=True):
            esc = re.escape(name)
            if self._kinds[name] == "company":
                # 法人格を前後どちらに付けても実体ごと消化する
                alts.append(rf"(?:{_LEGAL_ALT})?{esc}(?:{_LEGAL_ALT})?")
            else:
                alts.append(esc)
        self._dict_re = re.compile("|".join(alts)) if alts else None

    def _core_name(self, matched: str) -> str:
        """マッチ文字列から法人格を剥がして辞書キーに戻す。"""
        if matched in self._kinds:
            return matched
        core = matched
        for form in _LEGAL_FORMS:
            if core.startswith(form):
                core = core[len(form):]
                break
        for form in _LEGAL_FORMS:
            if core.endswith(form):
                core = core[: -len(form)]
                break
        return core

    def mask(self, text: str, mapping: dict | None = None) -> tuple[str, dict]:
        """text を脱敏し (脱敏後テキスト, 実名->伏せ字 の mapping) を返す。

        mapping を渡すと採番を引き継ぐ。複数文書（要件書 + RAG召回した先例）を跨いで
        同一実体に同一ラベルを与えるため。渡さない場合は毎回 A社/担当者01 から始まるので、
        別文書の別会社が同じラベルになり監査表が壊れる。
        """
        mapping = {} if mapping is None else mapping
        counters = {"company": 0, "person": 0}
        # 既存 mapping から採番位置を復元（custom の値は連番ラベルではないので数えない）
        for v in mapping.values():
            if _COMPANY_LABEL_RE.fullmatch(v):
                counters["company"] += 1
            elif _PERSON_LABEL_RE.fullmatch(v):
                counters["person"] += 1

        def label_for(kind: str, name: str) -> str:
            if name in mapping:
                return mapping[name]
            if kind == "company":
                lab = company_label(counters["company"])
                counters["company"] += 1
            else:
                counters["person"] += 1
                lab = f"担当者{counters['person']:02d}"   # 無制限・衝突なし
            mapping[name] = lab
            return lab

        out = normalize(text)

        # 辞書 + custom（単一パス・最長一致優先）
        if self._dict_re is not None:
            def _dict_sub(m: re.Match) -> str:
                core = self._core_name(m.group(0))
                kind = self._kinds.get(core)
                if kind == "custom":
                    label = self._custom_norm[core]
                    mapping[core] = label
                    return label
                if kind is None:      # 法人格を剥がしても辞書に無い = 想定外、原文維持せず会社扱い
                    kind = "company"
                return label_for(kind, core)
            out = self._dict_re.sub(_dict_sub, out)

        # パターン: 会社（辞書外）
        def _company_sub(m: re.Match) -> str:
            name = m.group(0)
            if _LABEL_RE.search(name):     # 既に伏せ字化済み
                return name
            return label_for("company", name)
        out = _COMPANY_PAT.sub(_company_sub, out)

        # パターン: 人名+敬称/役職（敬称・役職は残す）
        def _person_sub(m: re.Match) -> str:
            name, suffix = m.group(1), m.group(2)
            if _LABEL_RE.fullmatch(name) or name in mapping.values():
                return m.group(0)
            if suffix in _TITLES and name in _ORG_WORDS:
                return m.group(0)          # 「人事部長」は人名ではない
            return label_for("person", name) + suffix
        out = _PERSON_PAT.sub(_person_sub, out)

        # 正規表現ルール
        for tag, pat in _RULES:
            out = pat.sub(f"[{tag}]", out)
        return out, mapping


if __name__ == "__main__":
    import sys
    src = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else \
        "株式会社田中商事の佐藤様(TEL 03-1234-5678, sato@tanaka.co.jp)より、予算3,500万円のご相談。"
    ent = str(Path(__file__).parent / "entities.json")
    masked, mp = Masker(ent).mask(src)
    print(masked)
    print("mapping:", json.dumps(mp, ensure_ascii=False))
