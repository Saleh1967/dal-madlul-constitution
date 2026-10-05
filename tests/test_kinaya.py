# -*- coding: utf-8 -*-
"""اختبار الكناية — أول اختبار حقيقي لمعنى المعنى: §58 الجرجاني بقاعدة وجودية مسجلة."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
KR = json.loads((ROOT / "data" / "kinaya_rules.json").read_text(encoding="utf-8"))
RULES = {r["from"]: r for r in KR["rules"]}
NEG = {n["surface"]: n for n in KR["negative_controls"]}


def resolve(surface: str):
    """المحرك الأدنى: قاعدة مسجلة أو رفض مسمّىً — لا اجتهاد."""
    if surface in RULES:
        return ("انتقال_مسجل", RULES[surface]["to"], RULES[surface]["id"])
    if surface in NEG:
        return ("رفض", NEG[surface]["expected"], None)
    return ("رفض", "رفض مسمّىً: بلا_قاعدة", None)


def test_gk1_registered_transition():
    verdict, target, rid = resolve("طويل النجاد")
    assert verdict == "انتقال_مسجل"
    assert target == "طويل القامة"
    assert rid == "KIN-1"
    assert "القامة" in RULES["طويل النجاد"]["rule"]


def test_gk2_registered_transition():
    verdict, target, rid = resolve("كثير رماد القدر")
    assert verdict == "انتقال_مسجل"
    assert target == "كثير القرى" and rid == "KIN-2"


def test_negative_control_no_rule():
    verdict, tag, _ = resolve("طويل السيف")
    assert verdict == "رفض" and "بلا_قاعدة" in tag


def test_unknown_surface_rejected_named():
    verdict, tag, _ = resolve("كثير الغبار")
    assert verdict == "رفض"
    # مسجل في الضوابط السلبية برفض مسمّى
    assert NEG["كثير الغبار"]["expected"] == "رفض مسمّىً: بلا_قاعدة"


def test_evidence_attached_to_every_rule():
    for r in KR["rules"]:
        assert r["evidence"].startswith("دلائل الإعجاز §58")
        assert r["bridge"]  # جسر النبهاني-الجرجاني مثبت


def test_every_rule_carries_lazum_metadata():
    for r in KR["rules"]:
        lz = r["lazum"]
        assert lz["degree"] in ("أخصّ", "مساوٍ")
        assert lz["manzila"] in ("وضعي", "عادي_وجودي", "شرعي")
        assert "عين التالي" in lz["form_used"]      # صيغة غير منتجة في الأخصّ
        assert lz["raiser"]["kind"]                  # لا صحة إلا برافع مسمّى
        assert "محكّ النظر" in lz["raiser"]["ghazali_check"]


def test_no_transition_without_registration():
    inv = " ".join(KR["invariants"])
    assert "لا انتقال إلا بقاعدة مسجلة" in inv
    assert "لا علاقة معجم" in inv
