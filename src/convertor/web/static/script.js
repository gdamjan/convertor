const dropArea = document.querySelector("#drop-area");
/** @type {HTMLInputElement} */
const fileInput = document.querySelector("#file-input");
const fileListContainer = document.querySelector("#file-list-container");

/**
 * @param {FileList} files
 */
function handleFileAdd(files) {
  for (const file of files) {
    if (!isValidFileType(file.type)) continue;

    const fileItem = document.createElement("div");
    fileItem.classList.add("not-ready");
    fileItem.textContent = `${file.name}`;
    fileListContainer.appendChild(fileItem);

    const reader = new FileReader();
    reader.readAsArrayBuffer(file);

    reader.addEventListener("loadend", (e) => {
      fileItem.classList.remove("not-ready");
      fileItem.classList.add("ready");
      // considering we used readAsArrayBuffer above, and it's not null in this callback, cast to ArrayBuffer
      const fileContent = /** @type {ArrayBuffer} */ (e.target.result);

      fileItem.addEventListener(
        "click",
        async () => {
          fileItem.classList.add("upload-in-progress");
          const success = await convertFile(file.name, fileContent);
          fileItem.classList.remove("upload-in-progress");
          fileItem.classList.add(success ? "success" : "error");
        },
        { once: true },
      );
    });
  }
}

/**
 * Where to convert: on the server by default, or in the browser with Pyodide
 * when the site ships the python wheels (the static site, e.g. GitHub Pages).
 * @type {Promise<"server" | "wasm">}
 */
const backend = fetch("wheels/wheels.json", { method: "HEAD" }).then(
  (resp) => (resp.ok ? "wasm" : "server"),
  () => "server",
);

/**
 * The in-browser conversion runs in Pyodide inside a Web Worker.
 * It's only started in wasm mode, as it downloads the whole python runtime.
 * @type {Worker | undefined}
 */
let worker;
let nextId = 0;
/** @type {Map<number, {resolve: (result: Uint8Array<ArrayBuffer>) => void, reject: (error: string) => void}>} */
const pending = new Map();

function getWorker() {
  if (worker === undefined) {
    worker = new Worker("worker.js", { type: "module" });
    worker.addEventListener("message", (/** @type {MessageEvent} */ ev) => {
      const { id, result, error } = ev.data;
      const request = pending.get(id);
      if (request === undefined) return;
      pending.delete(id);
      error === undefined ? request.resolve(result) : request.reject(error);
    });
  }
  return worker;
}

// in wasm mode, start loading python right away, while the user picks files
backend.then((b) => b === "wasm" && getWorker());

/**
 * @param {ArrayBuffer} fileContent
 * @returns {Promise<Blob>}
 */
async function convertInWorker(fileContent) {
  const id = nextId++;
  /** @type {Uint8Array<ArrayBuffer>} */
  const result = await new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    // copy, so the file can be converted again
    getWorker().postMessage({ id, content: fileContent.slice(0) });
  });
  return new Blob([result], {
    type: "application/vnd.oasis.opendocument.text",
  });
}

/**
 * @param {ArrayBuffer} fileContent
 * @returns {Promise<Blob>}
 */
async function convertOnServer(fileContent) {
  const resp = await fetch("upload", { method: "PUT", body: fileContent });
  if (!resp.ok) {
    throw new Error(`server error ${resp.status}`);
  }
  return await resp.blob();
}

/**
 * @param {ArrayBuffer} fileContent
 * @returns {Promise<Blob>}
 */
async function convert(fileContent) {
  return (await backend) === "wasm"
    ? await convertInWorker(fileContent)
    : await convertOnServer(fileContent);
}

/**
 * @param {string} fileName
 * @param {ArrayBuffer} fileContent
 * @returns {Promise<boolean>}
 */
async function convertFile(fileName, fileContent) {
  try {
    const blob = await convert(fileContent);
    const blobUrl = window.URL.createObjectURL(blob);
    // create fake link and initiate download
    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = fileName.replace(/(\.odt)?$/i, "-NEW.odt");
    a.click();
    return true;
  } catch (exc) {
    console.log(exc);
    return false;
  }
}

/**
 * @param {string} type
 * @returns boolean
 */
function isValidFileType(type) {
  const allowedTypes = ["application/vnd.oasis.opendocument.text"];
  return allowedTypes.includes(type);
}

dropArea.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", () => {
  handleFileAdd(fileInput.files);
});

dropArea.addEventListener("drop", (/** @type {DragEvent} */ ev) => {
  preventDefaults(ev);
  dropArea.classList.remove("drag-over", "drag-reject");
  handleFileAdd(ev.dataTransfer.files);
});

dropArea.addEventListener("dragover", (/** @type {DragEvent} */ ev) => {
  preventDefaults(ev);
  /** @type {boolean} */
  let allow = false;
  if (ev.dataTransfer !== null) {
    // if there's at least one allowed file, then fine, we'll filter the rest later
    allow = Array.prototype.some.call(
      ev.dataTransfer.items,
      (/** @type {DataTransferItem}*/ item) => {
        return isValidFileType(item.type) && item.kind === "file";
      },
    );
  }

  if (allow) {
    dropArea.classList.add("drag-over");
    ev.dataTransfer.dropEffect = "copy";
  } else {
    dropArea.classList.add("drag-reject");
    ev.dataTransfer.dropEffect = "none";
  }
});

dropArea.addEventListener("dragleave", (ev) => {
  preventDefaults(ev);
  dropArea.classList.remove("drag-over", "drag-reject");
});

dropArea.addEventListener("dragenter", preventDefaults);

/**
 * Help popup dialog
 */
/** @type {HTMLDialogElement} */
const dialog = document.querySelector("#help-dialog");
const showButton = document.querySelector("#help-fab>button");
const closeButton = document.querySelector("#help-dialog button");

showButton.addEventListener("click", () => {
  dialog.showModal();
});

closeButton.addEventListener("click", () => {
  dialog.close();
});

dialog.addEventListener("click", () => {
  dialog.close();
});

/** Keyboard shortcuts */
document.addEventListener("keydown", function (ev) {
  if (ev.key === "?") {
    preventDefaults(ev);
    dialog.showModal();
    return;
  }
  if (ev.key === "o") {
    preventDefaults(ev);
    fileInput.click();
    return;
  }
});

/**
 * Service Worker to enable offline use
 */
if ("serviceWorker" in navigator) {
  try {
    // relative paths, so it works under a sub-path like GitHub Pages
    const registration = await navigator.serviceWorker.register("sw.js");
    if (registration.installing) {
      console.log("Service worker for offline use - installing");
    } else if (registration.waiting) {
      console.log("Service worker for offline use - installed");
    } else if (registration.active) {
      console.log("Service worker for offline use - active");
    }
  } catch (error) {
    console.error(
      `Service worker for offline use - Registration failed with ${error}`,
    );
  }
}

/**
 * Utility function to prevent default browser behavior
 * @param {Event} ev
 */
function preventDefaults(ev) {
  ev.preventDefault();
  ev.stopPropagation();
  return false;
}

// prevent droping on the html body to avoid mis-drops
document.body.addEventListener("dragstart", preventDefaults);
document.body.addEventListener("dragenter", preventDefaults);
document.body.addEventListener("dragover", preventDefaults);
document.body.addEventListener("drop", preventDefaults);

// this is an ES module
export {};
