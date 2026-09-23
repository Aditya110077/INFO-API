# main.py
import os
import json
import time
import threading
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf.json_format import MessageToDict

import AccountPersonalShow_pb2 as _7P

urllib3.disable_warnings()

# ============================================================
# REGION-WISE SERVER URLs
# ============================================================
REGION_SERVERS = {
    "IND": "https://client.ind.freefiremobile.com",
    "BD":  "https://clientbp.ggpolarbear.com",
}

# ============================================================
# REGION-WISE CREDENTIALS
# ============================================================
REGION_CREDS = {
    "IND": {
        "uid": "7723310557",
        "pw":  "F330768A0B6A3D69C88DA97868754D4EE99AEB600BDE5D98D53D8B234F1DD0D4"
    },
    "BD": {
        "uid": "7906685972",
        "pw":  "ARIYAN_MAX_BD_hmm8BSik"
    },
}

LOGIN_UID = REGION_CREDS["IND"]["uid"]
LOGIN_PW  = REGION_CREDS["IND"]["pw"]

# ============================================================
# CRYPTO KEYS
# ============================================================
_3K = b'Yg&tc%DEuh6%Zc^8'
_4V = b'6oyZDr22E3ychjM%'

# ============================================================
# TOKEN SERVER
# ============================================================
_TOK = "http://148.113.25.200:6293/Tok"

_6T  = 15
_8A  = "Dalvik/2.1.0 (Linux; U; Android 11)"
_9R  = "v1 1"
_10L = "OB55"

C = "\033[1;31m"; W = "\033[1;30m"; S = "\033[0m"
G = "\033[1;32m"; Y = "\033[1;33m"


def YoUr_MoM(d):
    return AES.new(_3K, AES.MODE_CBC, _4V).encrypt(pad(d, 16))


def UNknown(d):
    try:
        return unpad(AES.new(_3K, AES.MODE_CBC, _4V).decrypt(d), 16)
    except Exception:
        return d


def ReSPeCt_GiRLs(n):
    r = bytearray()
    while n >= 0x80:
        r.append((n & 0x7F) | 0x80)
        n >>= 7
    r.append(n)
    return bytes(r)


def YOuR_FaThER(uid):
    return YoUr_MoM(b"\x08" + ReSPeCt_GiRLs(int(uid)))


def LOvE_HaTe(uid, pw, region="IND"):
    try:
        r = requests.get(f"{_TOK}?uid={uid}&pw={pw}", timeout=_6T)
        if r.status_code != 200:
            return None

        j = r.json()
        if not j.get("Tok"):
            return None

        reg = region.upper()
        server = REGION_SERVERS.get(reg, REGION_SERVERS["IND"])

        return {
            "jwt":    j["Tok"],
            "addr":   j.get("addr") or server,
            "ver":    j.get("Ver", "1.132.7"),
            "ob":     j.get("Ob", _10L),
            "region": reg
        }
    except Exception:
        return None


def SiLeNt_KiLL(target_uid, login_uid=None, login_pw=None, region="IND"):
    reg = region.upper()
    res = {"jwt": None, "resp": None, "err": None, "region": reg}

    def InSiDe():
        try:
            if reg not in REGION_SERVERS:
                res["err"] = f"Unsupported region: {reg}"
                return

            creds = REGION_CREDS.get(reg)
            if not creds:
                res["err"] = f"No credentials for region: {reg}"
                return

            luid = login_uid or creds["uid"]
            lpw  = login_pw  or creds["pw"]

            tok = LOvE_HaTe(luid, lpw, reg)
            if not tok:
                res["err"] = f"JWT fetch failed for region {reg}"
                return

            res["jwt"] = tok["jwt"]
            res["region"] = tok["region"]

            headers = {
                "Authorization":  f"Bearer {tok['jwt']}",
                "Content-Type":   "application/x-www-form-urlencoded",
                "User-Agent":     _8A,
                "X-GA":           _9R,
                "ReleaseVersion": tok["ob"],
                "Connection":     "Keep-Alive",
            }

            res["resp"] = requests.post(
                f"{tok['addr']}/GetPlayerPersonalShow",
                headers=headers,
                data=YOuR_FaThER(target_uid),
                timeout=_6T,
                verify=False
            )
        except Exception as e:
            res["err"] = e

    t = threading.Thread(target=InSiDe)
    t.start()
    print(f" {C}[*]{W} FETCHING PERSONAL SHOW ({reg})...{S}")
    while t.is_alive():
        time.sleep(0.1)
    print(f" {G}[OK]{W} DONE{S}\n")
    return res


def full_json(dec_data):
    info = _7P.AccountPersonalShowInfo()
    info.ParseFromString(dec_data)

    kwargs = {
        "preserving_proto_field_name": True,
        "use_integers_for_enums": True
    }

    for arg in ("always_print_fields_with_no_presence",
                "including_default_value_fields"):
        try:
            return MessageToDict(info, **kwargs, **{arg: True})
        except TypeError:
            continue
    return MessageToDict(info, **kwargs)


def MaIn():
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print(f"{C}============================================={S}")
        print(f"{C}   FREE FIRE — PERSONAL SHOW (IND + BD)      {S}")
        print(f"{C}============================================={S}\n")

        region = input(f"{C}[?]{W} Region (IND/BD) : {S}").strip().upper()
        if region not in REGION_SERVERS:
            print(f"{C}[!] Invalid region. Use IND or BD{S}")
            input(f"\n{W}Press ENTER...{S}")
            continue

        target = input(f"{C}[?]{W} Target UID : {S}").strip()
        if not target or not target.isdigit():
            print(f"{C}[!] Invalid UID{S}")
            input(f"\n{W}Press ENTER...{S}")
            continue

        data = SiLeNt_KiLL(target, region=region)

        if data["err"]:
            print(f"{C}[!] Error: {data['err']}{S}")
        elif not data["jwt"]:
            print(f"{C}[!] Token fetch failed{S}")
        elif data["resp"] is None:
            print(f"{C}[!] No response{S}")
        elif data["resp"].status_code != 200:
            print(f"{C}[!] HTTP {data['resp'].status_code}{S}")
            print(f"{Y}{data['resp'].text[:400]}{S}")
        else:
            dec = UNknown(data["resp"].content)
            try:
                j = full_json(dec)
                print(f"{G}============= FULL JSON RESPONSE ============={S}")
                print(json.dumps(j, indent=2, ensure_ascii=False))
                print(f"{G}=============================================={S}")
                fn = f"player_{region}_{target}.json"
                with open(fn, "w", encoding="utf-8") as f:
                    json.dump(j, f, indent=2, ensure_ascii=False)
                print(f"{Y}[+] Saved to {fn}{S}")
            except Exception as e:
                print(f"{C}[!] Parse failed: {e}{S}")
                print(f"{Y}raw hex: {dec.hex()}{S}")

        print(f"\n{W}Press ENTER to continue (Ctrl+C to exit){S}")
        input()


if __name__ == "__main__":
    try:
        MaIn()
    except KeyboardInterrupt:
        print(f"\n{C}[!] Exited{S}")