#!/usr/bin/env python3
"""appsec_mine_crypto_net.py - mine CRYPTO / NETWORK-SECURITY / AUTH-SESSION landmine facts
(insecure-by-default deprecations + habit-reversals) from three standards source-groups:

  1. RFCs        appsec-corpus/rfc/*.txt        (IETF Trust, short quotation)   -> TLS1.3/JWT/OAuth/HSTS/cookies/JWA
  2. NIST        appsec-corpus/nist/*.pdf       (NIST, public domain)           -> TLS/auth/crypto transitions
  3. Mozilla     appsec-corpus/mozilla-tls/json (Mozilla, MPL-2.0)              -> secure server-side TLS config

These sources are NORMATIVE PROSE, not code, so facts are mostly text-only (type DEPRECATED_CRYPTO /
HABIT_REVERSAL). Uses the shared pipeline appsec_core.run() for extract/ground/repair/dedupe.

usage:  DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python appsec_mine_crypto_net.py \
            [--only rfc|nist|mozilla] [--limit N] [--test]
out:    experts/appsec/facts/crypto_net.jsonl  (+ .rejects.jsonl)
"""
import glob, json, os, re, sys
import appsec_core as C

HERE = os.path.dirname(os.path.abspath(__file__))
CORP = os.path.join(HERE, "..", "..", "appsec-corpus")
OUT  = "experts/appsec/facts/crypto_net"

# ---- extra system guidance: these are NORMATIVE STANDARDS (prose), not tutorials -------------------
EXTRA_SYS = (
"This source is a NORMATIVE SECURITY STANDARD (an IETF RFC, a NIST Special Publication, or the Mozilla "
"server-side TLS config). Its rules are ground truth. Extract only landmine facts a code-generation model "
"gets WRONG BY DEFAULT: deprecated/forbidden crypto (MD5, SHA-1, RSA PKCS#1 v1.5, RC4, 3DES, DES, static "
"RSA/DH key exchange, CBC ciphers, TLS<1.2, SSLv3, weak/short keys), habit-reversals (reject alg:none, pin "
"algorithms, prefer RSAES-OAEP over PKCS1v1.5, require PKCE, drop the OAuth implicit flow, validate "
"certificates, set HSTS, Secure/HttpOnly/SameSite cookies, __Host- prefix). SKIP generic protocol "
"description, wire formats, state machines, IANA registries, and anything that is not a security "
"do/don't a developer would get wrong. Almost every fact here is TEXT-ONLY: set code_bad and code_good to "
"null unless a verbatim code snippet is literally present. type is DEPRECATED_CRYPTO for a "
"forbidden/deprecated algorithm or version, HABIT_REVERSAL when the trained default is now wrong. "
"door MUST be one of: crypto, network-security, auth-session. quote must be a SHORT verbatim phrase.")

# ---- normative-content gate: only feed sections that carry a security do/don't ---------------------
NORM_RE = re.compile(r"\b(MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|REQUIRED|"
                     r"deprecat|disallow|forbidden|prohibit|removed|no longer|obsolet|"
                     r"legacy use|weak|insecure|vulnerab|downgrade|must not be used|not approved)\b", re.I)
# security-vocab gate (drop normative sections that are pure protocol mechanics)
SEC_RE = re.compile(r"\b(TLS|SSL|cipher|RSA|SHA-?1|MD5|RC4|3DES|DES|CBC|OAEP|PKCS|hash|"
                    r"certificate|cert|HSTS|Strict-Transport|cookie|SameSite|Secure|HttpOnly|"
                    r"algorithm|alg|none|PKCE|implicit|redirect|token|JWT|JWS|JWE|OAuth|key|"
                    r"entropy|random|nonce|signature|encrypt|OCSP|renegotiat|compression|"
                    r"downgrade|version)\b", re.I)

