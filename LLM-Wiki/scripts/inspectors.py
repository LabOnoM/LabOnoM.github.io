"""Format-aware file inspection and digest utilities for LLM-Wiki.

Distinguishes full-file raw SHA-256 digests from Git blob SHA-1 OIDs and Git
commit IDs, and inspects scientific, document, spreadsheet, presentation,
statistical, image, microscopy, omics, and source-code formats using Python
standard-library parsers and magic-byte signatures.
"""

from __future__ import annotations

import ast
import csv
import gzip
import hashlib
import io
import json
import re
import struct
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Files visually inspected via multimodal image examination and documented in LLM-Wiki/figures/
VISUALLY_INSPECTED_IMAGES = frozenset(
    {
        "_posts/PostAttachedFiles/IGV_BAM_Screenshot.png",
        "_posts/PostAttachedFiles/Identical_Statistical_Results_qPCR.png",
        "_posts/PostAttachedFiles/Identical_qPCR_Results.png",
        "_posts/PostAttachedFiles/GitHub_Issue_20250604.png",
        "_posts/PostAttachedFiles/AI_Response_20250604.png",
        "_posts/PostAttachedFiles/NatureLifeCycleVsLabLifeCycle.png",
        "_posts/PostAttachedFiles/Zebrafish-evolution-and-range.png",
        "img/Software_brief.jpeg",
        "img/gallery/Ono_2025.jpg",
    }
)

TEXT_EXTENSIONS = frozenset(
    {
        ".md",
        ".markdown",
        ".txt",
        ".py",
        ".js",
        ".sh",
        ".rb",
        ".yml",
        ".yaml",
        ".json",
        ".jsonl",
        ".css",
        ".scss",
        ".xml",
        ".svg",
        ".csv",
        ".tsv",
        ".html",
        ".htm",
        ".gemspec",
        ".gitignore",
        ".regentignore",
    }
)

TEXT_BASENAMES = frozenset(
    {"Gemfile", "LICENSE", "CNAME", ".gitignore", ".regentignore"}
)


def compute_raw_sha256(data: bytes) -> str:
    """Return 64-hex SHA-256 of exact raw file bytes."""
    return hashlib.sha256(data).hexdigest()


def compute_git_blob_oid(data: bytes) -> str:
    """Return 40-hex Git blob SHA-1 OID: sha1('blob <len>\\0' + data)."""
    header = f"blob {len(data)}\x00".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _parse_png_info(data: bytes) -> Dict[str, Any]:
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
        color_map = {
            0: "grayscale",
            2: "rgb",
            3: "indexed",
            4: "grayscale_alpha",
            6: "rgba",
        }
        return {
            "width": width,
            "height": height,
            "bit_depth": bit_depth,
            "color_mode": color_map.get(color_type, f"code_{color_type}"),
        }
    return {}


def _parse_jpeg_info(data: bytes) -> Dict[str, Any]:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return {}
    idx = 2
    sof_markers = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    while idx + 4 <= len(data):
        if data[idx] != 0xFF:
            idx += 1
            continue
        while idx < len(data) and data[idx] == 0xFF:
            idx += 1
        if idx >= len(data):
            break
        marker = data[idx]
        idx += 1
        if marker in (0xD8, 0xD9) or (0xD0 <= marker <= 0xD7):
            continue
        if idx + 2 > len(data):
            break
        seg_len = struct.unpack(">H", data[idx : idx + 2])[0]
        if seg_len < 2 or idx + seg_len > len(data):
            break
        if marker in sof_markers and idx + 7 < len(data):
            precision = data[idx + 2]
            height, width, components = struct.unpack(">HHB", data[idx + 3 : idx + 8])
            return {
                "width": width,
                "height": height,
                "bit_depth": precision,
                "channels": components,
            }
        idx += seg_len
    return {}


def _parse_gif_info(data: bytes) -> Dict[str, Any]:
    if len(data) < 10 or data[:6] not in (b"GIF87a", b"GIF89a"):
        return {}
    width, height = struct.unpack("<HH", data[6:10])
    # Approximation of frame count via Graphic Control Extension / Image Separator
    gce_frames = data.count(b"\x21\xf9\x04")
    return {
        "gif_version": data[:6].decode("ascii"),
        "width": width,
        "height": height,
        "estimated_frames": max(1, gce_frames),
    }


