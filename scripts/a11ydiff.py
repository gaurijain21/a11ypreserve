from __future__ import annotations

import json
import sys
from pathlib import Path

from extract_semantics import extract


def compare(source: dict, output: dict) -> list[dict]:
    results = []
    def add(feature, src, out, result, reason):
        results.append({"feature": feature, "source": src, "output": out, "result": result, "reason": reason})
    if source.get("language"):
        if output.get("language") == source["language"]:
            add("document_language", source["language"], output.get("language"), "PRESERVED", "exact language value")
        elif output.get("language"):
            add("document_language", source["language"], output.get("language"), "MUTATED", "destination language differs")
        elif output.get("format") == "pdf" and not output.get("tagged"):
            add("document_language", source["language"], None, "LOST", "PDF supports /Lang, but output is not tagged and has no /Lang")
        else:
            add("document_language", source["language"], None, "LOST", "no destination language")
    if source.get("headings"):
        if output.get("headings") == source["headings"]:
            add("heading_hierarchy", source["headings"], output["headings"], "PRESERVED", "same heading sequence")
        elif output.get("format") == "pdf" and output.get("tagged"):
            add("heading_hierarchy", source["headings"], output.get("headings"), "MEASUREMENT_ERROR", "PDF tag parser not implemented")
        else:
            add("heading_hierarchy", source["headings"], output.get("headings"), "LOST", "no equivalent extracted structure")
    if source.get("images"):
        src_alt = [x.get("alt") for x in source["images"]]
        out_alt = [x.get("alt") for x in output.get("images", [])]
        if src_alt == out_alt:
            add("image_alt_text", src_alt, out_alt, "PRESERVED", "exact alternative text")
        elif output.get("format") == "pdf" and output.get("tagged"):
            add("image_alt_text", src_alt, out_alt, "MEASUREMENT_ERROR", "PDF is tagged but figure /Alt extraction is not implemented")
        elif out_alt and any(out_alt):
            add("image_alt_text", src_alt, out_alt, "MUTATED", "output contains different non-empty alternative text")
        elif output.get("format") == "pdf" and not output.get("tagged"):
            add("image_alt_text", src_alt, None, "LOST", "PDF supports figure /Alt, but output has no tagged structure")
        else:
            add("image_alt_text", src_alt, out_alt, "LOST", "no equivalent extracted alternative text")
    if source.get("lists"):
        if output.get("lists") == source["lists"]:
            add("list_nesting", source["lists"], output["lists"], "PRESERVED", "same nesting depths")
        elif output.get("format") == "pdf" and output.get("tagged"):
            add("list_nesting", source["lists"], output.get("lists"), "MEASUREMENT_ERROR", "PDF is tagged but list-structure extraction is not implemented")
        else:
            add("list_nesting", source["lists"], output.get("lists"), "DEGRADED", "list content exists but nesting differs or is unavailable")
    if source.get("table_headers"):
        if output.get("table_headers") == source["table_headers"]:
            add("table_headers", source["table_headers"], output["table_headers"], "PRESERVED", "same header presence")
        elif output.get("format") == "pdf" and output.get("tagged"):
            add("table_headers", source["table_headers"], output.get("table_headers"), "MEASUREMENT_ERROR", "PDF is tagged but table-structure extraction is not implemented")
        elif output.get("format") == "pdf" and not output.get("tagged"):
            add("table_headers", source["table_headers"], None, "LOST", "PDF supports table structure, but output is not tagged")
        else:
            add("table_headers", source["table_headers"], output.get("table_headers"), "LOST", "no equivalent extracted header semantics")
    return results


def main(source_path: str, output_path: str) -> None:
    source = extract(Path(source_path))
    output = extract(Path(output_path))
    report = {"source": source_path, "output": output_path, "features": compare(source, output)}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