def pick_door(text, default):
    """crypto (algorithms/keys/hashes) vs network-security (TLS versions/transport/HSTS) vs
    auth-session (tokens/cookies/oauth flows). Deterministic, forced per item so the door spread
    stays inside the 3 requested doors."""
    t = text.lower()
    auth = len(re.findall(r"\b(jwt|jws|jwe|token|oauth|pkce|implicit|redirect_uri|redirect uri|"
                          r"cookie|samesite|httponly|session|authoriz|__host|__secure|claim|audience|issuer)\b", t))
    net  = len(re.findall(r"\b(tls|ssl|hsts|strict-transport|renegotiat|downgrade|transport|"
                          r"handshake|ocsp|staple|protocol version|tlsv|sslv)\b", t))
    cry  = len(re.findall(r"\b(md5|sha-?1|sha-?256|rc4|3des|des|cbc|oaep|pkcs|rsa|ecdsa|hash|"
                          r"cipher|algorithm|key size|key length|entropy|random|nonce|signature|"
                          r"encrypt|curve|diffie|dh\b|kdf|hmac)\b", t))
    score = {"auth-session": auth, "network-security": net, "crypto": cry}
    best = max(score, key=score.get)
    return best if score[best] > 0 else default

# ==================== 1. RFC adapter =================================================================
RFC_META = {  # file stem -> (lib, version, default door)
 "rfc8446": ("tls",     "1.3 (RFC 8446)",  "network-security"),
 "rfc8725": ("jwt",     "BCP 225 (RFC 8725)", "auth-session"),
 "rfc9700": ("oauth",   "BCP 240 (RFC 9700)", "auth-session"),
 "rfc6797": ("hsts",    "RFC 6797",        "network-security"),
 "rfc6265": ("cookies", "RFC 6265",        "auth-session"),
 "rfc9110": ("http",    "RFC 9110",        "network-security"),
 "rfc7518": ("jwa",     "RFC 7518",        "crypto"),
}
# strong prohibition / deprecation verbs (the real landmines, not every MUST/SHOULD)
STRONG = re.compile(r"\b(MUST NOT|SHALL NOT|SHOULD NOT|deprecat|disallow|forbidden|prohibit|"
                    r"removed|no longer|obsolet|must not be used|not approved|not be used|weak|"
                    r"vulnerab|downgrade)\b", re.I)
# concrete weak/legacy primitives (bite signal for ranking)
PRIM = re.compile(r"\b(md5|sha-?1|rc4|3des|\bdes\b|cbc|export|null cipher|anon|sslv[23]|ssl 3|"
                  r"tls 1\.0|tls 1\.1|tlsv1\.0|tlsv1\.1|pkcs#?1|rsa1_5|rsaes-pkcs1|static (rsa|dh)|"
                  r"renegotiat|compression|\balg\b.{0,12}none|\"none\"|implicit (grant|flow)|"
                  r"pkce|includesubdomains|max-age|httponly|samesite|__host|__secure|oaep)", re.I)
# per-RFC section cap (keep the highest-bite sections; concentrate away from protocol mechanics)
RFC_CAP = {"jwt": 8, "oauth": 16, "jwa": 12, "cookies": 8, "hsts": 8, "tls": 14, "http": 8}

FOOTER = re.compile(r"^\S.*\[Page \d+\]\s*$")
HEADER = re.compile(r"^RFC \d+\s+.*\d{4}\s*$")
SECHDR = re.compile(r"^(\d+(?:\.\d+)*)\.\s+(\S.+)$")
APXHDR = re.compile(r"^(Appendix [A-Z](?:\.\d+)*)\.\s+(\S.+)$")

def clean_rfc(raw):
    out = []
    for ln in raw.replace("\f", "\n").split("\n"):
        if FOOTER.match(ln) or HEADER.match(ln): continue
        out.append(ln.rstrip())
    return "\n".join(out)

def split_rfc_sections(text):
    """Yield (secid, title, body). A header line is a top-of-body numbered/appendix heading."""
    lines = text.split("\n")
    secs, cur = [], None
    for ln in lines:
        m = SECHDR.match(ln) or APXHDR.match(ln)
        # a real heading: short, title-cased-ish, not a wrapped sentence (no trailing lowercase run)
        if m and len(ln) < 72 and not ln.rstrip().endswith((",", "the", "of", "a", "to")):
            if cur: secs.append(cur)
            cur = [m.group(1), m.group(2).strip(), []]
        elif cur:
            cur[2].append(ln)
    if cur: secs.append(cur)
    for sid, title, body in secs:
        yield sid, title, "\n".join(body).strip()