def _parse_ico_info(data: bytes) -> Dict[str, Any]:
    if len(data) < 22 or data[:4] != b"\x00\x00\x01\x00":
        return {}
    count = struct.unpack("<H", data[4:6])[0]
    w = data[6] or 256
    h = data[7] or 256
    bpp = struct.unpack("<H", data[12:14])[0]
    return {"icon_entries": count, "primary_width": w, "primary_height": h, "bpp": bpp}


def _parse_tiff_info(data: bytes) -> Dict[str, Any]:
    if len(data) < 8:
        return {}
    endian = "<" if data[:2] == b"II" else (">" if data[:2] == b"MM" else None)
    if not endian:
        return {}
    magic = struct.unpack(endian + "H", data[2:4])[0]
    if magic == 43:
        return {"tiff_variant": "BigTIFF_64bit"}
    if magic != 42:
        return {}
    ifd_offset = struct.unpack(endian + "I", data[4:8])[0]
    info: Dict[str, Any] = {"tiff_variant": "Baseline_TIFF"}
    if ifd_offset + 2 <= len(data):
        num_entries = struct.unpack(endian + "H", data[ifd_offset : ifd_offset + 2])[0]
        pos = ifd_offset + 2
        for _ in range(min(num_entries, 64)):
            if pos + 12 > len(data):
                break
            tag, typ, cnt, val_bytes = struct.unpack(
                endian + "HHII", data[pos : pos + 12]
            )
            pos += 12
            if tag == 256:
                info["width"] = val_bytes
            elif tag == 257:
                info["height"] = val_bytes
            elif tag == 277:
                info["samples_per_pixel"] = val_bytes
            elif tag == 270 and cnt < 65536 and val_bytes + cnt <= len(data):
                desc = data[val_bytes : val_bytes + min(cnt, 512)].decode(
                    "utf-8", errors="ignore"
                )
                if "OME" in desc:
                    info["tiff_variant"] = "OME-TIFF"
    return info


def _parse_thermo_raw(data: bytes) -> Dict[str, Any]:
    # Thermo Finnigan Xcalibur RAW files store UTF-16LE "Finnigan" at offset 2
    if len(data) >= 64 and b"F\x00i\x00n\x00n\x00i\x00g\x00a\x00n\x00" in data[:64]:
        version = struct.unpack("<I", data[36:40])[0] if len(data) >= 40 else None
        return {"instrument_vendor": "Thermo_Finnigan", "raw_header_version": version}
    return {}


def _parse_xlsx(zf: zipfile.ZipFile) -> Dict[str, Any]:
    ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    sheets: List[str] = []
    if "xl/workbook.xml" in zf.namelist():
        root = ET.fromstring(zf.read("xl/workbook.xml"))
        for sh in root.findall(".//s:sheet", ns):
            sheets.append(sh.attrib.get("name", ""))
    formula_cells = 0
    nonempty_cells = 0
    for name in zf.namelist():
        if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"):
            sroot = ET.fromstring(zf.read(name))
            for cell in sroot.findall(".//s:c", ns):
                has_f = cell.find("s:f", ns) is not None
                has_v = cell.find("s:v", ns) is not None
                if has_f:
                    formula_cells += 1
                if has_f or has_v:
                    nonempty_cells += 1
    return {
        "sheet_count": len(sheets),
        "sheets": sheets,
        "nonempty_cells": nonempty_cells,
        "formula_cells": formula_cells,
    }


def _parse_pptx(zf: zipfile.ZipFile) -> Dict[str, Any]:
    slides = [
        n
        for n in zf.namelist()
        if n.startswith("ppt/slides/slide") and n.endswith(".xml")
    ]
    chars = 0
    for s in slides:
        txt = re.sub(r"<[^>]+>", " ", zf.read(s).decode("utf-8", errors="ignore"))
        chars += len(txt.strip())
    return {"slide_count": len(slides), "extracted_text_chars": chars}


