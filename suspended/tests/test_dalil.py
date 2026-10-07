import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"src/slge"))
import slge_dalil as dm
def test_conventions_and_dalalat():
    assert dm.haqiqa("قائم", dm.CONVENTIONS["قائم"])
    assert all(dm.dalala("كتاب", m) for m in dm.DALALAT)
def test_majaz_needs_qarina():
    assert dm.majaz("عِلْم", "غزير", qarina="اصطلاح")
    assert not dm.majaz("عِلْم", "غزير", qarina=None)
def test_mantuq_mafhum_closed():
    assert all(dm.mantuq_or_mafhum(m) for m in list(dm.MANTUQ) + list(dm.MAFHUM))
def test_sources_present():
    d = (ROOT/"data/nabhani_sources.json").read_text(encoding="utf-8")
    assert "الدال" in d and "المدلول" in d and "الرواية" in d
