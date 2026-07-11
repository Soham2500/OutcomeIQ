function downloadTextFile(content: string, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function escapeCsvCell(value: unknown): string {
  if (value === null || value === undefined) {
    return "";
  }
  const text = String(value);
  if (/[",\n\r]/.test(text)) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return text;
}

export function exportProjectSummaryAsJson(data: unknown, filename: string) {
  downloadTextFile(
    JSON.stringify(data, null, 2),
    filename,
    "application/json;charset=utf-8",
  );
}

export function exportProjectSummaryAsCsv(
  rows: Array<Record<string, unknown>>,
  filename: string,
) {
  if (rows.length === 0) {
    downloadTextFile("", filename, "text/csv;charset=utf-8");
    return;
  }

  const headers = Object.keys(rows[0]);
  const lines = [
    headers.map(escapeCsvCell).join(","),
    ...rows.map((row) => headers.map((header) => escapeCsvCell(row[header])).join(",")),
  ];
  downloadTextFile(lines.join("\n"), filename, "text/csv;charset=utf-8");
}