def rfc_items(limit=None):
    per_lib = {}   # lib -> list of (rank, item)
    for path in sorted(glob.glob(os.path.join(CORP, "rfc", "*.txt"))):
        stem = os.path.splitext(os.path.basename(path))[0]
        lib, ver, ddoor = RFC_META.get(stem, (stem, stem, "network-security"))
        raw = open(path, encoding="utf-8-sig").read()
        for sid, title, body in split_rfc_sections(clean_rfc(raw)):
            if len(body) < 120: continue
            if re.search(r"\b(References|IANA Considerations|Acknowledge|Contributors|Authors)\b", title, re.I):
                continue
            if not (SEC_RE.search(body) and STRONG.search(body)):   # strong prohibition/deprecation only
                continue
            corpus = f"RFC section {sid}. {title}\n\n{body}"[:6000]
            door = pick_door(title + " " + body, ddoor)
            rank = len(STRONG.findall(body)) + 2 * len(PRIM.findall(title + " " + body))
            per_lib.setdefault(lib, []).append((rank, {
                "llm_input": f"SOURCE: {lib} {ver}\nSECTION {sid}: {title}\n\n{body[:5500]}",
                "corpus": corpus, "source": f"{stem} §{sid}",
                "license_note": "IETF Trust, short quotation",
                "lib": lib, "version": ver, "door": door}))
    items = []
    for lib, lst in per_lib.items():
        lst.sort(key=lambda x: -x[0])
        items += [it for _, it in lst[:RFC_CAP.get(lib, 10)]]
    return items[:limit] if limit else items

# ==================== 2. NIST PDF adapter ============================================================
NIST_META = {  # file stem -> (lib, version, default door)
 "SP800-52r2":  ("tls-config",       "NIST SP 800-52r2",   "network-security"),
 "SP800-63b":   ("auth",             "NIST SP 800-63B",    "auth-session"),
 "SP800-131Ar2":("crypto-transition","NIST SP 800-131Ar2", "crypto"),
 "SP800-175Br1":("crypto-usage",     "NIST SP 800-175Br1", "crypto"),
}

def pdf_text(path):
    try:
        from pypdf import PdfReader
        r = PdfReader(path)
        return "\n".join((pg.extract_text() or "") for pg in r.pages)
    except Exception as e:
        print(f"  !! pypdf failed on {os.path.basename(path)}: {e}")
        return ""

def nist_chunks(text):
    """PDF text is messy: chunk on blank-line paragraph groups into ~2.5k windows on para boundary."""
    text = re.sub(r"[ \t]+", " ", text)
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    buf, size = [], 0
    for p in paras:
        buf.append(p); size += len(p)
        if size >= 2200:
            yield "\n\n".join(buf); buf, size = [], 0
    if buf: yield "\n\n".join(buf)

def nist_items(limit=None):
    items = []
    for path in sorted(glob.glob(os.path.join(CORP, "nist", "*.pdf"))):
        stem = os.path.splitext(os.path.basename(path))[0]
        lib, ver, ddoor = NIST_META.get(stem, (stem, stem, "crypto"))
        txt = pdf_text(path)
        if not txt.strip():
            print(f"  !! NIST {stem}: no extractable text, SKIPPING")
            continue
        n = 0
        for ch in nist_chunks(txt):
            if len(ch) < 200: continue
            if not (NORM_RE.search(ch) and SEC_RE.search(ch)): continue
            corpus = ch[:6000]
            door = pick_door(ch, ddoor)
            items.append({
                "llm_input": f"SOURCE: {lib} ({ver})\n\n{ch[:5500]}",
                "corpus": corpus, "source": ver,
                "license_note": "NIST, public domain",
                "lib": lib, "version": ver, "door": door})
            n += 1
        print(f"  NIST {stem}: {n} normative chunks queued")
    return items[:limit] if limit else items

