# slge_dalil.py — محرك الدال والمدلول معًا: طبقة الدلالة في المنظومة
# المنهج: كتب الشخصية الثلاثة (الأول/التفكير/الثالث) — SLGE بالترخيص المتدرج.
# مقعده في العمود الفقري: بعد الإملاء وقبل المبنيات (المعنى يُبنى على الصوت ويحمل البنية).
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import slge

CONVENTIONS = {  # DL1: الوضع = تخصيص لفظ بمعنى (عينة معلنة؛ استيفاؤها رواية)
 "كتاب": "مجموع صحائف تُقرأ", "عِلْم": "معرفة بمعلومات وواقع مدرَك",
 "جَهْل": "نقص المعرفة", "مِنْ": "ابتداء وانفصال", "عَلَى": "علوّ واستعلاء",
 "قائم": "ثابت منتصب", "حَسَن": "ممدوح", "قَبِيح": "مذموم",
}
DALALAT = {"مطابقة": "تمام المسمى", "تضمن": "جزء المسمى", "تلويح": "لازم المسمى غير الجزء"}
NASAB   = {"إسنادية", "تقييدية", "إضافية"}
MANTUQ  = {"مطابقة", "تضمن", "تلويح"}                       # DL5: المنطوق
MAFHUM  = {"موافقة", "مخالفة_صفة", "مخالفة_شرط", "مخالفة_غاية", "مخالفة_عدد"}  # المفهوم (مغلق)

def dalala(word, mode):
    """DL2: الدلالة جائزة ⇐ نمطها من الثلاثة المغلقة."""
    return mode in DALALAT

def haqiqa(word, use):
    """DL3: الحقيقة = استعمال اللفظ فيما وُضع له."""
    return CONVENTIONS.get(word) == use

def majaz(word, use, qarina):
    """DL3: المجاز = استعمال في غير ما وُضع له لعلاقة، ولا يصح بلا قرينة."""
    return CONVENTIONS.get(word) != use and bool(qarina)

def nisba_ok(sentence):
    """DL4: غرض الوضع إفادة نسب من الثلاث (إسناد/تقييد/إضاف)."""
    return any(k in sentence for k in ("فاعل", "مفعول", "الذي", "ذو"))

def mantuq_or_mafhum(mode):
    """DL5: التقسيم التشريعي مغلق: منطوق (3) أو مفهوم (5) — لا ثالث."""
    return mode in MANTUQ or mode in MAFHUM

def maful(word, has_reality):
    """DL6: مفهوم ⇐ للمعنى واقع مدرَك (محسوس أو متصور مسلَّم به)؛ وإلا فهو معلومات لا مفاهيم."""
    return CONVENTIONS.get(word) if has_reality else None

if __name__ == "__main__":
    ok = True
    q = lambda b, n: (b, n)
    checks = [
      q(all(dalala(w, m) for m in DALALAT for w in list(CONVENTIONS)[:2]), "DL2 الدلالات الثلاث مغلقة"),
      q(not dalala("كتاب", "مخالفة"), "DL2 رفض النمط الخارج"),
      q(haqiqa("قائم", CONVENTIONS["قائم"]) and not haqiqa("قائم", "عالٍ"), "DL3 الحقيقة"),
      q(majaz("عِلْم", "كثير المال", qarina="المعنى الاصطلاحي") and not majaz("عِلْم", "كثير المال", qarina=None), "DL3 المجاز بلا قرينة مرفوض"),
      q(nisba_ok("زيد فاعل ضرب") and nisba_ok("الكتاب الذي قرأته"), "DL4 النسب الثلاث"),
      q(all(mantuq_or_mafhum(m) for m in list(MANTUQ) + list(MAFHUM)) and not mantuq_or_mafhum("إيماء"), "DL5 المنطوق والمفهوم مغلقان"),
      q(maful("عِلْم", True) == CONVENTIONS["عِلْم"] and maful("سحابة_اليقين", False) is None, "DL6 مفهوم/معلومات"),
      q(len(CONVENTIONS) >= 8 and len(MAFHUM) == 5 and len(DALALAT) == 3, "DL1/5 استيفاء العينات المعلنة"),
    ]
    for b, n in checks:
        ok &= b; print(f"  {'✓' if b else '⛔'} {n}")
    print("SLGE-DALIL:", "ALL PASS — signifier and signified, licensed" if ok else "BREACH")
    sys.exit(0 if ok else 1)