def _parse_docx(zf: zipfile.ZipFile) -> Dict[str, Any]:
    if "word/document.xml" not in zf.namelist():
        return {"paragraphs": 0}
    xml_bytes = zf.read("word/document.xml")
    root = ET.fromstring(xml_bytes)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paras = root.findall(".//w:p", ns)
    texts = [t.text or "" for t in root.findall(".//w:t", ns)]
    return {"paragraphs": len(paras), "extracted_text_chars": sum(len(t) for t in texts)}


def _parse_prism_zip(zf: zipfile.ZipFile) -> Dict[str, Any]:
    names = zf.namelist()
    version = None
    if "document.json" in names:
        doc = json.loads(zf.read("document.json").decode("utf-8", errors="replace"))
        version = doc.get("prismVersion") or doc.get("fileVersion")
        if isinstance(doc.get("createdBy"), dict):
            version = doc["createdBy"].get("prismVersion", version)
    tables = [n for n in names if n.startswith("data/tables/") and n.endswith("/data.csv")]
    analyses: List[str] = []
    for n in sorted(names):
        if n.startswith("analyses/") and n.endswith("/parameters.json"):
            pdata = json.loads(zf.read(n).decode("utf-8", errors="replace"))
            atype = pdata.get("analysisType") or pdata.get("title") or "unknown"
            analyses.append(str(atype))
    return {
        "prism_version": version,
        "table_count": len(tables),
        "analysis_count": len(analyses),
        "analysis_types": analyses,
    }


def _parse_pdf(data: bytes) -> Tuple[str, Dict[str, Any]]:
    m = re.match(rb"%PDF-(\d+\.\d+)", data[:16])
    version = m.group(1).decode("ascii") if m else "unknown"
    pages = len(re.findall(rb"/Type\s*/Page\b", data))
    streams = len(re.findall(rb"\bstream\r?\n", data))
    has_text_ops = bool(re.search(rb"\bBT\b.*?\bET\b", data, flags=re.DOTALL))
    status = "inspected_structured" if (pages > 0 or has_text_ops) else "inspected_metadata_only"
    return status, {
        "pdf_version": version,
        "estimated_pages": pages,
        "stream_objects": streams,
    }


def _parse_ms_office_lock(data: bytes) -> Dict[str, Any]:
    owner = ""
    if len(data) >= 2:
        name_len = data[0]
        if 1 <= name_len <= 64 and 1 + name_len <= len(data):
            candidate = data[1 : 1 + name_len].decode("utf-8", errors="ignore")
            if candidate.isprintable():
                owner = candidate
    if not owner:
        m = re.search(rb"([A-Za-z][A-Za-z0-9 _.-]{2,40})", data)
        if m:
            owner = m.group(1).decode("ascii", errors="ignore")
    return {"lock_owner": owner, "byte_length": len(data)}


def _parse_markdown(text: str) -> Dict[str, Any]:
    lines = text.splitlines()
    fm_keys: List[str] = []
    if lines and lines[0].strip() == "---":
        for ln in lines[1:80]:
            if ln.strip() == "---":
                break
            m = re.match(r"^([A-Za-z0-9_-]+)\s*:", ln)
            if m:
                fm_keys.append(m.group(1))
    headings = [ln.lstrip("#").strip() for ln in lines if re.match(r"^#{1,3}\s+", ln)]
    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", text)
    return {
        "line_count": len(lines),
        "frontmatter_keys": fm_keys,
        "heading_count": len(headings),
        "top_headings": headings[:5],
        "wikilink_count": len(wikilinks),
    }