# ==================== 3. Mozilla server-side TLS adapter ============================================
def moz_render(name, cfg):
    """Render one Mozilla config level into faithful normative prose (the grounding corpus)."""
    L = [f"Mozilla server-side TLS: {name} configuration."]
    tv = cfg.get("tls_versions") or []
    if tv:
        L.append(f"The {name} configuration enables only these TLS protocol versions: {', '.join(tv)}. "
                 f"All older protocol versions (SSLv2, SSLv3, TLS 1.0, TLS 1.1) are disabled.")
        if "TLSv1.2" in tv or "TLSv1.3" in tv:
            L.append("TLS versions below 1.2 must not be enabled.")
    if cfg.get("openssl_ciphersuites"):
        L.append(f"Permitted TLS 1.3 cipher suites: {', '.join(cfg['openssl_ciphersuites'])}.")
    if cfg.get("openssl_ciphers"):
        L.append(f"Permitted TLS 1.2 cipher suites (in order): {', '.join(cfg['openssl_ciphers'])}. "
                 f"Any cipher not on this list (RC4, 3DES, DES, export, NULL, anonymous, CBC-only legacy) is disabled.")
    if cfg.get("rsa_key_size"):
        L.append(f"Minimum RSA key size is {cfg['rsa_key_size']} bits.")
    if cfg.get("dh_param_size"):
        L.append(f"Minimum Diffie-Hellman parameter size is {cfg['dh_param_size']} bits.")
    if cfg.get("ecdh_param_size"):
        L.append(f"Minimum ECDH parameter size is {cfg['ecdh_param_size']} bits.")
    if cfg.get("tls_curves"):
        L.append(f"Permitted TLS curves: {', '.join(cfg['tls_curves'])}.")
    if cfg.get("hsts_min_age"):
        L.append(f"HTTP Strict Transport Security (HSTS) must be enabled with a max-age of at least "
                 f"{cfg['hsts_min_age']} seconds.")
    if cfg.get("ocsp_staple"):
        L.append("OCSP stapling must be enabled.")
    if cfg.get("maximum_certificate_lifespan"):
        L.append(f"Maximum certificate lifespan is {cfg['maximum_certificate_lifespan']} days.")
    if cfg.get("certificate_signatures"):
        L.append(f"Permitted certificate signature algorithms: {', '.join(cfg['certificate_signatures'])} "
                 f"(SHA-1 signatures are not permitted).")
    return "\n".join(L)

def moz_items(limit=None):
    items = []
    path = os.path.join(CORP, "mozilla-tls", "json", "server-side-tls-conf-5.0.json")
    data = json.load(open(path, encoding="utf-8"))
    ver = "Mozilla server-side TLS 5.0"
    # 'modern' and 'intermediate' hold the secure-config landmines; 'old' is the insecure legacy set
    for name in ("modern", "intermediate"):
        cfg = data.get("configurations", {}).get(name)
        if not cfg: continue
        corpus = moz_render(name, cfg)
        door = "network-security"
        items.append({
            "llm_input": f"SOURCE: Mozilla server-side TLS guidelines, '{name}' configuration.\n\n{corpus}\n\n"
                         "Emit the secure-configuration landmines (TLS version floor, forbidden weak ciphers, "
                         "minimum key sizes, HSTS max-age, OCSP stapling) a developer gets wrong by default.",
            "corpus": corpus, "source": f"mozilla-tls {name}",
            "license_note": "Mozilla, MPL-2.0",
            "lib": "tls-config", "version": ver, "door": door})
    return items[:limit] if limit else items

# ==================== driver ========================================================================
def main():
    only  = sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
    limit = int(sys.argv[sys.argv.index("--limit")+1]) if "--limit" in sys.argv else None
    test  = "--test" in sys.argv

    items = []
    if only in (None, "rfc"):     items += rfc_items()
    if only in (None, "nist"):    items += nist_items()
    if only in (None, "mozilla"): items += moz_items()

    print(f"\nadapters produced {len(items)} items"
          f" (rfc/nist/mozilla split computed by source prefix)")
    by = {}
    for it in items: by[it["source"].split()[0]] = by.get(it["source"].split()[0], 0) + 1
    for k, v in sorted(by.items()): print(f"    {k}: {v}")

    if test:
        items = items[:limit or 4]
        print(f"\n[TEST] mining {len(items)} items only")
    elif limit:
        items = items[:limit]

    door_ct = {}
    for it in items: door_ct[it["door"]] = door_ct.get(it["door"], 0) + 1
    print(f"item door spread: {door_ct}\n")

    C.run(items, OUT, extra_sys=EXTRA_SYS, id_prefix="std")

if __name__ == "__main__":
    main()
