# -*- coding: utf-8 -*-
"""日本語ビジネス文書のPII/機密マスキング（薄切片版）

方針:
  レイヤ1: 正規表現（電話/メール/郵便番号/金額/URL）
  レイヤ2: 辞書（既知の顧客企業名・人名 → config/entities.json）
  レイヤ3: パターン（「株式会社X」「X株式会社」「X様/氏」）
一貫性: 同一実体は文書全体で同一の伏せ字（田中商事→A社）にマッピングし、
        逆引き表(mapping)を返す。復元・監査に使う。

制限(薄切片): 辞書外の人名は「様/氏/さん」が付く場合のみ検出。
             本格版は GiNZA(NER) を重ねる予定 → docs/PITFALLS.md 参照。
"""
import json
import re
from pathlib import Path

_RULES = [
    ("PHONE",  re.compile(r"(?:0\d{1,4}[-(]\d{1,4}[-)]\d{3,4})")),
    ("EMAIL",  re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("POSTAL", re.compile(r"〒\d{3}-?\d{4}")),
    ("MONEY",  re.compile(r"(?:[0-9,，]+|[一二三四五六七八九十百千]+)(?:億|万)?円")),
    ("URL",    re.compile(r"https?://[^\s　]+")),
]
# 会社名: 株式会社が前後に付く固有名 (辞書に無いものはこのパターンで拾う)
_COMPANY_PAT = re.compile(r"(?:株式会社|有限会社)[一-龥ァ-ヶa-zA-Zａ-ｚＡ-Ｚ0-9０-９]{2,12}|[一-龥ァ-ヶa-zA-Z]{2,12}(?:株式会社|有限会社)")
# 人名: 「◯◯様」「◯◯氏」「◯◯さん」(2-4文字の漢字)
_PERSON_PAT = re.compile(r"([一-龥]{2,4})(様|氏|さん|部長|課長|社長)")

_COMPANY_LABELS = [f"{c}社" for c in "ABCDEFGHIJKLMN"]


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

    def mask(self, text: str) -> tuple[str, dict]:
        mapping: dict[str, str] = {}   # 実名 -> 伏せ字
        counters = {"company": 0, "person": 0}

        def label_for(kind: str, name: str) -> str:
            if name in mapping:
                return mapping[name]
            if kind == "company":
                lab = _COMPANY_LABELS[min(counters["company"], len(_COMPANY_LABELS) - 1)]
                counters["company"] += 1
            else:
                counters["person"] += 1
                lab = f"担当者{counters['person']:02d}"   # 無制限・衝突なし
            mapping[name] = lab
            return lab

        out = text
        # custom直接指定（最長一致優先。地名・製品名など）
        for name in sorted(self.custom, key=len, reverse=True):
            if name in out:
                out = out.replace(name, self.custom[name])
                mapping[name] = self.custom[name]
        # 辞書実体（最長一致優先）
        for name in sorted(self.dict_companies, key=len, reverse=True):
            if name in out:
                out = out.replace(name, label_for("company", name))
        for name in sorted(self.dict_persons, key=len, reverse=True):
            if name in out:
                out = out.replace(name, label_for("person", name))
        # パターン: 会社
        for m in list(_COMPANY_PAT.finditer(out)):
            name = m.group(0)
            if any(lab in name for lab in _COMPANY_LABELS):
                continue
            out = out.replace(name, label_for("company", name))
        # パターン: 人名+敬称（敬称は残す）。既に伏せ字化済みのラベルは再マスクしない
        def _person_sub(m: re.Match) -> str:
            name = m.group(1)
            if name.startswith("担当者") or name in mapping.values():
                return m.group(0)
            return label_for("person", name) + m.group(2)
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