def _parse_html(text: str, raw_size: int) -> Tuple[str, bool, str, Dict[str, Any]]:
    stripped = text.lstrip()
    lines = text.splitlines()
    # Check LiteSpeed 404 HTML error stubs saved in asset directories
    if "404 Not Found" in text and "LiteSpeed Web Server" in text and raw_size < 1024:
        return (
            "html_404_error_stub",
            True,
            "inspected_anomalous",
            {"line_count": len(lines), "server_stub": "LiteSpeed_404"},
        )
    # Check truncated mid-tag HTML fragment (e.g., 00.NIH_10xVisiumHD.html starting with </script>)
    if stripped.startswith("</"):
        return (
            "html_truncated_fragment",
            True,
            "inspected_anomalous",
            {
                "line_count": len(lines),
                "is_truncated_artifact": True,
                "prefix": stripped[:60],
            },
        )
    # Check Jupyter Notebook HTML export
    if "jp-Notebook" in text or "jp-Cell" in text or "ipynb" in text[:4096]:
        code_cells = len(re.findall(r'class="[^"]*jp-CodeCell[^"]*"', text))
        md_cells = len(re.findall(r'class="[^"]*jp-MarkdownCell[^"]*"', text))
        embedded_pngs = len(re.findall(r"data:image/png;base64,", text))
        title_m = re.search(r"<title>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
        return (
            "jupyter_html_notebook",
            False,
            "inspected_full",
            {
                "line_count": len(lines),
                "title": title_m.group(1).strip() if title_m else "",
                "code_cells": code_cells,
                "markdown_cells": md_cells,
                "embedded_png_count": embedded_pngs,
            },
        )
    title_m = re.search(r"<title>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
    return (
        "html_document",
        False,
        "inspected_full",
        {
            "line_count": len(lines),
            "title": title_m.group(1).strip() if title_m else "",
            "has_frontmatter": stripped.startswith("---"),
        },
    )


def _parse_python(text: str) -> Dict[str, Any]:
    lines = text.splitlines()
    try:
        tree = ast.parse(text)
        funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        return {
            "line_count": len(lines),
            "function_count": len(funcs),
            "functions": funcs[:15],
            "class_count": len(classes),
            "classes": classes[:10],
        }
    except SyntaxError as exc:
        return {"line_count": len(lines), "syntax_error": str(exc)}


def _parse_delimited(text: str, delimiter: str) -> Dict[str, Any]:
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    rows = list(reader)
    header = rows[0] if rows else []
    return {
        "row_count": max(0, len(rows) - 1),
        "column_count": len(header),
        "columns": header[:20],
    }


def inspect_workspace_file(
    abs_path: Path,
    rel_path: str,
    git_index_oid: Optional[str] = None,
) -> Dict[str, Any]:
    """Read, hash, and inspect a single workspace file with format-specific parsers."""
    stat = abs_path.stat()
    size_bytes = stat.st_size
    mtime_ns = stat.st_mtime_ns
    mtime_utc = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    ext = abs_path.suffix.lower()
    basename = abs_path.name

    try:
        data = abs_path.read_bytes()
    except OSError as exc:
        return {
            "rel_path": rel_path,
            "size_bytes": size_bytes,
            "mtime_ns": mtime_ns,
            "mtime_utc": mtime_utc,
            "raw_sha256": None,
            "working_git_blob_oid": None,
            "git_index_blob_oid": git_index_oid,
            "git_tracked": git_index_oid is not None,
            "git_dirty_vs_index": None,
            "ext": ext,
            "detected_format": "unreadable",
            "format_mismatch": False,
            "inspection_status": "unhashed",
            "summary_metrics": {"error": str(exc)},
        }

    raw_sha256 = compute_raw_sha256(data)
    working_blob_oid = compute_git_blob_oid(data)
    git_tracked = git_index_oid is not None
    git_dirty = (working_blob_oid != git_index_oid) if git_tracked else None

    detected_format = "unknown_binary"
    format_mismatch = False
    inspection_status = "unsupported"
    metrics: Dict[str, Any] = {}

    # 1. MS Office owner lock file check (~$*.pptx, ~$*.xlsx, ~$*.docx)
    if basename.startswith("~$") and ext in (".pptx", ".xlsx", ".docx") and data[:4] != b"PK\x03\x04":
        detected_format = "ms_office_owner_lock"
        format_mismatch = True
        inspection_status = "inspected_anomalous"
        metrics = _parse_ms_office_lock(data)

    # 2. ZIP-based archives (.xlsx, .pptx, .docx, .prism, .zip)
    elif data[:4] == b"PK\x03\x04":
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                names = set(zf.namelist())
                if ext == ".prism" or "document.json" in names:
                    detected_format = "graphpad_prism_zip"
                    inspection_status = "inspected_structured"
                    metrics = _parse_prism_zip(zf)
                elif "xl/workbook.xml" in names:
                    detected_format = "ooxml_xlsx_spreadsheet"
                    inspection_status = "inspected_structured"
                    metrics = _parse_xlsx(zf)
                elif any(n.startswith("ppt/") for n in names):
                    detected_format = "ooxml_pptx_presentation"
                    inspection_status = "inspected_structured"
                    metrics = _parse_pptx(zf)
                elif "word/document.xml" in names:
                    detected_format = "ooxml_docx_document"
                    inspection_status = "inspected_structured"
                    metrics = _parse_docx(zf)
                else:
                    detected_format = "zip_archive"
                    inspection_status = "inspected_structured"
                    metrics = {"entry_count": len(names)}
        except zipfile.BadZipFile as exc:
            detected_format = "corrupted_zip_container"
            format_mismatch = True
            inspection_status = "inspected_anomalous"
            metrics = {"zip_error": str(exc)}

    # 3. Legacy OLE2 Compound Document (.xls, .doc, .ppt)
    elif data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        detected_format = "ole2_compound_document"
        inspection_status = "inspected_metadata_only"
        metrics = {"ole2_bytes": size_bytes}

    # 4. PDF
    elif data[:5] == b"%PDF-":
        detected_format = "pdf_document"
        inspection_status, metrics = _parse_pdf(data)

    # 5. Thermo Finnigan mass spectrometry .RAW
    elif _parse_thermo_raw(data):
        detected_format = "thermo_finnigan_raw"
        inspection_status = "inspected_metadata_only"
        metrics = _parse_thermo_raw(data)

    # 6. TIFF / BigTIFF / OME-TIFF / Camera TIFF-RAW
    elif data[:4] in (b"II*\x00", b"MM\x00*", b"II+\x00", b"MM\x00+"):
        metrics = _parse_tiff_info(data)
        detected_format = (
            "camera_tiff_raw"
            if ext == ".raw"
            else metrics.get("tiff_variant", "tiff_image").lower()
        )
        inspection_status = "inspected_structured"

    # 7. HDF5 / AnnData (.h5, .hdf5, .h5ad)
    elif data[:8] == b"\x89HDF\r\n\x1a\n":
        detected_format = "hdf5_container"
        inspection_status = "inspected_metadata_only"
        metrics = {"hdf5_superblock_version": data[8] if len(data) > 8 else None}

    # 8. Gzip / BGZF (.gz, .bam, .fq.gz)
    elif data[:2] == b"\x1f\x8b":
        is_bgzf = len(data) >= 16 and data[12:14] == b"BC"
        detected_format = "bgzf_genomics_stream" if is_bgzf else "gzip_archive"
        inspection_status = "inspected_metadata_only"
        try:
            sample = gzip.decompress(data[:65536])[:256]
            if sample[:4] == b"BAM\x01":
                detected_format = "bam_alignment"
        except Exception:
            pass
        metrics = {"bgzf": is_bgzf}

    # 9. Apache Parquet
    elif data[:4] == b"PAR1":
        detected_format = "apache_parquet"
        inspection_status = "inspected_metadata_only"

    # 10. Raster Images (PNG, JPEG, GIF, ICO)
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        detected_format = "png_image"
        format_mismatch = ext not in (".png",)
        inspection_status = (
            "inspected_visual_and_metadata"
            if rel_path in VISUALLY_INSPECTED_IMAGES
            else "inspected_structured"
        )
        metrics = _parse_png_info(data)
    elif data[:2] == b"\xff\xd8":
        detected_format = "jpeg_image"
        format_mismatch = ext not in (".jpg", ".jpeg")
        inspection_status = (
            "inspected_visual_and_metadata"
            if rel_path in VISUALLY_INSPECTED_IMAGES
            else "inspected_structured"
        )
        metrics = _parse_jpeg_info(data)
    elif data[:6] in (b"GIF87a", b"GIF89a"):
        detected_format = "gif_image"
        format_mismatch = ext != ".gif"
        inspection_status = "inspected_structured"
        metrics = _parse_gif_info(data)
    elif data[:4] == b"\x00\x00\x01\x00" and ext == ".ico":
        detected_format = "ico_icon"
        inspection_status = "inspected_structured"
        metrics = _parse_ico_info(data)

    # 11. Web / Desktop Font binaries (.woff, .woff2, .ttf, .otf, .eot)
    elif ext in (".woff", ".woff2", ".ttf", ".otf", ".eot") or data[:4] in (b"wOFF", b"wOF2", b"OTTO"):
        magic_tag = data[:4].decode("latin1", errors="replace")
        detected_format = f"font_{ext.lstrip('.') or 'binary'}"
        inspection_status = "inspected_metadata_only"
        metrics = {"header_tag": repr(magic_tag)}

    # 12. UTF-8 Text, Code, Structured Config, SVG, CSV/TSV, HTML, Markdown
    else:
        try:
            text = data.decode("utf-8")
            is_utf8 = True
        except UnicodeDecodeError:
            is_utf8 = False
            text = ""

        if is_utf8 or ext in TEXT_EXTENSIONS or basename in TEXT_BASENAMES:
            if not is_utf8:
                text = data.decode("latin-1", errors="replace")
            if ext in (".html", ".htm"):
                detected_format, format_mismatch, inspection_status, metrics = _parse_html(
                    text, size_bytes
                )
            elif ext in (".md", ".markdown"):
                detected_format = "markdown_document"
                inspection_status = "inspected_full"
                metrics = _parse_markdown(text)
            elif ext == ".py":
                detected_format = "python_source"
                inspection_status = "inspected_full"
                metrics = _parse_python(text)
            elif ext in (".json",):
                detected_format = "json_document"
                try:
                    parsed = json.loads(text)
                    inspection_status = "inspected_full"
                    metrics = {
                        "top_type": type(parsed).__name__,
                        "top_len": len(parsed) if isinstance(parsed, (list, dict)) else 1,
                    }
                except json.JSONDecodeError as exc:
                    format_mismatch = True
                    inspection_status = "inspected_anomalous"
                    metrics = {"json_error": str(exc)}
            elif ext == ".jsonl":
                detected_format = "jsonl_ledger"
                lines = [ln for ln in text.splitlines() if ln.strip()]
                inspection_status = "inspected_full"
                metrics = {"record_count": len(lines)}
            elif ext == ".csv":
                detected_format = "csv_table"
                inspection_status = "inspected_full"
                metrics = _parse_delimited(text, ",")
            elif ext == ".tsv":
                detected_format = "tsv_table"
                inspection_status = "inspected_full"
                metrics = _parse_delimited(text, "\t")
            elif ext == ".svg":
                detected_format = "svg_vector_graphic"
                inspection_status = "inspected_full"
                vb = re.search(r'viewBox="([^"]+)"', text)
                metrics = {
                    "line_count": len(text.splitlines()),
                    "viewBox": vb.group(1) if vb else None,
                }
            elif ext == ".xml":
                detected_format = "xml_document"
                inspection_status = "inspected_full"
                metrics = {"line_count": len(text.splitlines())}
            elif ext in (".yml", ".yaml"):
                detected_format = "yaml_config"
                inspection_status = "inspected_full"
                metrics = {"line_count": len(text.splitlines())}
            elif ext in (".js", ".sh", ".rb", ".css", ".scss", ".gemspec") or basename in TEXT_BASENAMES:
                detected_format = f"source_{(ext.lstrip('.') or basename.lower())}"
                inspection_status = "inspected_full"
                metrics = {"line_count": len(text.splitlines())}
            else:
                detected_format = "plain_text"
                inspection_status = "inspected_full"
                metrics = {"line_count": len(text.splitlines())}

    return {
        "rel_path": rel_path,
        "size_bytes": size_bytes,
        "mtime_ns": mtime_ns,
        "mtime_utc": mtime_utc,
        "raw_sha256": raw_sha256,
        "working_git_blob_oid": working_blob_oid,
        "git_index_blob_oid": git_index_oid,
        "git_tracked": git_tracked,
        "git_dirty_vs_index": git_dirty,
        "ext": ext,
        "detected_format": detected_format,
        "format_mismatch": format_mismatch,
        "inspection_status": inspection_status,
        "summary_metrics": metrics,
    }
