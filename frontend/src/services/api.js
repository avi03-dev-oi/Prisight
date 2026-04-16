const BASE = "http://127.0.0.1:8000";

export async function api(url, method = "GET", body, isForm = false) {
  const res = await fetch(BASE + url, {
    method,
    headers: isForm ? {} : { "Content-Type": "application/json" },
    body: body
      ? isForm
        ? body
        : JSON.stringify(body)
      : null,
  });

  if (!res.ok) throw await res.json();
  return res.json();
}
