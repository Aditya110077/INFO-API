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

LOGIN_UID = "7723310557"
LOGIN_PW  = "F330768A0B6A3D69C88DA97868754D4EE99AEB600BDE5D98D53D8B234F1DD0D4"

_3K = b'Yg&tc%DEuh6%Zc^8'
_4V = b'6oyZDr22E3ychjM%'
_5B  = "https://client.ind.freefiremobile.com"
_TOK = "http://148.113.25.200:6293/Tok"

_6T  = 15
_8A  = "Dalvik/2.1.0 (Linux; U; Android 11)"
_9R  = "v1 1"
_10L = "OB55"

C = "\033[1;31m"; W = "\033[1;30m"; S = "\033[0m"
G = "\033[1;32m"; Y = "\033[1;33m"


def YoUr_MoM(d): return AES.new(_3K, AES.MODE_CBC, _4V).encrypt(pad(d, 16))

def UNknown(d):
    try:    return unpad(AES.new(_3K, AES.MODE_CBC, _4V).decrypt(d), 16)
    except: return d

def ReSPeCt_GiRLs(n):
    r = bytearray()
    while n >= 0x80:
        r.append((n & 0x7F) | 0x80); n >>= 7
    r.append(n); return bytes(r)

def YOuR_FaThER(uid):
    return YoUr_MoM(b"\x08" + ReSPeCt_GiRLs(int(uid)))


def LOvE_HaTe(uid, pw):
    try:
        r = requests.get(f"{_TOK}?uid={uid}&pw={pw}", timeout=_6T)
        if r.status_code != 200: return None
        j = r.json()
        if not j.get("Tok"): return None
        return {"jwt": j["Tok"], "addr": j.get("addr", _5B),
                "ver": j.get("Ver", "1.132.7"), "ob": j.get("Ob", _10L)}
    except Exception:
        return None


def SiLeNt_KiLL(target_uid, login_uid, login_pw):
    res = {"jwt": None, "resp": None, "err": None}

    def InSiDe():
        try:
            tok = LOvE_HaTe(login_uid, login_pw)
            if not tok:
                res["err"] = "JWT fetch failed"
                return
            res["jwt"] = tok["jwt"]
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
                headers=headers, data=YOuR_FaThER(target_uid),
                timeout=_6T, verify=False)
        except Exception as e:
            res["err"] = e

    t = threading.Thread(target=InSiDe); t.start()
    print(f" {C}[*]{W} FETCHING PERSONAL SHOW...{S}")
    while t.is_alive(): time.sleep(0.1)
    print(f" {G}[OK]{W} DONE{S}\n")
    return res


def full_json(dec_data):
    """Version-agnostic full JSON dump."""
    info = _7P.AccountPersonalShowInfo()
    info.ParseFromString(dec_data)

    kwargs = {"preserving_proto_field_name": True,
              "use_integers_for_enums": True}

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
        print(f"{C}   FREE FIRE — PERSONAL SHOW (FULL JSON)     {S}")
        print(f"{C}============================================={S}\n")
        print(f" {W}Login UID : {LOGIN_UID}{S}\n")

        target = input(f"{C}[?]{W} Target UID : {S}").strip()
        if not target or not target.isdigit():
            print(f"{C}[!] Invalid UID{S}")
            input(f"\n{W}Press ENTER...{S}"); continue

        data = SiLeNt_KiLL(target, LOGIN_UID, LOGIN_PW)

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
                fn = f"player_{target}.json"
                with open(fn, "w", encoding="utf-8") as f:
                    json.dump(j, f, indent=2, ensure_ascii=False)
                print(f"{Y}[+] Saved to {fn}{S}")
            except Exception as e:
                print(f"{C}[!] Parse failed: {e}{S}")
                print(f"{Y}raw hex: {dec.hex()}{S}")

        print(f"\n{W}Press ENTER to continue (Ctrl+C to exit){S}")
        input()


# ============================================================
# RENDER / GUNICORN ENTRYPOINT
# Is part ko add karna zaroori tha, warna gunicorn error dega.
# ============================================================
if __name__ == "__main__":
    # Sirf terminal mode (agar aap manually chalao toh)
    # Render pe gunicorn isko execute nahi karega, woh `aditya:app` use karega
    try:
        MaIn()
    except KeyboardInterrupt:
        print(f"\n{C}[!] Exited{S}")