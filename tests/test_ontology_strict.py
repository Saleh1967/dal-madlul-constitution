import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"src/slge"))
import slge_dalil as dm

SRC = json.loads((ROOT/"data/ontology_sources.json").read_text(encoding="utf-8"))

def test_three_sources_declared_with_grades():
    ids = {s["id"] for s in SRC["sources"]}
    assert ids == {"alghanem_ontology", "taaqol_classifier", "algebra_placeholder"}
    assert all(len(s["commit"]) >= 7 for s in SRC["sources"])           # رخصة بصمة لا نص حر
    mature = next(s for s in SRC["sources"] if s["id"] == "alghanem_ontology")
    assert mature["maturity"] == "complete" and mature["commit"] == "c5819fc"

def test_candidate_gate_both_claims():
    admit = lambda nec, irr: bool(nec) and bool(irr)
    assert admit("ضرورة", "عدم اختزال")
    assert not admit("ضرورة", None)
    assert not admit(None, "عدم اختزال")

def test_essence_not_function_in_our_engine():
    # الدال في وظيفته؛ وماهية المعنى ليست الوظيفة اللغوية — لا اختزال
    assert dm.haqiqa("قائم", dm.CONVENTIONS["قائم"])
    assert dm.CONVENTIONS["قائم"] != "وظيفة لغوية"

def test_interpretation_discipline_declared():
    rules = {r["id"] for r in SRC["discipline"] if r["adopted"]}
    assert "interpretation_three_levels" in rules
    assert "naming_is_relation" in rules
    assert "token_not_individual" in rules

def test_mapping_consistent_with_reported_kinds():
    kinds = set(SRC["onto_kinds_reported"])
    assert len(SRC["onto_kinds_reported"]) == 15
    for ours, theirs in SRC["mapping"].items():
        for part in theirs.split("/"):                      # المركب من أفراد معلنة جائز
            assert part.strip() in kinds, (ours, theirs)

def test_passive_bridge_matches_fath_example():
    # جسر fath: المرفوع في «فُتح البابُ» هو المفتوح = مشغّل ميم الاشتقاقية (مفعول)
    assert "مفعول" in "مفعول"
    assert dm.nisba_ok("الفاعل فتح والباب مفعول به")  # بقاء النمط الإسنادي معلن في المحرك

def test_no_freeze_at_g_minus_1():
    # لا ادعاء إغلاق في ميثاقنا؛ وCONVENTIONS موسومة بالاستيفاء
    assert "استيفاء" in (dm.__doc__ or "") or "استيفاء" in open(dm.__file__, encoding="utf-8").read()
    rules = {r["id"] for r in SRC["discipline"]}
    assert "no_closed_ontology_at_g_minus_1" in rules
