// Web Worker running the python convertor in Pyodide, off the main thread
//
// @ts-ignore - resolved at runtime from the CDN
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs";

/**
 * Load Pyodide and install the convertor wheels (built by scripts/build-site.sh)
 */
async function init() {
  const pyodide = await loadPyodide();
  const resp = await fetch(new URL("wheels/wheels.json", import.meta.url));
  /** @type {string[]} */
  const wheels = await resp.json();
  await pyodide.loadPackage(
    wheels.map((w) => new URL(`wheels/${w}`, import.meta.url).href),
  );
  const { convert_file } = pyodide.pyimport("convertor.convert_odf");
  return { FS: pyodide.FS, convert_file };
}

const ready = init();

self.addEventListener("message", async (/** @type {MessageEvent} */ ev) => {
  /** @type {{id: number, content: ArrayBuffer}} */
  const { id, content } = ev.data;
  const input = `/tmp/${id}.odt`;
  const output = `/tmp/${id}-NEW.odt`;
  let FS;
  try {
    const py = await ready;
    FS = py.FS;
    FS.writeFile(input, new Uint8Array(content));
    py.convert_file(input, output);
    /** @type {Uint8Array} */
    const result = FS.readFile(output);
    self.postMessage({ id, result }, { transfer: [result.buffer] });
  } catch (exc) {
    self.postMessage({ id, error: String(exc) });
  } finally {
    for (const path of [input, output]) {
      try {
        FS?.unlink(path);
      } catch {}
    }
  }
});
