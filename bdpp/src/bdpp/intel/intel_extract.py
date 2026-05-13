"""The three Intel features.

Each one is independently toggleable. Position Intel runs heuristically with no API spend;
Company Intel and Contact Intel use Anthropic if a key is set, otherwise they fall back to None.
"""
from __future__ import annotations

import re
from typing import Optional


# A curated bank of engineering skill keywords commonly found in Controls / Electrical Engineer postings.
SKILL_BANK = [
    # PLCs / control systems
    "Allen-Bradley", "Allen Bradley", "Rockwell", "Siemens S7", "Siemens PLC", "Studio 5000",
    "RSLogix", "TIA Portal", "Beckhoff", "TwinCAT", "Mitsubishi PLC", "Modicon", "Omron",
    "PLC programming", "ladder logic", "Structured Text",
    # HMI / SCADA
    "FactoryTalk", "Wonderware", "Ignition", "WinCC", "iFIX", "SCADA", "HMI",
    # Industrial protocols
    "EtherNet/IP", "Profinet", "Profibus", "Modbus", "OPC UA", "DeviceNet", "CAN bus", "CANopen",
    # Electrical / power
    "AutoCAD Electrical", "EPLAN", "SOLIDWORKS Electrical", "schematic capture",
    "motor control", "VFD", "servo drives", "stepper", "480V", "three-phase",
    "PCB design", "Altium", "KiCad", "Cadence", "Eagle CAD",
    # Embedded / firmware
    "C", "C++", "embedded", "firmware", "microcontroller", "STM32", "PIC", "ARM",
    "FPGA", "VHDL", "Verilog", "Xilinx", "Altera",
    # Process / instrumentation
    "P&ID", "P and ID", "P-and-ID", "instrumentation", "calibration", "ISA-5.1",
    # Robotics
    "robotics", "ROS", "kinematics", "motion planning", "FANUC", "ABB robot", "KUKA",
    "Universal Robots", "UR10",
    # Quality / standards
    "ISO 9001", "AS9100", "UL", "NFPA 79", "NEC", "IPC-A-610",
    # Methods
    "Six Sigma", "Lean", "Kaizen", "DFM", "DFMA", "FMEA",
    # Software / tools used by EEs/Controls
    "LabVIEW", "MATLAB", "Simulink", "Python", "SQL",
    # Hardware test / instrumentation
    "oscilloscope", "DAQ", "soldering",
]


def extract_skills_heuristic(description: str, max_skills: int = 3) -> list[str]:
    """Pull the top N skill keywords from a job description by frequency + appearance."""
    if not description:
        return []
    text = description.lower()
    hits: dict[str, int] = {}
    for sk in SKILL_BANK:
        key = sk.lower()
        # Count occurrences — penalize very short keywords
        count = text.count(key)
        if count > 0:
            hits[sk] = count + (2 if len(sk) > 6 else 0)
    # Rank & dedupe near-duplicates (Allen Bradley vs Allen-Bradley)
    ranked = sorted(hits.items(), key=lambda kv: (-kv[1], kv[0]))
    seen_norm: set[str] = set()
    out: list[str] = []
    for skill, _ in ranked:
        norm = re.sub(r"[^a-z0-9]", "", skill.lower())
        if norm in seen_norm:
            continue
        seen_norm.add(norm)
        out.append(skill)
        if len(out) >= max_skills:
            break
    return out


def run_intel(
    *,
    description: str,
    enable_position: bool,
    enable_company: bool,
    enable_contact: bool,
    company_what: Optional[str] = None,
    contact_signal: Optional[str] = None,
) -> dict:
    """Return {'position_skills': [..], 'company_intel': str|None, 'contact_intel': str|None}."""
    out = {"position_skills": [], "company_intel": None, "contact_intel": None}
    if enable_position:
        out["position_skills"] = extract_skills_heuristic(description, max_skills=3)
    if enable_company and company_what:
        # Trim to <10 words, lower-case-first form
        words = company_what.strip().rstrip(".").split()
        out["company_intel"] = " ".join(words[:10])
    if enable_contact and contact_signal:
        out["contact_intel"] = contact_signal[:160]
    return out
