"""Position / Company / Contact Intel."""
from __future__ import annotations
import re


SKILL_BANK = [
    "Allen-Bradley", "Rockwell", "Siemens S7", "Studio 5000", "RSLogix", "TIA Portal",
    "Beckhoff", "TwinCAT", "Mitsubishi PLC", "Modicon", "Omron", "PLC programming",
    "ladder logic", "Structured Text", "FactoryTalk", "Wonderware", "Ignition", "SCADA",
    "HMI", "EtherNet/IP", "Profinet", "Profibus", "Modbus", "OPC UA", "DeviceNet",
    "AutoCAD Electrical", "EPLAN", "SOLIDWORKS Electrical", "schematic capture",
    "motor control", "VFD", "servo drives", "PCB design", "Altium", "KiCad", "Cadence",
    "C", "C++", "embedded", "firmware", "microcontroller", "STM32", "ARM", "FPGA",
    "VHDL", "Verilog", "P&ID", "instrumentation", "calibration", "ROS", "FANUC",
    "ABB robot", "KUKA", "ISO 9001", "AS9100", "UL", "NFPA 79", "NEC", "Six Sigma",
    "Lean", "FMEA", "LabVIEW", "MATLAB", "Simulink", "Python",
]


def extract_skills(description, n=3):
    if not description:
        return []
    text = description.lower()
    hits = {}
    for sk in SKILL_BANK:
        c = text.count(sk.lower())
        if c > 0:
            hits[sk] = c + (2 if len(sk) > 6 else 0)
    ranked = sorted(hits.items(), key=lambda kv: (-kv[1], kv[0]))
    seen = set()
    out = []
    for sk, _ in ranked:
        norm = re.sub(r"[^a-z0-9]", "", sk.lower())
        if norm in seen:
            continue
        seen.add(norm)
        out.append(sk)
        if len(out) >= n:
            break
    return out
